# cht-full-skill · V0.0.6

> 把 gstack 的**角色制工程流水线**、superpowers 的**研发纪律**，以及 archify、ECC（234 个代码/IT 技能）、diagram-design（45 种品牌图型）**合成一个 skill**。
> 一个想法进来，一个已验证的 PR 出去；要画图、要查技术栈、要品牌级配图，一个仓库全包。

[![version](https://img.shields.io/badge/version-0.0.6-blue.svg)](VERSION)
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

结果：**16 个命令 + 234 个代码/IT 技能 + 双绘图引擎（archify / diagram-design）+ grill 决策护栏 + ub-mode 工程纪律基线，13 道门禁，0 运行时依赖**。纯 Markdown + POSIX shell。

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
| `/cht-sql` | 数据库 | "给 orders 加 user_id 索引，零停机" —— SQL/ORM 一键路由 |
| `/cht-ecc <技术>` | 检索 | "用 React 怎么做""给 K8s 加个 deployment" —— 在 234 个代码/IT 技能里找 |
| `/cht-arch` | 画图 | 画**结构正确**的架构/序列/ER/数据流图（archify，先校验再画） |
| `/cht-diagram` | 画图 | 画**品牌级、好看**的架构/流程/甘特/象限/雷达图（diagram-design，45 种） |
| `/cht-grill` | 决策护栏 | "grill me / 先确认再动手"——动手前连续盘问、逼出共识，防 AI 擅自做主（grill-me / grilling） |
| `/cht-ub` | 工程纪律 | "工程纪律 / 量化门禁 / ub-mode"——三段式工作法 + 量化质量门（CRAP<10 / 重复度<0.8 / 变异 0 存活），受 Uncle Bob 的 ub-mode 启发（原创重述） |

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

本仓库是五套 MIT 项目的**方法论合并、嫁接与重写**（外加一处署名影响 ub-mode，见上表），署名与许可全文见 [NOTICE.md](NOTICE.md)：

| 来源 | 作用 | 在本仓库的位置 |
|---|---|---|
| [garrytan/gstack](https://github.com/garrytan/gstack)（MIT） | 角色制工程流水线 | 流水线骨架与八角色 |
| [obra/superpowers](https://github.com/obra/superpowers)（MIT） | 研发纪律与执行细则 | 门禁、TDD、调试、完成前验证 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC)（MIT，29 万★） | 代理工具链增强框架 | 按"代码/IT"筛出 **234 个技能**嫁接入 `skills/`，`/cht-ecc` 检索 |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)（MIT，6.3 万★） | 编辑式品牌可视化 | 完整引擎嫁接入 `diagram-design/`，`/cht-diagram` 入口 |
| [mattpocock/skills](https://github.com/mattpocock/skills)（MIT） | 决策护栏（grill-me / grilling） | 嫁接入 `skills/grill-me` + `skills/grilling`，`/cht-grill` 入口，防 AI 擅自做主 |

**影响来源（非 MIT，未获再分发授权，仅作方法引用）**：[unclebob/ub-mode](https://github.com/unclebob/ub-mode)（★★★★ 6.4k，未声明许可证）——其"三段式工作法 + 量化质量门"启发了 `references/18-engineering-discipline.md` 与 `/cht-ub`，内容为**原创重述并署名**，未复制其文件；门禁工具 crapper/dryer/mutator（0BSD）仅作外链指针。

- **不包含**上游代码、bun 编译产物、浏览器二进制、hooks 脚本、ECC 非技术领域技能、diagram-design 示例 HTML 与开发期构建脚本。
- **包含**四套的方法论结构，重新组织为单一流水线，并改写为中文可执行清单。

如果你想要完整的 gstack（含 `/browse`、`/qa` 真实浏览器驱动、`/cso` 安全审计等工具链），直接装上游；本仓库是"轻量、可移植、方法论优先"的路线。

## 许可

MIT，见 [LICENSE](LICENSE)。
