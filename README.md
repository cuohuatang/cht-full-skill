# cht-full-skill · V0.0.1

> 把 gstack 的**角色制工程流水线**和 superpowers 的**研发纪律**合成一个 skill。
> 一个想法进来，一个已验证的 PR 出去。

[![version](https://img.shields.io/badge/version-0.0.1-blue.svg)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![skill](https://img.shields.io/badge/format-agent--skill-8A2BE2.svg)](SKILL.md)

---

## 这是什么

一个**单一入口**的研发全流程技能。装上之后，你的 agent 不再是"你说一句它写一段"，而是按一支工程团队的方式工作：

```
Think → Spec → Plan → Build → Review → Test → Ship → Reflect
```

每一阶段都有：明确的角色视角、明确的产出物、明确的**门禁**。不过门禁，不许进下一阶段。

## 为什么要合并

两套方法论各缺一半：

| | gstack | superpowers |
|---|---|---|
| 强项 | 角色分工清楚，每阶段谁负责什么一目了然；审查维度具体（CEO 四档范围、设计七维打分、门禁完整性专查） | 执行纪律硬（没看过的失败测试不算测试、没证据不许说完成、调试必须先根因、裁决不停摆） |
| 弱项 | 依赖 bun 编译的二进制与浏览器包，重；命令 30+ 个，记不住 | 角色视角弱，容易变成"一个人埋头写" |
| 本仓库做法 | 取**骨架与角色** | 取**纪律与执行细则** |

结果：**8 个命令，13 道门禁，0 依赖**。纯 Markdown + POSIX shell。

## 安装

```bash
# 方式一：一键
curl -fsSL https://raw.githubusercontent.com/cuohuatang/cht-full-skill/main/scripts/install.sh | bash

# 方式二：克隆后安装（推荐，可升级）
git clone https://github.com/cuohuatang/cht-full-skill.git ~/.codebuddy/skills/cht-full-skill
bash ~/.codebuddy/skills/cht-full-skill/scripts/install.sh --local

# 装到 Claude Code
bash scripts/install.sh --target ~/.claude/skills

# 校验
bash scripts/verify.sh
```

安装脚本会检查 `frontmatter.name` 是否等于目录名——不一致的 skill 永远不会被识别，这是最常见的手工安装事故。

## 命令

| 命令 | 阶段 | 你什么时候用它 |
|---|---|---|
| `/cht-spec --discover` | Think | "我想做一个……" —— 先被六个问题问一遍 |
| `/cht-spec` | Spec | 需求比较清楚了，落成可验收的 SPEC |
| `/cht-plan` | Plan | 出方案、拆任务、定范围（含"砍掉什么"） |
| `/cht-build` | Build | 按计划逐任务 TDD 实现，中途不打断你 |
| `/cht-review` | Review | 找能过 CI 但炸线上的问题，含门禁降级专查 |
| `/cht-debug` | 任意 | 报错 / 测试挂 / 线上异常 —— 先根因，后修复 |
| `/cht-qa` | Test | 真实环境 QA，或上线前"这句话我能证明吗" |
| `/cht-ship` | Ship | 发版：门禁、灰度、观察、回滚预案 |
| `/cht-status` | 任意 | "现在到哪一步了" |
| `/cht-roles` | 任意 | 八个视角各看一遍 |
| `/cht-retro` | Reflect | 复盘并把判断沉淀下来 |

## 项目里会产生什么

```
docs/cht/
├── SPEC.md          # 范围 / 非目标 / 可判定验收 / 成功度量
├── PLAN.md          # 文件结构 + 任务四要素 + 三张审查表 + 回滚
├── LEDGER.md        # 执行账本：RED/GREEN/RULING/BLOCKED
├── REVIEW.md        # 分级发现（P0-P3 / AUTO-FIXED / ASK）
├── QA-REPORT.md     # 每个 bug 六要素 + 可重放证据
├── RELEASES.md      # 发布记录与观察结果
├── RETRO.md         # 四问复盘
└── LEARNINGS.md     # 跨会话可复用判断（≤30 条）
```

初始化：`bash scripts/new-sprint.sh /path/to/project "特性名"`

## 三条铁律

```
1. 没有 spec 不写计划；没有计划不写代码。
2. 没亲眼看见它失败的测试，不叫测试。
3. 没有本轮新跑出来的验证证据，不许说"完成"。
```

这三条是这个仓库存在的全部理由。其余都是它们的展开。

## 与上游的关系

本仓库是 [garrytan/gstack](https://github.com/garrytan/gstack)（MIT，Garry Tan / YC）与
[obra/superpowers](https://github.com/obra/superpowers)（MIT，Jesse Vincent）的**方法论合并与重写**。

- **不包含**上游代码、bun 编译产物、浏览器二进制、hooks 脚本。
- **包含**两者的方法论结构，重新组织为单一流水线，并改写为中文可执行清单。
- 上游署名与许可全文见 [NOTICE.md](NOTICE.md)。

如果你想要完整的 gstack（含 `/browse`、`/qa` 真实浏览器驱动、`/cso` 安全审计等工具链），直接装上游；本仓库是"轻量、可移植、方法论优先"的路线。

## 许可

MIT，见 [LICENSE](LICENSE)。
