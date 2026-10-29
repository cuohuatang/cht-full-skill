---
name: cht-full-skill
description: 全栈交付方法论（研发全流程技能）。把模糊需求变成已合并、已部署、已验证的生产代码：六问逼出真需求 → 可执行 spec → 计划分解 → TDD 逐任务实现 → 分级代码评审 → 真实环境 QA → 发布门禁。内含 CEO / 产品经理 / 架构师 / 设计师 / 工程师 / 评审 / QA / 发布 八个角色视角，以及并行 worktree 与复盘记忆。Use when 用户要做需求梳理、写规格、出技术方案、拆任务、开发功能、修 bug、做代码评审、QA 测试、发版上线、写 skill，或说"帮我把这个做出来""这个功能怎么做""review 一下""测试一下""上线"。适用于 TDD、子代理开发、调试、重构、多代理并行、遗留代码维护等场景。
version: "0.0.1"
license: MIT
homepage: https://github.com/cuohuatang/cht-full-skill
---

# cht-full-skill · V0.0.1

> 一句话：**它不是工具箱，是一支工程团队的工作流。** 一个想法进来，一个已验证的 PR 出去。

本 skill 把两套业界方法论合成一条流水线：

| 来源 | 提供什么 | 在本 skill 中的位置 |
|---|---|---|
| **gstack**（Garry Tan / YC） | 角色制虚拟工程团队、七阶段冲刺、每阶段的审查与门禁 | 流水线的**骨架**与**角色**（`references/08-roles.md`） |
| **superpowers**（obra） | 需求逼问、计划粒度、TDD、子代理执行、系统化调试、完成前验证 | 流水线的**纪律**与**执行细则**（`references/01`–`06`） |

合并后只有一个入口、一套命令、一份产出物标准。不需要记两套。

---

## 何时加载本 skill

命中任意一条就加载，不要凭感觉直接开写代码：

- 要做新功能、新组件、新服务、新页面，或"帮我实现一个……"
- 需求还很模糊，用户说的是"想要一个能 X 的东西"
- 要出技术方案、拆分任务、评估工期
- 要修 bug、查线上异常、解释"为什么这个测试挂了"
- 要做 code review、上线前检查、发版、部署、写 PR
- 要 QA 测试（网页 / API / CLI / 定时任务 / webhook）
- 要写或改一个 agent skill

---

## 三条铁律（违反任意一条，整条流水线作废）

```
1. 没有 spec 不写计划；没有计划不写代码。
2. 没亲眼看见它失败的测试，不叫测试（RED before GREEN）。
3. 没有本轮新跑出来的验证证据，不许说"完成 / 已修复 / 通过"。
```

第 3 条的具体形式：不许写"应该可以了""理论上没问题""测试都过了"——除非你**刚刚**跑过那条命令，并读完了完整输出（`references/06-qa.md`）。

---

## 流水线

```
Think → Spec → Plan → Build → Review → Test → Ship → Reflect
  ↑                                                        │
  └──────────────── learnings 回写 ─────────────────────────┘
```

| # | 阶段 | 命令 | 主导角色 | 产出物 | 门禁（不过不许进下一阶段） |
|---|---|---|---|---|---|
| 0 | **Think** 逼问 | `/cht-spec --discover` | YC Office Hours | 对话记录 + `SPEC.md` 草稿 | 六个问题里该问的都问完；至少一次"这真是你要的吗"的挑战 |
| 1 | **Spec** 定稿 | `/cht-spec` | 产品经理 | `docs/cht/SPEC.md` | 范围、非目标、验收标准、成功度量四项齐全 |
| 2 | **Plan** 拆解 | `/cht-plan` | 架构师 + 工程经理 | `docs/cht/PLAN.md` | 每个任务含：文件路径、接口签名、验证命令、完成定义 |
| 3 | **Build** 实现 | `/cht-build` | 工程师 | 代码 + 逐任务 ledger | 每个任务都走过 RED→GREEN→提交 |
| 4 | **Review** 评审 | `/cht-review` | 评审工程师 + 设计师 | `docs/cht/REVIEW.md` | 阻断级问题清零；降级门禁（弱化测试/放宽超时）全部点名到人 |
| 5 | **Test** 验证 | `/cht-qa` | QA | `docs/cht/QA-REPORT.md` | 每个 bug 有可重放证据 + 一条失败转通过的回归测试 |
| 6 | **Ship** 发布 | `/cht-ship` | 发布工程师 | PR + 发布记录 | 测试、覆盖率、文档、变更说明四项同步；CI 绿 |
| 7 | **Reflect** 复盘 | `/cht-retro` | 工程经理 | `docs/cht/RETRO.md` + learnings | 至少一条可复用的判断写进项目记忆 |

小任务允许跳阶段，**但跳过的阶段要在回复里明说跳了哪个、为什么**。默认全走。

---

## 路由：用户说了什么 → 走哪一步

| 用户的话 | 进入 | 别做 |
|---|---|---|
| "我想做一个……" / "能不能加个……" | `/cht-spec --discover` — 先逼问，别急着答应 | 不要立刻列出技术方案 |
| "需求是这样的：……（已很具体）" | `/cht-spec` 直接落文档，快速确认后进 Plan | 不要重复追问已知信息 |
| "出个方案 / 怎么实现 / 用什么技术" | `/cht-plan` | 不要顺手把代码写了 |
| "开始做 / 按计划执行" | `/cht-build` | 不要中途反复问"要继续吗" |
| "review 一下 / 看看有没有问题" | `/cht-review` | 不要只夸不挑；不要沉默地全改 |
| "跑不起来 / 报错了 / 测试挂了" | `/cht-debug` — 先定位根因 | **禁止**先猜着改代码 |
| "测试一下 / QA 一下 / 验证下页面" | `/cht-qa` | 不要用"看起来没问题"当结论 |
| "发版 / 提 PR / 上线" | `/cht-ship` | 不要跳过测试跑 PR |
| "现在到哪一步了" | `/cht-status` 读 `docs/cht/` 下的产出 | 不要凭记忆汇报 |

---

## 八个角色（同一件事，八个视角看一遍）

完整职责、输入输出、否决权见 `references/08-roles.md`。速查：

| 角色 | 只关心一件事 | 有否决权的问题 |
|---|---|---|
| **CEO / 创始人** | 这值得做吗？有没有更小的切口？ | 范围失控 → 砍需求 |
| **产品经理** | 验收标准写清楚了吗？ | 验收标准不可测 → 打回 |
| **架构师** | 数据怎么流？边界在哪？失败长什么样？ | 隐藏假设没暴露 → 打回 |
| **设计师** | 这是产品还是 AI 味模板？ | 设计维度低于及格线 → 打回 |
| **工程师** | 每个任务能不能被一个测试证明？ | —（执行方） |
| **评审工程师** | 哪个 bug 能过 CI 但炸线上？ | 阻断级问题 → 阻断合并 |
| **QA** | 真实环境里真的跑通了吗？ | 无可重放证据 → 不算通过 |
| **发布工程师** | 回滚路径是什么？ | 回滚不可行 → 不许发 |

数据分析视角并入 CEO 与 QA：上线前定义度量，上线后看真实数据（`references/07-ship.md`）。

---

## 参考文档索引

按需读取，不要一次性全读：

| 文件 | 内容 | 什么时候读 |
|---|---|---|
| `references/01-discovery.md` | 六问逼需求、假设挑战、方案对比、SPEC 模板 | 阶段 0–1 |
| `references/02-planning.md` | 计划粒度标准、文件结构决策、四档范围模式、三路审查 | 阶段 2 |
| `references/03-execution.md` | TDD 循环、子代理 vs 内联、ledger、裁决规则 | 阶段 3 |
| `references/04-debugging.md` | 根因铁律、四阶段定位、三次失败停手 | 任何 bug |
| `references/05-review.md` | 评审分级、降级门禁识别、接收评审的纪律 | 阶段 4 |
| `references/06-qa.md` | 环境矩阵、复现→回归→修因→复验、完成前验证门 | 阶段 5 |
| `references/07-ship.md` | 发布门禁清单、PR 描述、回滚、金丝雀 | 阶段 6 |
| `references/08-roles.md` | 八角色作战手册 + 角色简报模板 | 需要换视角时 |
| `references/09-parallel.md` | worktree 隔离、并行代理分派、合并纪律 | 多任务并行 |
| `references/10-memory.md` | ledger、learnings、复盘、跨会话记忆 | 阶段 7 / 长任务 |
| `references/11-writing-skills.md` | 用 TDD 写 skill、防臃肿五阶梯 | 写 skill 时 |

产出物模板在 `assets/templates/`：`SPEC.md`、`PLAN.md`、`REVIEW.md`、`QA-REPORT.md`、`RETRO.md`、`LEDGER.md`、`ROLE-BRIEF.md`。

---

## 反模式清单（看到自己这样，立刻停）

| 反模式 | 为什么致命 | 正确做法 |
|---|---|---|
| 需求没问清就开始写 | 写的是你以为的需求，返工成本最高 | 走阶段 0 |
| "我先把代码写出来再补计划" | 计划的作用是暴露决策，不是记录决策 | 先写 `PLAN.md` |
| 一次改十个文件，不跑测试 | 出错时无法定位是哪一处 | 一个任务一次提交一次验证 |
| 测试写完立刻改到绿 | 你不知道它测的对不对 | 先跑出 RED，看它失败在预期原因上 |
| 报错后直接改代码试运气 | 治好症状，留下病根 | `/cht-debug` 四阶段 |
| "应该没问题了" | 没有证据的断言 = 撒谎 | 跑命令，贴输出 |
| 评审意见全部照做 | 包括技术上错的意见 | 先验证，再决定（`references/05`） |
| 每个任务停下来问"要继续吗" | 消耗用户注意力，零信息量 | 连续执行，只在四种情况停 |
| 隐瞒降级（弱化断言、跳过测试、放宽超时） | 门禁形同虚设 | 每一项点名到人 |

---

## 只在四种情况停下来问用户

1. **不可逆操作**：删数据、强推、覆盖远程、清库。
2. **安全敏感**：涉及密钥、权限、对外暴露、生产写操作。
3. **工作区之外的副作用**：合并、推共享分支、发布、发消息、花钱。
4. **计划本身已崩**：往后每条路都是猜的。

其余一律**自己裁决并记录**：

```
Ruling: <决定了什么> — <为什么> — <错了的代价>
```

错误裁决的代价是可见的返工；卡住等回答的代价是用户的一整天（`references/03-execution.md`）。

---

## 快速上手

```bash
# 安装（默认装到 ~/.codebuddy/skills/，可指定 --target ~/.claude/skills）
curl -fsSL https://raw.githubusercontent.com/cuohuatang/cht-full-skill/main/scripts/install.sh | bash

# 或本地安装
git clone https://github.com/cuohuatang/cht-full-skill.git ~/.codebuddy/skills/cht-full-skill
bash ~/.codebuddy/skills/cht-full-skill/scripts/install.sh --local

# 校验
bash ~/.codebuddy/skills/cht-full-skill/scripts/verify.sh
```

典型一次完整冲刺：

```
你     ：我想做一个把会议录音变成行动项的工具
Agent  ：/cht-spec --discover     ← 六个问题，逼到你说出真实场景
Agent  ：/cht-spec                ← SPEC.md，你逐段确认
Agent  ：/cht-plan                ← PLAN.md，8 个任务，每个都能被一个测试证明
Agent  ：/cht-build               ← 逐任务 RED→GREEN→commit，不打断你
Agent  ：/cht-review              ← 2 项自动修，1 项要你拍板（并发竞态）
Agent  ：/cht-qa                  ← 真实浏览器走一遍，抓到 1 个 bug，补回归测试
Agent  ：/cht-ship                ← PR + 发布说明 + 回滚路径
```

---

## 来源与许可

MIT。衍生自两个 MIT 项目，方法论归属原作者：

- [garrytan/gstack](https://github.com/garrytan/gstack) — Garry Tan，YC。角色制工程流水线。
- [obra/superpowers](https://github.com/obra/superpowers) — Jesse Vincent。可组合 skill 的研发方法论。

本仓库为两者的**方法论合并与重写**，不含上游的 bun 编译工具链与浏览器二进制；纯 Markdown + POSIX shell，任何支持 skill 的 agent 都能用。详见 `NOTICE.md`。
