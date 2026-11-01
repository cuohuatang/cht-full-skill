# 参考 15 · diagram-design 可视化技能库（来自 cathrynlavery/diagram-design · MIT）

> 一条铁律：画图前先想清楚“读者看图比看一段话能多懂多少？”——如果不多，就别画，改用表或段落。
> 本库从 [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)（MIT，6.3 万★）**原样嫁接**全部引擎到 `diagram-design/`，版本 `metadata.version: 2.6`。

## 它是什么

一个 **Agent Skill**：你用一句大白话说要什么图，它吐出**一个自包含 HTML 文件（内嵌 SVG）**，双击即可在浏览器看。核心不是“画出来”，而是**审美好、有品牌一致性**。

- **45 种图型**，每种三套变体（极简亮 / 极简暗 / 完整编辑风）
- **编辑式设计系统**：1px 细线、零阴影、坐标吸附 4px 网格、只用 1 个强调色（accent 最多给 1~2 个焦点元素）
- **品牌入驻**：给它一个网址，自动抓配色+字体映射到语义角色（paper/ink/muted/accent/link），之后每张图跟你的站点一致
- **导入重绘**：把已有的 `.drawio` / Mermaid / Excalidraw 按本设计系统重画，并给一份“保真度清单”
- **四旋钮**：Format(html/svg/png) × Size(10 种预设) × Detail(≤24/≤12/≤7 节点) × Audience(工程师/混合/高管)

## 和 archify 怎么选（同是画图，取向相反）

| | **archify**（`archify/`） | **diagram-design**（`diagram-design/`） |
|---|---|---|
| 取向 | **先校验再画**，防“凭空捏造架构” | **先好看再画**，防“AI 敷衍图” |
| 强项 | 结构正确、序列图/数据流贴近真实系统 | 审美、品牌一致性、出版级排版 |
| 图型数 | ~10 种（系统结构向） | 45 种（多了甘特、看板、桑基、象限、Wardley、雷达等商业图） |
| 输出 | 自包含交互式 HTML | 自包含 HTML+SVG，可导图 |
| 一句话 | “别画错” | “画得好看” |

**调用建议**：说“画得专业/好看点、跟我们品牌一致”→ diagram-design；说“别画错、先校验结构”→ archify。

## 怎么调用（三步）

1. 读 `diagram-design/SKILL.md`（主入口，含哲学、反模式、设计系统、复杂度预算、输出清单）。
2. 按 §3 视觉类型表选图型，加载对应的 `diagram-design/references/type-<图型>.md`（**画之前必须加载该类型参考**）。
3. 从 `diagram-design/assets/template.html`（或 `-dark` / `-full`）复制模板，替换 eyebrow/h1/SVG 内容，跑 §9 审美闸门。

> 快捷命令：`/cht-diagram <描述>` —— 例如 `/cht-diagram 给我画一个三层架构图：前端、后端、PostgreSQL、Redis 缓存，深色、16:9 幻灯片尺寸`。

## 关键参考文件（都在 `diagram-design/references/`）

| 文件 | 作用 | 何时读 |
|---|---|---|
| `style-guide.md` | 唯一真源：颜色/字体/语义角色 token、默认调色板 | 每次画前查 `{ink}`/`{accent}` 等占位符的实际色值 |
| `onboarding.md` | 品牌入驻流程（网址/本地设计系统/粘贴 token/保存 profile） | 首次在项目里画图、要做品牌适配时 |
| `profiles.md` | 多客户命名 profile（`.diagram-design` 标记解析） | 多品牌并行项目、复用已存品牌 |
| `semantic-patterns.md` | 行为语义模式（队列瓶颈/阶段框架/安全铺路等） | 当“行为/状态/风险”承载含义时先于图型选 |
| `primitives-core.md` | 通用 SVG 原语 + 6 条强制连线规则 + 无障碍 SVG 契约 | 画箭头/节点、做几何校验时 |
| `primitive-*.md` | 标注/手绘/图标集/终端窗口 四种可选原语 | 需要对应变体时 |
| `output-spec.md` | 四旋钮 + 尺寸预设的 viewBox 与字号梯度 | 设 Format/Size/Detail/Audience 时 |
| `layout-budget.md` | 4px 网格、每类型复杂度预算、汇总卡模式 | 布局超标要拆分、或做卡片时 |
| `animation.md` | 可选动效（reveal/step/loop），静态仍是默认 | 明确要求动效时 |
| `import-*.md` | drawio / mermaid / excalidraw 导入重绘 | 要把已有图重画成统一风格时 |
| `export.md` | 导出 SVG/PNG 的步骤与脚本参数 | 要导出交付物时 |
| `type-*.md`（29 个） | 每种图型的布局语法与类型专属反模式 | 画该图型前必读 |

## 脚本（在 `diagram-design/scripts/`）

| 脚本 | 用途 | 依赖 |
|---|---|---|
| `self_check.py` | 自检：无障碍 SVG 契约、单文件安全、内容在 viewBox 内 | 纯 Python |
| `drawio_extract.py` / `mermaid_extract.py` / `excalidraw_extract.py` | 导入时抽取源图节点/边/容器（输出 digest） | 纯 Python |
| `export_svg.py` | 导出 SVG（只交付 `<svg>` 节点） | 纯 Python |
| `export_png.py` | 导出 PNG（栅格化） | **需 Playwright + Chromium** |
| `verify-geometry.py` / `verify-motion.py` | 几何/动效校验 | 纯 Python（在仓库根 `scripts/`） |

> ⚠️ PNG 导出要装 `playwright` 和 Chromium；只导出 SVG 则无需任何依赖。HTML 本身双击即可看，不依赖任何东西。

## 首次使用的风格闸门

新项目第一次画图前，先开 `references/style-guide.md` 看默认 token 还是出厂值（paper `#f5f5f5` / ink `#2d3142` / accent `#bf4520`）。若是出厂值，会**暂停询问**是否做品牌适配（网址/本地设计系统/粘贴 token/保存 profile），避免把默认皮肤图直接塞进品牌项目。

## 反模式速记（AI 敷衍图的典型特征）

深色模式+青紫辉光 · 用 JetBrains Mono 当通用“开发字体” · 每个节点都画成一样的方块 · 图例飘在图内 · 箭头标签没遮罩矩形 · 竖排文字写在箭头上 · 三个等宽总结卡 · 任何元素带阴影 · 圆角超过 10px · accent 涂满一堆“重要”节点 · 照搬 Mermaid 的自动布局。

## 移植说明

- 全部文件原样保留于 `diagram-design/`，未改写内容；相对路径（`references/`、`assets/`）完好，skill 内部交叉引用不断。
- 示例 HTML（100+ 个 `assets/example-*.html`）为纯展示产物，**未搬运**，以免仓库臃肿；需要看效果可去上游图库 https://cathrynlavery.github.io/diagram-design/ 。
- 上游根目录的构建脚本（`scripts/build-icons.py`、`lint-skin.py`、`fix-mojibake.py`）为开发期工具，未搬运。
