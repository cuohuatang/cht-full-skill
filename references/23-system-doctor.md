# 系统体检与自修复闭环（T0 检测技能组 · V0.0.9）

> 面向"已经开发到 90%、逻辑有点乱、全插件化的系统"：全面查**不合理逻辑 / 没连通 / 空壳**，再分级自修复。
> 本文是**编排说明**——把 cht-full-skill 里已有的检测能力串成一条闭环，并补上唯一缺的"壳检测"引擎。

## 先说清楚：这次嫁了什么、没嫁什么

**诚实标注，避免"假嫁接"**——本闭环共 5 组能力，其中 **4 组本来就在这仓库里**（V0.0.3 从 ECC 嫁入的 234 个技能自带），本次做的是**编排**：给它们一个统一入口（`/cht-doctor`）、一份调度顺序、一条验证闭环。真正新增的只有 1 个引擎。

| # | 能力 | 来源 | 本次动作 |
|---|---|---|---|
| 1 | **扫壳**（占位 / 假数据 / stub） | [`theater-detection-audit`](https://github.com/DNYoussef/ai-chrome-extension/tree/main/.claude/skills/theater-detection-audit) · **MIT** | ✅ **新增引擎**，整包嫁入 `skills/theater-detection-audit/` |
| 2 | 插件/连接器**盘点**（live / broken / missing） | `workspace-surface-audit` + `automation-audit-ops`（ECC，MIT） | 编排，已内置 |
| 3 | **断链**分析（调用链 / 契约 / 数据流） | `module-regression` + `change-impact`（ECC，MIT） | 编排，已内置 |
| 4 | **不合理逻辑** + 存量系统体检 | `brownfield-retrospective` + `production-audit`（ECC，MIT） | 编排，已内置 |
| 5 | **验证闭环**（防"假修好"） | `verification-loop` + `delivery-gate` / `gateguard`（ECC，MIT） | 编排，已内置 |

> 未嫁：Codebase Health Auditor / Millie Fix / heal-skill 三个外部技能来自聚合站、**仓库级许可未声明**，按本仓库一贯纪律（ub-mode 无许可即只做原创重述）**不复制其文件**，仅在文末留外链指针。其中 `heal-skill` 修的是 skill 库自身而非业务代码，尤其别误用。

## 四类问题 → 谁来查

| 用户说的 | 技术定义 | 负责技能 | 产出 |
|---|---|---|---|
| **"哪些是壳"** | 硬编码 mock、stub 空函数、TODO/FIXME/HACK、被注释掉的真逻辑、假错误处理、test-mode 分支 | `theater-detection-audit` | 逐项 `文件:行号 + 触发模式 + 上下文 + 补全建议` |
| **"没连通"** | 注册了没人调 / 调了没实现 / 接口契约不匹配 / 上游产出下游没消费 | `workspace-surface-audit`、`automation-audit-ops`、`module-regression`、`change-impact` | 插件清单 + 下游消费者台账 + 断裂点 |
| **"不合理"** | 逻辑绕、结构坏味、缺验收、上线会炸的点 | `brownfield-retrospective`、`production-audit` | 四轴差距台账 + 上线就绪清单 |
| **"自我修复"** | 改完必须证明真的好了 | `verification-loop`、`delivery-gate`、`gateguard` | 四层验证门结果 |

## 七步闭环（`/cht-doctor` 的调度顺序）

```
1. 盘点   workspace-surface-audit / automation-audit-ops
          → 全量插件清单，逐个标 live / broken / redundant / missing
          → 先出 keep / merge / cut / fix 建议，不动任何代码

2. 扫壳   theater-detection-audit
          → 按 7 类 theater 模式扫描（见下节），逐项读完整上下文
          → 关键：区分「故意留的扩展点」与「忘了实现的 stub」，别一刀切

3. 查断链 module-regression / change-impact
          → 为每个模块建下游消费者台账，走调用路径 / API 契约 / 数据流 / 回滚
          → 找出"注册了没人调""改 A 断了 B"

4. 判合理 brownfield-retrospective / production-audit
          → 四轴差距台账（思考 / 编码实践 / 缺失文件 / 决策重建）
          → 本地证据的上线就绪审计，不把代码发到外部服务

5. 分级   P0 阻断（崩溃 / 断链 / 数据错）
          P1 空壳补全（有明确实现意图的占位）
          P2 优化建议（结构 / 命名 / 去重 / 文档）

6. 修复   只自动修 P0；P1 逐条给 diff 让人确认；P2 只报告不动手
          → 检测与修复拆成独立上下文/隔离副本，别边查边改
          → 每次改动小批、可回滚

7. 验证   verification-loop（build / typecheck / lint / tests+coverage / security grep / diff review）
          + delivery-gate / gateguard（四层门：问题清零 / 产物完整 / 数据流完整 / 零绕过）
          → 四层全过才说"完成"，否则回到第 6 步
```

**四层验证门**（`references/23` 采用的硬标准，缺一层不算过）：
1. **Issues Clear** — 检测到的问题全部有结论
2. **Output Complete** — 预期文件都存在且内容有效（不是空占位文件）
3. **Data Flow Intact** — 上游产出确实被下游消费（专治"没连通"）
4. **Zero Workarounds** — 执行链里没有绕过行为

## 插件化系统的三个特殊注意点

1. **"壳"不等于 bug**。插件架构里大量空实现是**设计上的扩展点**（接口、钩子、预留槽位）。自动补全很可能把预留接口写成错误逻辑，比不改更危险。第 2 步必须逐项判"故意 / 未完成"，不确定的一律降级到 P1 交人确认。
2. **"没连通"可能是解耦**。插件靠注册表/事件总线松耦合，静态扫调用链本就看不到连接。判定断链前先查注册机制与运行时装配，别把"通过总线连接"误报成断链。
3. **改一个插件会带崩别的**。`module-regression` 的下游消费者台账是这里的保险——修复后必须跑**变更模块 + 所有受影响下游**的可执行验收命令，用真实退出码当证据。

## 文件地图

| 路径 | 作用 |
|---|---|
| `skills/theater-detection-audit/SKILL.md` | **新增引擎**（17KB）：7 类 theater 定义、两阶段审计法、生产级补全流程 |
| `skills/theater-detection-audit/theater-detection-audit-process.dot` | 审计流程图 |
| `skills/theater-detection-audit/LICENSE` | MIT 原文，**保留** |
| `skills/workspace-surface-audit/` `skills/automation-audit-ops/` | 盘点与自动化清单（内置） |
| `skills/module-regression/` `skills/change-impact/` | 断链与影响分析（内置） |
| `skills/brownfield-retrospective/` `skills/production-audit/` | 存量差距与上线就绪（内置） |
| `skills/verification-loop/` `skills/delivery-gate/` `skills/gateguard/` | 验证闭环（内置） |
| `commands/cht-doctor.md` | 一键入口 |

## theater 的 7 类模式（扫壳时逐类过）

1. **假数据 / 硬编码响应** — 返回固定对象而非查库/调 API
2. **TODO / FIXME / HACK / XXX / TEMP / STUB** 标记
3. **空实现 / stub 函数** — 空函数体、直接返回默认值、函数体被注释
4. **被注释掉的生产逻辑** — 真实现在注释里，跑了简化版
5. **过度简化的错误处理** — catch 后什么都不做、永远成功
6. **test-mode 条件分支** — 测试与生产走完全不同的简化路径
7. **可疑常量** — 写死的用户 ID / 示例邮箱 / 固定时间戳

## 许可

新增引擎 `theater-detection-audit` 为 **MIT**（DNYoussef），其 `LICENSE` 已随目录带入，勿删。其余 4 组为仓库既有的 ECC（MIT）技能。本仓库主许可仍为 MIT。`NOTICE.md` 已单列该来源。
