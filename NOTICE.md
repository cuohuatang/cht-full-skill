# NOTICE · 来源与衍生说明

本仓库（`cht-full-skill`）是两份 MIT 许可方法论作品的**合并与重写**。此处说明来源、
保留了什么、去掉了什么，以及为什么。

## 上游

### 1. gstack

- 仓库：https://github.com/garrytan/gstack
- 作者：Garry Tan（Y Combinator 总裁兼 CEO）
- 许可：MIT
- 定位：把编码 agent 变成一支虚拟工程团队（CEO / 工程经理 / 设计师 / 评审 / QA / 安全官 / 发布工程师），
  以 slash 命令组织的完整冲刺。

**本仓库采用的部分**

| 采用 | 落在哪 |
|---|---|
| 冲刺阶段划分 `Think → Plan → Build → Review → Test → Ship → Reflect` | `SKILL.md` 流水线表 |
| 角色制视角与"每个角色只问一个问题 + 否决权" | `references/08-roles.md` |
| 四档范围模式（扩张 / 选择性扩张 / 维持 / 收缩） | `references/02-planning.md §3` |
| 设计七维度打分与 AI 味检测 | `references/02-planning.md §4.2` |
| 门禁完整性专查（弱化断言 / 跳过测试 / 放宽超时点名到人） | `references/05-review.md §2.5` |
| 六问产品诊断（Q1 需求真实性 … Q6 未来契合） | `references/01-discovery.md §2` |
| QA 的真实环境矩阵（网页 / API / CLI / 任务 / webhook） | `references/06-qa.md §2` |
| 发布金丝雀观察阈值与"倾向回滚"原则 | `references/07-ship.md §5` |

**未采用的部分**

- bun 编译的二进制工具链（`browse`、`design`、`pdf`、各 `gstack-*` CLI）
- 浏览器捆绑包、Aside 集成、Cookie 导入、反爬 stealth
- hooks、telemetry、auto-update、team mode、工作状态目录
- `/cso` 的运行时扫描容器、iOS QA 的 StateServer

原因：这些依赖特定运行时与原生工具链，会破坏本仓库"纯 Markdown + POSIX shell、任何 agent 可用"的目标。

### 2. superpowers

- 仓库：https://github.com/obra/superpowers
- 作者：Jesse Vincent（obra）
- 许可：MIT
- 定位：一套可组合的 skill 研发方法论 —— 先逼出规格，再写计划，再 TDD 执行，最后验证。

**本仓库采用的部分**

| 采用 | 落在哪 |
|---|---|
| 需求逼问与"先摆方案再写文档"的流程 | `references/01-discovery.md §1、§4、§5` |
| 计划的任务粒度标准（文件 / 接口 / 验证 / 完成定义） | `references/02-planning.md §1` |
| TDD 的 RED-GREEN-REFACTOR 与"必须看见它失败" | `references/03-execution.md §1` |
| 子代理驱动 vs 内联执行的取舍 | `references/03-execution.md §2` |
| 执行账本（ledger）与"裁决而非停摆" | `references/03-execution.md §4、§5` |
| 系统化调试四阶段与"三次失败停手" | `references/04-debugging.md` |
| 完成前验证门（Iron Gate） | `references/06-qa.md §1` |
| 代码评审的收发纪律 | `references/05-review.md §4` |
| worktree 隔离与并行代理分派 | `references/09-parallel.md` |
| 用 TDD 写 skill、防臃肿五阶梯 | `references/11-writing-skills.md` |

**未采用的部分**

- 各 runtime 的安装脚本与 marketplace 配置
- 视觉伴侣（visual companion）与其 telemetry
- 上游 skill 之间的 `superpowers:` 命名空间引用（本仓库改为单文件内索引，避免跨 skill 依赖）

## 本仓库新增的部分

以下内容不属于任何上游，为本仓库原创整理：

- 八阶段 → 八命令的统一路由表（`SKILL.md`「路由」）
- 13 道门禁清单（`references/07-ship.md §1`）
- 三种产出物分层的记忆模型（Ledger / Learnings / Retro，`references/10-memory.md`）
- 反模式总表（`SKILL.md` 末尾）
- 全部 shell 脚本（`scripts/`）与产出物模板（`assets/templates/`）
- 中文重写与"可执行清单化"改写

## 许可合规

两份上游均为 MIT。MIT 要求保留版权声明与许可声明，本仓库在 `LICENSE` 文件末尾
完整保留了两份原始版权声明。衍生作品同样以 MIT 发布。

如果上游作者认为此处署名或引用方式需要调整，请开 issue，会立即修改。

## 引用建议

```
cht-full-skill (MIT) — 方法论合并自 garrytan/gstack 与 obra/superpowers
https://github.com/cuohuatang/cht-full-skill
```
