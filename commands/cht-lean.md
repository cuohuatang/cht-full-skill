---
name: cht-lean
description: 极简代码一键入口。治 AI 过度设计：写之前爬 6 步决策阶梯（已有代码→标准库→已装依赖→一行→最少代码），写完查肥肉（diff 评审/全仓审计/捷径债台账）。受 Ponytail（DietrichGebert，MIT，Ponytail 5）启发，六个上游 skill 原样嫁入 skills/ponytail*/。
version: "0.4.0"
license: MIT
---

# /cht-lean · 极简代码（Ponytail 范围纪律）

> 六个上游 skill **原样嫁入**（sha256 与上游一致）：`skills/ponytail/`、`ponytail-review/`、`ponytail-audit/`、`ponytail-debt/`、`ponytail-gain/`、`ponytail-help/` + `skills/ponytail/LICENSE`（MIT）。
> 方法论重述与 cht 集成边界见 `references/20-lean-code.md`。

## 与 /cht-ub 的分工（不要混用）

- `/cht-lean` 管**范围**：决定"一开始就不写多余的部分"（写前阶梯 + 写后查肥肉）。
- `/cht-ub` 管**过程**：决定"怎么把要写的做对"（三段式 + 量化门）。
- 典型组合：`/cht-lean` 砍范围 → 三段式交付 → 量化门收尾。

## 调用形态

| 形态 | 触发 | 做什么 |
|---|---|---|
| 默认 | `/cht-lean` 或"别过度设计 / 最简方案 / yagni" | 对当前任务激活 **full 档**：先爬 6 步阶梯，产出最小完整改动，结尾一行交代"跳过了什么/没查什么/风险" |
| 切档 | `/cht-lean lite` / `ultra` / `off` | lite=只做被要求的并点名更小选项；ultra=动手前质询请求本身；off=退出。档位持续本会话 |
| diff 评审 | `/cht-lean review`（或"这段改得是不是过度了"） | 按 `skills/ponytail-review/SKILL.md` 走：先读懂 diff 触及的全部代码（调用方/被调方/测试），六维找问题，每条发现四要素 + 编号，结尾 `Verdict:` 与 `Lean: -N 行`；**只报告不改代码** |
| 全仓审计 | `/cht-lean audit`（或"哪些能删 / 哪里过度设计"） | 按 `skills/ponytail-audit/SKILL.md` 走：建图先行（入口/数据流/预期负载），按代价深挖而非逐文件，六维 + 三分组最多 20 条，结尾 `Verdict:` + `Lean: -N 行, -M 依赖` + `Not checked:`；**只报告不改代码** |
| 捷径债台账 | `/cht-lean debt` | 按 `skills/ponytail-debt/SKILL.md` 走：grep 全仓 `shortcut:` 注释（跳过 .git 与 .gitignore 覆盖物），逐条"上限 + 升级触发器"，**无触发器的标 `no-trigger` 并置顶警告**；持久化前先问用户 |
| 收益记分牌 | `/cht-lean gain` | 按 `skills/ponytail-gain/SKILL.md` 走：只展示官方基准数字（39 任务×5 次：LOC −53% / token −45% / 成本 −26% / 时间 −41%），**禁止编造本仓库节省数字** |
| 帮助 | `/cht-lean help` | 按 `skills/ponytail-help/SKILL.md` 展示速查卡 |

## 6 步决策阶梯（写任何代码前，从上往下取第一个能完整解决的）

```
1. 真需要存在吗？    没人要的功能/选项/灵活性 → 砍，一行点名砍了什么
2. 代码库已有？      按周边代码的用法用现成 helper/组件/模式
3. 标准库/平台能力？  能做就用（自家封装 > 原生控件）
4. 已装依赖能做？    能做就用；绝不为几行代码新增依赖
5. 一行能搞定？      读者一眼能懂的一行就一行
6. 都不行            → 能工作的最少代码
```

配套：对方案懒、对事情不懒（调用方/测试/fixture 全收尾）；删除优于新增；修 bug 先 grep 所有调用方、在共享代码修根因；非平凡逻辑（尤其**金额与安全**）留一个小测试；捷径写成 `shortcut: <上限>, <何时升级>`。

## 输出模板（默认形态）

```
档位：full（lite/ultra/off 注明）
阶梯：1✗ 2✗ 3✓ → <选了哪步、为什么上一步不行>
改动：<最小完整改动；触及的调用方/测试/fixture 清单>
跳过：<一行点名没做的部分>
未查/风险：<一行>
```

## 红牌（违反即停）

- 以"ponytail"为借口砍用户明确要求的功能或校验——**Never cut：信任边界校验/防数据丢失错误处理/安全/可访问性/用户要求的一切**。
- 新增依赖/抽象层/配置项却给不出阶梯 1–5 步为何都不行的证据。
- 编造"本仓库节省 X 行/X token"（没写出来的版本没有基线）。
- 用档位静默改写用户需求而不是推回确认（ultra 是推回，不是自作主张）。
- **cht 三条铁律永远 > ponytail 懒规则**：懒 ≠ 少验证，没跑过的不许说完成；金额/安全/鉴权改动必须过 `/cht-doctor` 四层验证门。
- review/audit/debt 是只读报告——借机改代码即违规。
