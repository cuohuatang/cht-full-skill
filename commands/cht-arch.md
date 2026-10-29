---
name: cht-arch
description: 阶段 2.5，把方案/代码库画成可交互架构图（architecture/tree/workflow/sequence/dataflow/lifecycle/erd/class/timeline/waterfall）。强制"源码证据、不编造"门禁，优先用 archify 真引擎，无 Node 时回退到便携渲染器。
version: "0.1.0"
---

# /cht-arch — 架构可视化（archify 嫁接）

把方案、流程、状态机或真实代码库，画成**自包含、可交互、双击就能看**的 HTML 图。详见 `references/12-archify.md`。

## 执行

1. **选 type**：`architecture` `tree` `workflow` `sequence` `dataflow` `lifecycle` `erd` `class` `timeline` `waterfall`（见参考 §2）。
2. **逼出事实，不编造**（门禁，参考 §4）：真实代码库图的每个节点/边都要有 `file:line` 或命令输出证据；拿不到的标 `unverified` 并说明；示意值必须在图注声明。
3. **写候选 JSON**：结构见 `references/12-archify.md §3`；形状参考 `archify/examples/*.json`（只学形状，别抄事实）。每个条目可带 `evidence` 字段。
4. **渲染**（自动二选一）：
   - 有 `node` 且 `archify/bin/archify.mjs` 存在 →
     `node archify/bin/archify.mjs finalize <type> <candidate.json> <out.html> --quality showcase --json`
     真实仓库图加 `--repo-root <repo>` 做证据校验。
   - 否则 → `python3 scripts/archify_lite.py <type> <candidate.json> <out.html>`（零依赖，离线可用）。
5. **过门禁再交付**：统计 `unverified` 项，存在未声明编造 → 不许说"图好了"（第三条铁律）。交付时给可点击的绝对路径链接 + 一句读法说明（省略了什么、哪些是示意）。

## 输出

- 单条可点击 Markdown 链接指向生成的 HTML（绝对路径，含空格用 `<...>` 包裹）。
- 一句话关键结论；说明抽象层级、刻意省略、示意值、缺失证据。
- 例：`画好 [Checkout 平台架构](/abs/path/checkout.html)。数据库主从为示意，未读源码确认。`

## 禁止

- 静默编造调用关系 / 字段 / 状态 / 耗时
- 把示意值当实测值陈述
- 图里的事实与 `PLAN.md`/`REVIEW.md`/`QA-REPORT.md` 矛盾却不说明

## 完成判据

- [ ] type 选对
- [ ] 每个节点/边有证据或标 `unverified`
- [ ] 示意值已在图注声明
- [ ] 渲染成功（真引擎四门禁通过 / 便携渲染器无报错）
- [ ] 图事实与文档一致
- [ ] 已给可点击链接 + 读法说明
