#!/usr/bin/env python3
# cht-full-skill · Graphify → Semantica 两段式桥接（V0.3.0）
#
# 只用 Python 标准库，0 第三方依赖；不 import graphify，也不 import semantica。
# 它做的不是「把图存进数据库」，而是把 Graphify 的 graph.json 翻译成
# 带 W3C PROV-O 语义的 lineage 中间格式，供 Semantica 摄入侧按映射落库。
#
# 用法：
#   python3 scripts/graph_bridge.py --env                      外部工具可用性（不自动安装）
#   python3 scripts/graph_bridge.py --plan                    两段式命令序列
#   python3 scripts/graph_bridge.py --verify graph.json        校验 graph.json 结构
#   python3 scripts/graph_bridge.py --bridge graph.json --out docs/cht/code-graph/lineage.json
#   python3 scripts/graph_bridge.py --selftest                内置三态回归，失败非零退出
#
# ⚠️ 诚实标注：Graphify 与 Semantica 上游之间**没有官方集成**。
#    下面的 EXTRACTED/INFERRED/AMBIGUOUS → PROV-O 映射是 cht 定义的适配约定，
#    不是任何一方的官方行为；lineage.json 是中间格式，真正入库仍需 Semantica 摄入侧实现。
#    完整契约见 references/26-code-graph-pipeline.md

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"
VALID_CONFIDENCE = ("EXTRACTED", "INFERRED", "AMBIGUOUS")

CONTRACT = {
    "EXTRACTED": {
        "prov": "prov:wasDerivedFrom",
        "target": "source_file#source_location",
        "cht_status": "verified",
        "admitted": True,
        "note": "源码显式关系，AST/解析确定性得出，可直接入图",
    },
    "INFERRED": {
        "prov": "prov:wasGeneratedBy",
        "target": "cht:inference-activity",
        "cht_status": "inferred",
        "admitted": True,
        "note": "推断关系，入图但必须保留 confidence_score 与推理活动来源",
    },
    "AMBIGUOUS": {
        "prov": "prov:wasGeneratedBy",
        "target": "cht:uncertain-activity",
        "cht_status": "needs_review",
        "admitted": False,
        "note": "不确定关系，只进复核队列，绝不混入正式图（不把猜测当事实）",
    },
}


def load_graph(path):
    """读取 Graphify 的 graph.json。真实结构是 NetworkX node-link：nodes + links。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("graph.json 顶层必须是对象")
    links = data.get("links")
    if links is None:  # 兼容部分版本/导出器使用 edges
        links = data.get("edges")
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not isinstance(links, list):
        raise ValueError("graph.json 需要 nodes 列表 + links(或 edges)列表")
    return data, nodes, links


def verify(data, nodes, links):
    """结构校验：不猜、不补全，缺什么报什么。

    注意：extraction-spec.md 里的「confidence_score REQUIRED」约束的是 LLM 抽取
    子 Agent 的输出；真实 graph.json 的 AST 代码路径会产出不带分数的 INFERRED 边
    （上游 worked/httpx 样例 330 边中有 156 条如此）。故此项只作警告，不阻断。
    """
    problems = []
    counts = {k: 0 for k in VALID_CONFIDENCE}
    counts["UNKNOWN"] = 0
    missing_source_file = 0
    unscored_inferred = 0
    for i, e in enumerate(links):
        if not isinstance(e, dict):
            problems.append(f"links[{i}] 不是对象")
            continue
        for key in ("source", "target", "relation", "confidence"):
            if not e.get(key):
                problems.append(f"links[{i}] 缺 {key}")
        conf = str(e.get("confidence", "")).upper()
        if conf in counts:
            counts[conf] += 1
        else:
            counts["UNKNOWN"] += 1
            problems.append(f"links[{i}] confidence 非法: {conf or '<空>'}")
        if conf == "INFERRED" and e.get("confidence_score") is None:
            unscored_inferred += 1
        if not e.get("source_file"):
            missing_source_file += 1
    warnings = []
    if unscored_inferred:
        warnings.append(
            f"{unscored_inferred} 条 INFERRED 边没有 confidence_score（AST 路径常见）；"
            "桥接时保持 null、不猜分，标记为 inferred_unscored"
        )
    return {
        "ok": not problems,
        "schema": "graphify node-link (nodes + links)",
        "nodes": len(nodes),
        "links": len(links),
        "by_confidence": counts,
        "links_missing_source_file": missing_source_file,
        "inferred_without_score": unscored_inferred,
        "warnings": warnings,
        "problems": problems[:20],
        "problems_total": len(problems),
    }


def bridge(data, source_label):
    """把 Graphify 的边翻译成 PROV-O lineage 中间格式。"""
    nodes = data.get("nodes") or []
    links = data.get("links")
    if links is None:
        links = data.get("edges") or []

    lineage = []
    review_queue = []
    counts = {k: 0 for k in VALID_CONFIDENCE}
    counts["INVALID"] = 0

    for i, e in enumerate(links):
        e = e if isinstance(e, dict) else {}
        raw = e.get("confidence")
        conf = str(raw or "").upper()
        rule = CONTRACT.get(conf)
        src_file = e.get("source_file")
        src_loc = e.get("source_location")
        rec = {
            "id": f"cht:edge/{i:04d}",
            "source": e.get("source"),
            "target": e.get("target"),
            "relation": e.get("relation"),
            "graphify_confidence": conf or None,
            "source_file": src_file,
            "source_location": src_loc,
            "confidence_score": e.get("confidence_score"),
            "also_seen": e.get("also_seen"),
        }
        if rule:
            counts[conf] += 1
            rec["prov"] = rule["prov"]
            rec["prov_target"] = (
                f"{src_file or 'unknown'}#{src_loc or ''}"
                if conf == "EXTRACTED"
                else rule["target"]
            )
            rec["cht_status"] = rule["cht_status"]
            rec["admitted"] = rule["admitted"]
            rec["note"] = rule["note"]
            # Graphify 硬约定：EXTRACTED 恒为 1.0（见 how-it-works.md），缺失时按契约补齐
            if conf == "EXTRACTED" and rec["confidence_score"] is None:
                rec["confidence_score"] = 1.0
            # AST 路径的 INFERRED 边可能没有分数：保持 null、绝不猜一个 0.5
            if conf == "INFERRED" and rec["confidence_score"] is None:
                rec["cht_status"] = "inferred_unscored"
                rec["note"] = "上游未提供 confidence_score；保持 null、不猜分，入图但标记为未打分"
            if not rule["admitted"]:
                review_queue.append(rec["id"])
        else:
            counts["INVALID"] += 1
            rec.update({
                "prov": None,
                "prov_target": None,
                "cht_status": "invalid_confidence",
                "admitted": False,
                "note": "confidence 不在三态内，一律拦下不入库",
            })
            review_queue.append(rec["id"])
        lineage.append(rec)

    admitted = sum(1 for r in lineage if r["admitted"])
    return {
        "bridge_version": VERSION,
        "source_graph": source_label,
        "source_schema": "graphify node-link (nodes + links)",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "upstream_integration": "none — 映射由 cht 定义，非 Graphify/Semantica 官方集成",
        "contract": CONTRACT,
        "summary": {
            "nodes": len(nodes),
            "links": len(links),
            "by_confidence": counts,
            "admitted": admitted,
            "held_for_review": len(review_queue),
            "inferred_unscored": sum(1 for r in lineage if r.get("cht_status") == "inferred_unscored"),
        },
        "lineage": lineage,
        "review_queue": review_queue,
    }


def env_report():
    """只检测，绝不自动安装。"""
    g = shutil.which("graphify")
    s = importlib.util.find_spec("semantica") is not None
    return {
        "graphify_cli": g or "NOT_FOUND",
        "semantica_package": "AVAILABLE" if s else "NOT_FOUND",
        "python": sys.version.split()[0],
        "install_hints": {
            "graphify": "uv tool install graphifyy   # 包名是双 y；然后 graphify install 注册 /graphify skill",
            "semantica": "pip install semantica     # 生产部署另需 Docker/Compose + 图存储后端",
        },
        "note": "cht 不捆绑任何引擎；以上均由用户自行安装，脚本只会检测。",
    }


PLAN = """[1] 建图 —— Graphify（把代码变成图，外部工具，cht 不捆绑）
    uv tool install graphifyy          # 包名 graphifyy 是双 y
    graphify install                   # 注册 /graphify skill 到你的 Agent
    /graphify .                        # 产出 graph.html / GRAPH_REPORT.md / graph.json
    规范：skills/graphify/references/extraction-spec.md、how-it-works.md、query.md

[2] 校验 + 桥接 —— cht（本脚本，纯标准库）
    python3 scripts/graph_bridge.py --verify <graph.json>
    python3 scripts/graph_bridge.py --bridge <graph.json> --out docs/cht/code-graph/lineage.json
    契约：EXTRACTED → prov:wasDerivedFrom；INFERRED → prov:wasGeneratedBy(保留置信分)；
          AMBIGUOUS → 只进复核队列，不入正式图

[3] 入库与搜索 —— Semantica（把图存好、搜得到，外部工具，cht 不捆绑）
    pip install semantica
    semantica doctor
    按 lineage.json 的映射把 admitted=true 的边摄入 ContextGraph，
    每条边附 PROV-O 来源记录；review_queue 里的边保持隔离待人工确认
    参考：skills/semantica/SKILL.md、references/glossary.md

[4] 查来源
    graphify query / path / explain     # 图内遍历，答案是一条可核对的路径
    Semantica provenance / decision trace  # 事实与决策的因果链、时间点快照
    ⚠️ 第 3 步的摄入代码需按 lineage.json 映射自行实现，上游没有现成适配器
"""


def selftest():
    """内置三态回归；用与 Graphify 真实结构一致的 nodes + links。"""
    sample = {
        "directed": True, "multigraph": False, "graph": {},
        "nodes": [
            {"id": "svc_order", "label": "OrderService", "file_type": "code",
             "source_file": "src/order.py", "source_location": "L1"},
            {"id": "svc_pay", "label": "PaymentClient", "file_type": "code",
             "source_file": "src/pay.py", "source_location": "L1"},
            {"id": "doc_spec", "label": "Spec", "file_type": "document",
             "source_file": "docs/spec.md", "source_location": "L1"},
        ],
        "links": [
            {"source": "svc_order", "target": "svc_pay", "relation": "calls",
             "confidence": "EXTRACTED", "source_file": "src/order.py", "source_location": "L42"},
            {"source": "svc_order", "target": "doc_spec", "relation": "conceptually_related_to",
             "confidence": "INFERRED", "confidence_score": 0.85,
             "source_file": "docs/spec.md", "source_location": "L7"},
            {"source": "svc_pay", "target": "doc_spec", "relation": "semantically_similar_to",
             "confidence": "AMBIGUOUS", "confidence_score": 0.2,
             "source_file": "docs/spec.md", "source_location": "L9"},
        ],
    }
    checks = []

    def chk(name, cond):
        checks.append((name, bool(cond)))

    nodes, links = sample["nodes"], sample["links"]
    v = verify(sample, nodes, links)
    chk("verify 判定合法", v["ok"])
    chk("verify 三态计数各 1", all(v["by_confidence"][k] == 1 for k in VALID_CONFIDENCE))

    out = bridge(sample, "<selftest>")
    by_id = {r["id"]: r for r in out["lineage"]}
    e0, e1, e2 = by_id["cht:edge/0000"], by_id["cht:edge/0001"], by_id["cht:edge/0002"]
    chk("EXTRACTED → wasDerivedFrom", e0["prov"] == "prov:wasDerivedFrom")
    chk("EXTRACTED 保留源码路径#行号", e0["prov_target"] == "src/order.py#L42")
    chk("EXTRACTED 缺分数时按契约补 1.0", e0["confidence_score"] == 1.0)
    chk("EXTRACTED 直接入图", e0["admitted"] is True)
    chk("INFERRED → wasGeneratedBy", e1["prov"] == "prov:wasGeneratedBy")
    chk("INFERRED 保留 0.85 不猜", e1["confidence_score"] == 0.85)
    chk("INFERRED 入图但标 inferred", e1["admitted"] is True and e1["cht_status"] == "inferred")
    chk("AMBIGUOUS 不入正式图", e2["admitted"] is False)
    chk("AMBIGUOUS 进复核队列", "cht:edge/0002" in out["review_queue"])
    chk("汇总 admitted=2 / held=1", out["summary"]["admitted"] == 2 and out["summary"]["held_for_review"] == 1)

    bad = {"nodes": [], "links": [{"source": "a", "target": "b", "relation": "x", "confidence": "GUESSED"}]}
    chk("非法 confidence 被拦下", bridge(bad, "<bad>")["summary"]["by_confidence"]["INVALID"] == 1)
    edges_variant = {"nodes": [], "edges": [dict(links[0])]}
    chk("兼容 edges 键名", len(bridge(edges_variant, "<edges>")["lineage"]) == 1)
    chk("verify 能报缺字段", not verify({"nodes": [], "links": [{"source": "a"}]}, [], [{"source": "a"}])["ok"])

    # 真实 AST 路径：INFERRED 边不带分数 → 警告而非阻断，且绝不猜分
    noscore = {"nodes": [], "links": [
        {"source": "a", "target": "b", "relation": "calls",
         "confidence": "INFERRED", "source_file": "a.py"}]}
    v2 = verify(noscore, [], noscore["links"])
    chk("INFERRED 无分数时 verify 仍通过", v2["ok"])
    chk("无分数计入 warnings", v2["inferred_without_score"] == 1 and len(v2["warnings"]) == 1)
    r2 = bridge(noscore, "<noscore>")["lineage"][0]
    chk("无分数保持 null、不猜值", r2["confidence_score"] is None)
    chk("无分数标 inferred_unscored", r2["cht_status"] == "inferred_unscored")

    failed = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'✓' if ok else '✗'} {n}")
    total = len(checks)
    print(f"\n自测结果：{total} 例，通过 {total - len(failed)}，失败 {len(failed)}")
    return not failed


def main():
    ap = argparse.ArgumentParser(description="Graphify → Semantica 两段式桥接（cht-full-skill）")
    ap.add_argument("--env", action="store_true", help="检测外部工具可用性，不自动安装")
    ap.add_argument("--plan", action="store_true", help="输出两段式命令序列")
    ap.add_argument("--verify", metavar="GRAPH_JSON", help="校验 graph.json 结构")
    ap.add_argument("--bridge", metavar="GRAPH_JSON", help="生成 PROV-O lineage 中间格式")
    ap.add_argument("--out", metavar="PATH", help="配合 --bridge 写到文件（默认 stdout）")
    ap.add_argument("--selftest", action="store_true", help="内置三态回归")
    a = ap.parse_args()

    if a.selftest:
        return 0 if selftest() else 1
    if a.env:
        print(json.dumps(env_report(), ensure_ascii=False, indent=2))
        return 0
    if a.plan:
        print(PLAN)
        return 0
    if a.verify:
        try:
            data, nodes, links = load_graph(a.verify)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"✗ 读取失败：{exc}", file=sys.stderr)
            return 1
        rep = verify(data, nodes, links)
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0 if rep["ok"] else 1
    if a.bridge:
        try:
            data, _, _ = load_graph(a.bridge)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"✗ 读取失败：{exc}", file=sys.stderr)
            return 1
        payload = json.dumps(bridge(data, a.bridge), ensure_ascii=False, indent=2)
        if a.out:
            p = Path(a.out)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(payload + "\n", encoding="utf-8")
            print(f"✓ 已写出 {p}  sha256={hashlib.sha256(payload.encode()).hexdigest()[:16]}")
        else:
            print(payload)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
