# Changelog

本仓库遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## V0.3.0 — 2026-11-15（已推送 GitHub）

把 **Graphify**（把代码变成图）与 **Semantica**（把图存好、搜得到、查得清来源）**合起来**嫁接入 cht，做成两段式代码图流水线。许可计数由「七份 MIT + 两份 Apache-2.0」更新为「**八份 MIT + 三份 Apache-2.0**」（新增 Graphify Apache-2.0、Semantica MIT）。

**先纠一个前提**：两个上游之间**没有官方集成**——核查 `Graphify-Labs/graphify` 仓库内全部 `semantica` 命中，均为 `semantically_similar_to`（语义相似边）的子串，不是项目引用。下面的衔接契约是 **cht 定义的**，不是任何一方官方行为，已全程诚实标注。

- **嫁法定性（沿用 `本周涨星Top项目-嫁接方案.md` 方案 3 的纪律）**：两者都是重运行时引擎——Graphify 需 Python 3.10+ / uv / `graphifyy`（双 y）/ tree-sitter，Semantica 需 Python 包 + RDF/LPG 图存储（生产还要 Docker/K8s）——与「纯 Markdown + 0 第三方依赖」硬冲突，**引擎一律不捆绑**。cht 只嫁纯文本契约、环境检测、格式桥接与命令编排
- **嫁入 9 个上游文件（原样未改，sha256 逐一比对一致）**：`skills/graphify/`（**Apache-2.0**，`extraction-spec.md` / `query.md` / `how-it-works.md` + `LICENSE` + `NOTICE` + `LICENSE-MIT`）、`skills/semantica/`（**MIT**，`SKILL.md` + `references/glossary.md` + `LICENSE`）
- **未嫁**：Graphify Python 引擎 / `worked/` 样例 / 其余 14 个宿主 skill 变体；Semantica Python 包、`provenance.md`(35KB) 与 `decision-intelligence.md`(32KB)——满是引擎调用代码，整包塞进纯 Markdown 仓库只会制造无效指令，核心方法论改为本仓库**原创重述并署名**
- **新增 `references/26-code-graph-pipeline.md`**：两段式流水线、**实测** `graph.json` 结构、三态 → W3C PROV-O 映射契约、硬门槛与降级、与 cht 各机制边界、8 条红牌
- **新增 `scripts/graph_bridge.py`**（Python **标准库**、0 第三方依赖，不 import 两个引擎）：`--env` 只检测不安装 / `--plan` 四段命令 / `--verify` 结构校验 / `--bridge` 生成 `lineage.json` / `--selftest` **19 例**回归
- **衔接契约**：`EXTRACTED` → `prov:wasDerivedFrom`（`source_file#source_location`）直接入图；`INFERRED` → `prov:wasGeneratedBy` 入图但保留置信档；`AMBIGUOUS` / 非法标签 → **只进复核队列，绝不混入正式图**（与 security-audit 的 `needs_validation` 纪律同源）
- **用上游真实数据校准过两次**：① 真实 `graph.json` 是 NetworkX node-link、键名 **`links` 不是 `edges`**（脚本两者兼容）；② `httpx` 样例 330 边中 **156 条 INFERRED 不带 `confidence_score`**——`extraction-spec.md` 的 REQUIRED 只约束 LLM 抽取子 Agent，**AST 代码路径不带**。故 `--verify` 降级为警告而非阻断，桥接保持 `null`、标 `inferred_unscored`，**绝不猜一个 0.5**。两份真实样例 `worked/httpx`(144 节点/330 边) 与 `worked/mixed-corpus`(22/38) 验证均 `ok=true`
- **新增 `commands/cht-graph.md`**：六态入口（默认 status / pipeline / build / bridge / store / query）；未装引擎时只给方法论与安装指引，不假装已建图
- 同步主 `SKILL.md`（加载条件、路由、参考索引 26、来源与许可）、README（命令数 21 → **22**、来源表、许可段）、`NOTICE.md`（新增第 11/12 节、许可计数、引用建议）、`VERSION` 及 frontmatter 至 `0.3.0`

> 注：`lineage.json` 是**中间格式**，不是已入库的图；真正落库仍需按映射在 Semantica 摄入侧写适配代码。`--verify` 输出与桥接产物**都不是验证证据**，不得据此宣称「图已入库且查得清」（三条铁律）。

## V0.2.0 — 2026-11-15（已推送 GitHub）

嫁接**提示词架构师**为**阶段 -1 前置闸门**（方法论由本仓库用户提供，经结构化整理与可执行化；**非第三方开源，不引入新许可**，许可计数仍为七份 MIT + 两份 Apache-2.0）。

> 为什么是 0.2.0 而不是 0.1.1：V0.1.0 已声明功能集冻结，本次是**解冻 + 新增入口关卡**，且改变了所有任务型输入的入口行为，属功能性变更，按 minor 递进。

**核心不是「怎么优化」，是「先判断该不该优化」**——用户明确要求「一定要区分不是所有提示词都优化，有些是禁止优化的」。

- **裁决主轴：规格完整度**：输入本身是否已构成完整可执行规格。是 → 原样透传；否 → 优化；拿不准 → 默认透传（漏优化只是多说一句，过度优化是擅自改写意图）
- **禁止优化硬闸门（6 条）**：R0 一票否决（用户说别改 / 只判断）、R1 寒暄致谢、R2 纯事实问答·翻译·摘要、R3 延续性修改、R4 已点名技能或文件、R9 灰区默认透传
- **任务型才优化**：下任务 / 归纳总结 / 生成 / 安装 / 修复 / 转换 / 推送 / 产出文件等重要任务
- **灰区裁决写死**：「摘要」≠「归纳总结」——单步转换不优化，带分析 / 结论 / 方案 / 交付物 / 多来源就优化；寒暄或延续里夹带新任务动词则升级为优化
- **新增 `scripts/prompt_gate.sh`**：POSIX sh、0 依赖、`LC_ALL=C`，输出 `PASS_THROUGH` / `OPTIMIZE` / `AMBIGUOUS`，`--why` 给命中规则，`--selftest` 内置 **26 例**回归（禁止类 13 / 任务类 11 / 灰区 2，含 1 例中文子串陷阱）。把「禁止优化」从口号变成能跑、能回归的规则
- **新增 `references/25-prompt-architect.md`**：四步优化规范（补隐性需求 / 双版本 / 结构化 / 全 Agent 适配）、双版本模板、ChatGPT·Claude Code·豆包·DeepSeek·harness·Kimi 适配矩阵、10 条「规避逻辑漏洞与无效指令」自检、与 cht 各机制的边界、8 条红牌
- **新增 `commands/cht-prompt.md`**：`/cht-prompt` 四态入口（默认双版本 / `--check` 只判断 / `--lite` / `--full`）；**透传时零改写、零解释**，连「无需优化」都不写
- **边界划死**：只补表达层不补业务层（受 `grill-me` 约束，防擅自加功能）；本关**不追问、不代替阶段 0 六问**；与 `caveman` 一个管输入一个管输出；**三条铁律优先**，优化后的提示词不得要求跳过验证；数字 / 路径 / 报错串 / 否定词逐字保留
- 主 `SKILL.md` 新增「前置关卡：提示词优化（阶段 -1）」段、加载条件、路由行、参考索引 25、来源说明；README 命令表加 `/cht-prompt`、命令数 20 → 21；NOTICE「本仓库新增的部分」增列该项；`VERSION` 及 frontmatter 同步至 `0.2.0`
- `scripts/verify.sh` 未改动；闸门自测独立可跑，不侵入安装体检

> 注：闸门是确定性预检，最终裁决仍由宿主结合上下文做出；判 `AMBIGUOUS` 一律按透传处理，不硬凑优化版本。

## V0.1.0 — 2026-11-15（已推送 GitHub）

**首个稳定里程碑**：`0.0.x` 的密集嫁接期收口，功能集冻结为「20 个命令 + 13 道门禁 + 0 运行时依赖」的完整流水线。**本版不新增功能、不新增技能文件**，只做版本跃迁与文档一致性整理。

- **版本跃迁**：`VERSION`、`SKILL.md`（frontmatter + 标题）、`README.md`（标题 + badge）同步至 `0.1.0`
- **CHANGELOG 时态统一**：V0.0.7 ~ V0.0.10 四条标题的状态标记统一为「（已推送 GitHub）」，与 V0.0.4 ~ V0.0.6 的历史写法一致——这四个版本当时均已成功推送并打 tag，旧措辞属发布后未回收的残留
- **历史陈述一律保留**：各命令卡 `version` 仍是其**引入版本**（如 `cht-caveman` 保持 `0.0.10`）、`SKILL.md` 的「V0.0.10 新增」标注、各版本条目里「同步至 0.0.x」的原话，均不改写；`v0.0.10` 及更早的 tag **一律不重建**
- 许可结构不变：**七份 MIT + 两份 Apache-2.0** + 一处署名影响（ub-mode）；未新增第三方代码，故 `NOTICE.md` 无改动

> 注：语义化版本下 `0.0.x → 0.1.0` 表示从初始开发进入首个可稳定引用的里程碑，但 `0.x` 整体仍不承诺向后兼容；命令名、目录结构在后续版本仍可能调整。

## V0.0.10 — 2026-11-15（已推送 GitHub）

嫁接 **caveman** 会话输出压缩技能（[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) v4.1.0，**Julius Brussee，Apache-2.0**，约 12 万★）。

**先纠两个误传**：① 网传"省 65% token"来自它的 proxy/engine 压缩层，**不是这个 skill**——官方 skill 实测默认档仅 **3%**（在噪声内）、ultracave 35%、megacave 9%，且无质量等价声明；② 3.0.0 起全仓库**已从 MIT 转 Apache-2.0**，故按 Apache-2.0 处理（保留 LICENSE + 上游 NOTICE）。

- **整包嫁接三档纯文本技能**：`skills/caveman/`（SKILL.md 4.7KB 九条规则 + README + **LICENSE Apache-2.0** + **上游 NOTICE** + `LICENSE-MIT` 历史文本）、`skills/ultracave/SKILL.md`、`skills/megacave/SKILL.md`。三个 SKILL.md **原样未改**
- 新增 `references/24-caveman.md`：三档对照、九条规则、7 条破例、**与三条铁律的冲突边界**、实测数据澄清、默认关闭策略、商标说明
- 新增 `commands/cht-caveman.md`：三档切换 / status / stop 入口
- **⚠️ 核心冲突已划死**：caveman 压缩会话输出，cht 第 3 条铁律要求"跑命令、贴完整输出"。**冲突时铁律优先**——只压缩会话旁白；命令完整输出 / 测试日志 / 报错栈 / 验证证据 / `docs/cht/` 全部产出物 / 代码 / commit / PR **一律正常散文、一字不动**（这正是上游 7 条「When to break the rules」+ 规则 6 的要求，cht 显式化提高优先级）
- **默认关闭、显式开启**：上游"加载即常驻"会污染产出物标准，cht 里必须 `/cht-caveman` 才开启
- **未嫁运行时**：Node `activation-rule.mjs`、60KB Python 压缩引擎、proxy/engine/browse/mcp、Docker、CI 全不搬——只取纯文本规则，守住 0 运行时依赖
- 主 `SKILL.md` 新增"会话输出压缩"段、参考索引加 24、加载条件加 caveman、来源加为**第二套 Apache-2.0**；README / NOTICE / VERSION 同步至 0.0.10

> 注：商标 "Caveman" 及 logo 为上游商标，Apache-2.0 不授予商标权；本仓库仅作署名性引用，不暗示背书或赞助。

## V0.0.9 — 2026-11-09（已推送 GitHub）

嫁接 **T0 系统检测/自修复技能组**，把上一轮给用户推荐的 5 组能力编排成 cht-full-skill 的统一入口，专治"已开发到 90%、逻辑乱、全插件化的系统"——查不合理逻辑 / 没连通 / 空壳 + 分级自修复。

**诚实标注**：5 组里 **4 组本就在本仓库**（V0.0.3 从 ECC 嫁入的 234 技能自带），本次是**编排**而非复制；真正新增文件只有 1 个 MIT 引擎。

- **新增引擎**：整包嫁入 `skills/theater-detection-audit/`（[DNYoussef/ai-chrome-extension](https://github.com/DNYoussef/ai-chrome-extension/tree/main/.claude/skills/theater-detection-audit)，**MIT**）——`SKILL.md`(17KB，7 类 theater 定义) + `theater-detection-audit-process.dot` + `LICENSE`(MIT，保留)。专治"哪些是壳"：mock / stub / TODO / 被注释掉的真逻辑 / 假错误处理
- **新增** `references/23-system-doctor.md`：四类问题映射、七步闭环、P0/P1/P2 分级、四层验证门、插件化系统特殊注意点（空实现常是故意的扩展点、事件总线会被误报成断链）
- **新增** `commands/cht-doctor.md`：统一入口，编排 `workspace-surface-audit` + `automation-audit-ops`（盘点）、`module-regression` + `change-impact`（断链）、`brownfield-retrospective` + `production-audit`（逻辑）、`verification-loop` + `delivery-gate` / `gateguard`（验证）
- 主 `SKILL.md` 新增"系统体检与自修复"段、参考索引加 23、加载条件加"全面检测/查壳/查断链"、来源加 DNYoussef 为**第七套 MIT**；命令用 `/cht-doctor`（`/cht-audit` 已被安全审计占用）
- README / NOTICE / VERSION 同步至 0.0.9；上游计数由"六套 MIT"更新为"七套 MIT"

> 注：未嫁 Codebase Health Auditor / Millie Fix / heal-skill 三个外部技能——来自聚合站、仓库级许可未声明，按 ub-mode 一贯纪律只留外链指针、不复制文件；`heal-skill` 修的是 skill 库自身而非业务代码。自动修复只覆盖 P0，P1 逐条给 diff 确认，报价/金额类逻辑不闷头全量自动改。

## V0.0.8 — 2026-11-03（已推送 GitHub）

嫁接 **security-audit** 对抗式安全审计技能（[cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)，**Cloudflare, Inc.，MIT**，约 5.7 万★）。**这是补全"本周涨星 Top5"方案里第一优先项，与 V0.0.7 的 skill-creator 形成"造技能 → 审安全 → 才发布"闭环。**

- **整包嫁接**其技能到 `skills/security-audit/`：`SKILL.md`(22KB) + `RECONNAISSANCE.md` + `HUNTING.md`(22KB) + `VALIDATION-AND-REPORTING.md`(17KB) + `ATTACK-CLASSES.md`(15KB) + **10 个领域伴侣**（Web/认证、客户端、云与部署、数据隔离、桌面/移动/IPC、内存安全、协议/RPC、资源耗尽、供应链、AI/LLM）+ `report-schema.json`(14KB) + 两个**零依赖** `.cjs` 校验器（仅 Node 内置 `fs`/`path`/`util`，各 28KB/33KB）+ `LICENSE`(Cloudflare MIT，**保留**)
- 新增 `references/19-security-audit.md`（引擎说明、六阶段、verdict 语义、文件地图、三大硬门槛、与发布门禁衔接、许可）
- 新增 `commands/cht-audit.md`（全量审计 / 聚焦 review / 只查方法论 三态入口）
- 主 `SKILL.md` 新增"安全审计"段、参考索引加 19、加载条件加 audit、来源加 security-audit 为**第六套（MIT）**
- README / NOTICE / VERSION 同步至 0.0.8；上游计数由"五套 MIT"更新为"六套 MIT"

> 注：三个硬门槛已在文档诚实标注——① 多 Agent 编排依赖宿主能否派子 Agent，不支持则降级单 Agent 手动走六阶段；② 要拿 `confirmed` 必须 OS 强制沙箱跑目标代码，无沙箱则证据停在 `needs_validation`，绝不假装能确认漏洞；③ 两个校验器借 Node ≥ 18 运行，不破坏"0 运行时依赖"底盘。

## V0.0.7 — 2026-11-03（已推送 GitHub）

嫁接 **skill-creator** 造技能引擎（[anthropics/skills → skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)，**Anthropic PBC，Apache-2.0**，约 18.7 万★）。**这是补全上次"本周涨星 Top5"遗漏的第 3 项**。

- **完整嫁接**其引擎到 `skills/skill-creator/`：`SKILL.md`(33KB 方法论) + `references/schemas.md` + `scripts/`(打包/校验/评测) + `agents/`(评分/对比/归因) + `eval-viewer/`(评审页) + `LICENSE.txt`(Apache-2.0，**保留**)
- 新增 `references/22-skill-creator.md`（引擎说明、文件地图、宿主相关坑：描述调优依赖 `claude -p`、并行评测依赖子 Agent）
- 新增 `commands/cht-make-skill.md`（造技能一键入口）
- 主 `SKILL.md` 新增"造技能引擎"段、参考索引加 22、加载条件加"造技能"、来源加 skill-creator 为**第六套（首个 Apache-2.0）**
- README / NOTICE / VERSION 同步至 0.0.7
- **许可处理**：本仓库主许可仍为 MIT，但 `skills/skill-creator/` 为 Apache-2.0——保留其 `LICENSE.txt`、改文件须标注、再分发须附许可证；NOTICE 单列该来源

> 注：skill-creator 的并行评测 / 盲测 A/B 需要宿主能派子 Agent，描述调优（`improve_description.py`）依赖 `claude -p`（Claude Code 专属）；其他宿主降级使用，已在文档中诚实标注。

## V0.0.6 — 2026-11-02（已推送 GitHub）

吸收 **ub-mode** 的工程纪律（[unclebob/ub-mode](https://github.com/unclebob/ub-mode)，★★★★ 6.4k，Robert C. Martin / "Uncle Bob"）。**关键合规决定：ub-mode 未声明许可证、默认版权所有，本仓库不复制其文件，改为原创重述并署名致敬**；同伴门禁工具（crapper/dryer/mutator，0BSD）仅作外链指针，不在仓库内分发。

- 本次只补 cht-full-skill **真正缺的两块**：① 三道**量化质量门**（CRAP<10 / 重复度<0.8 / 变异测试 0 存活）作为推荐基线；② **攻击前提**式根因排查法。三段式（Work→Right→Practice）、TDD、留痕提交等与既有 gstack/superpowers 纪律不重复造轮子。
- 新增 `references/18-engineering-discipline.md`（三段式 + 量化门 + 与三条铁律关系 + 反模式；开头明示灵感来源与"未复制原文"）
- 新增 `commands/cht-ub.md`（工程纪律一键入口）
- `references/06-qa.md` 新增 §5.1「可选量化质量门」作为收尾基线
- 主 `SKILL.md` 新增"工程纪律"段、参考索引加 18、加载条件加 ub、来源加 ub-mode 为**署名影响**（非 MIT）
- README / NOTICE / VERSION 同步至 0.0.6

> 注：若未来要"原样内置" ub-mode，需向 Uncle Bob 申请许可或等其补 license；在此之前一律走"重述 + 署名"路线，避免污染 MIT 合规底盘。

## V0.0.5 — 2026-11-01（已推送 GitHub）

嫁接 **grill-me + grilling** 决策护栏（[mattpocock/skills](https://github.com/mattpocock/skills)，MIT），专门治"AI 稀里糊涂就下决定、擅自改东西"。

- 完整嫁接 `skills/grill-me/`（入口 SKILL.md + `agents/openai.yaml` + `docs.md`）与 `skills/grilling/`（盘问引擎 SKILL.md + `agents/openai.yaml`）；`grill-me` 内部 `Call the Skill tool with "grilling"`，两者同装才可用
- `grill-me` 上游设 `disable-model-invocation: true`：agent 不会自己偷偷调用，必须由用户或流程显式触发——把"擅自做主"关进笼子
- 新增 `references/16-grill-me.md`（引擎说明、grilling 访谈协议、与三条铁律的关系、反模式对照）
- 新增 `commands/cht-grill.md`（动手前连续盘问、逼出共识的一键入口）
- 主 `SKILL.md` 新增"决策护栏"段、参考索引加 16、加载条件加 grill、来源加 grill-me 为第五套；NOTICE / README 同步

> 注：`grilling` 是真正的"盘问"逻辑（设计树 + frontier + 轮次访谈），`grill-me` 是它的用户触发入口。单装 `grill-me` 会变成死链，故二者一并嫁入。

## V0.0.4 — 2026-11-01（已推送 GitHub）

嫁接 **diagram-design** 编辑式品牌可视化引擎（[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)，MIT，6.3 万★），与 archify 形成"结构正确 vs 审美品牌"双引擎。

- 完整嫁接引擎到 `diagram-design/`：`SKILL.md`(v2.6) + `references/`(43 篇：style-guide / onboarding / profiles / semantic-patterns / primitives-core + 4 原语 / output-spec / layout-budget / animation / 3 个 import / export / 29 个图型 type-*) + `assets/` 模板(浅/深/完整/终端) + `scripts/`(self_check / 3 个抽取 / export_svg / export_png / verify-geometry / verify-motion)
- 新增 `references/15-diagram-design.md`（引擎说明、与 archify 分工、文件地图、反模式速记）
- 新增 `commands/cht-diagram.md`（一句话入口，四旋钮、品牌入驻、导入/导出路由）
- 主 `SKILL.md` 新增"可视化引擎库"段、参考索引加 15、来源加 diagram-design 为第四套；NOTICE 同步

> 注：diagram-design 的 100+ 个示例 HTML（纯展示）与开发期构建脚本未搬运，避免臃肿；要看效果去上游图库 https://cathrynlavery.github.io/diagram-design/ 。

## V0.0.3 — 2026-11-01（未发布，本地已就绪）
按用户要求，从 [affaan-m/ECC](https://github.com/affaan-m/ECC)（MIT，29 万★）**按"程序 / 代码开发 / IT 技术"筛出全部相关技能嫁接**，共 **234 个**（剔除医疗、金融、法律、科研、创意媒体、物流制造等非技术领域的约 80 个）。

### 嫁接 · 代码/IT 技能（234 个，8 大类）

- **语言·运行时（36）**：python / rust / golang / typescript / java / kotlin / swift / csharp / cpp / perl / dart / flutter / fsharp / nodejs / bun / dotnet 等
- **前端·移动（19）**：react / vue / angular / nextjs / nuxt / vite / swiftui / android / ios / compose-multiplatform / react-native 等
- **后端·框架（22）**：django / fastapi / nestjs / laravel / rails / springboot / quarkus / api-* / backend / hexagonal 等
- **数据库·ORM（8）**：postgres / mysql / clickhouse / redis / prisma / jpa / mybatis / database-migrations
- **基础设施·运维（19）**：docker / kubernetes / deployment / homelab-* / cisco-ios / netmiko / network-* / canary / flox 等
- **AI·智能体·ML（51）**：agent-* / mcp-server-patterns / llm-* / pytorch / recsys / deepseek / unified-memory 等
- **测试·质量·安全（23）**：tdd-workflow / e2e-testing / security-review / security-scan / codehealth-mcp / production-audit 等
- **工程实践·流程（56）**：api-design / git-workflow / architecture-decision-records / contract-first / coding-standards / error-handling / deep-research 等

### 新增

- `references/14-ecc-code-skills.md`：234 个技能完整分类目录（8 大类，每条带一句话说明）
- `commands/cht-ecc.md`：按关键词检索并路由到对应 ECC 技能的命令
- 主 `SKILL.md` "嫁接技能库"段重写，指向完整目录；版本升至 0.0.3

## V0.0.2 — 2026-10-30（未发布，本地已就绪）

从 [affaan-m/ECC](https://github.com/affaan-m/ECC)（MIT，29 万★）**精选 18 个最通用技能嫁接**，不搬其余 290+ 细分领域技能，避免上下文膨胀。

### 嫁接 · 数据库 / SQL 族（重点做全）

- `postgres-patterns`、`mysql-patterns`、`database-migrations`、`prisma-patterns`、
  `mybatis-patterns`、`jpa-patterns`、`clickhouse-io`

### 嫁接 · 通用工程族

- `tdd-workflow`、`api-design`、`backend-patterns`、`security-review`、`coding-standards`、
  `error-handling`、`architecture-decision-records`、`git-workflow`、`contract-first`、
  `mcp-server-patterns`、`deep-research`

### 新增桥梁

- `references/13-sql-db.md`：SQL/数据库总路由与方言→技能决策矩阵
- `commands/cht-sql.md`：数据库/SQL 一键入口命令
- `SKILL.md` 新增「嫁接技能库」段，列出 18 个技能路径与适用场景
- `NOTICE.md` 补 ECC 来源与未采用说明

### 设计决定

- **为什么只挑 18 个**：ECC 300+ 技能中大量是医疗/金融/homelab/小众语言框架，对通用开发无意义。
  只搬跨项目通用的数据库与工程实践，并把数据库族整族搬入以打通交叉引用。
- **为什么原样保留**：ECC 技能自带 `metadata.origin: ECC`，本仓库不改写其内容，仅做路由与决策包装。

## V0.0.1 — 2026-10-29

首个公开发布。合并 **gstack** 的角色制工程流水线与 **superpowers** 的研发纪律，重写为单一入口的轻量 skill。

### 新增

- `SKILL.md` 主入口：八阶段流水线、八阶段路由表、三条铁律、八角色速查、反模式总表
- 11 份参考文档（`references/`）：需求逼问、计划与三路审查、TDD 执行、系统化调试、代码评审、
  QA 与验证门、发布、八角色作战手册、并行与 worktree、记忆与复盘、用 TDD 写 skill
- 11 个命令卡（`commands/`）：`/cht-spec` `/cht-plan` `/cht-build` `/cht-review` `/cht-debug`
  `/cht-qa` `/cht-ship` `/cht-status` `/cht-roles` `/cht-retro`
- 7 份产出物模板（`assets/templates/`）：SPEC / PLAN / REVIEW / QA-REPORT / LEDGER / RETRO / ROLE-BRIEF
- 3 个脚本（`scripts/`）：`install.sh`（含 name 一致性校验与旧版备份）、`verify.sh`（安装体检）、
  `new-sprint.sh`（在项目内初始化 `docs/cht/`）

### 设计决定

- **为什么合并而不是二选一**：gstack 强在分工与审查维度，弱在依赖重、命令多；superpowers 强在执行纪律，
  弱在角色视角。合并后是 8 个命令、0 依赖、13 道门禁。
- **为什么不打包上游代码**：上游依赖 bun 编译产物与浏览器包，会锁死运行时。本仓库只取方法论，保证任何
  支持 skill 的 agent 都能直接用。
- **为什么用 `docs/cht/` 承载产出**：让计划、账本、评审、QA、复盘成为仓库资产，而不是会话里的临时文本。
  会话会结束，文件不会。
- **为什么强调"门禁完整性"**：弱化断言、跳过测试、放宽超时是 agent 最常见也最隐蔽的作弊方式。
  单独设一节专查，并强制点名到人。

### 已知限制

- 不含真实浏览器驱动（`/cht-qa` 依赖 agent 自身具备的浏览器能力）
- 不含安全扫描容器（安全以评审清单形式内置在 `/cht-review --security`）
- 不做跨项目指标聚合（`/cht-retro` 只复盘单项目；多项目可自行汇总 `RETRO.md`）
