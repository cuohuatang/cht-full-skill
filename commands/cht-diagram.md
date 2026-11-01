---
name: cht-diagram
description: 用 diagram-design 引擎（cathrynlavery/diagram-design，MIT，45 种图型，编辑式品牌风格）画出版级、自包含 HTML+SVG 图。当用户要“画图/做架构图/画个流程图/时序图/甘特图/象限图/重画 Mermaid/drawio/excalidraw/导出 PNG 或 SVG/统一品牌配图”时使用。
---

# /cht-diagram · 品牌级可视化（diagram-design 引擎）

用已嫁接的 [diagram-design](https://github.com/cathrynlavery/diagram-design) 引擎（`diagram-design/`，MIT）生成**自包含 HTML+SVG** 图：审美统一、可贴品牌、双击即看。与 archify（`/cht-arch`）取向相反——**这里追求“好看+品牌一致”，archify 追求“结构正确+先校验”**。

## 用法

```
/cht-diagram <用大白话描述要什么图>  [可选: 明暗 / 尺寸 / 受众]
```

例如：
- `/cht-diagram 给我画一个三层架构图：前端、后端、PostgreSQL、Redis 缓存` → 选 Architecture，出 `template.html`
- `/cht-diagram 用深色、16:9 幻灯片画一个 bearer token 调用在 401 时刷新时序图` → 选 Sequence，出 `template-dark.html` + slide 预设
- `/cht-diagram 把这份 Mermaid 重画成我们品牌风格` → 走 `import-mermaid.md`
- `/cht-diagram 导出这张图成 PNG 和 SVG` → 走 `references/export.md`

## 执行步骤

1. **选语义模式（若行为承载含义）**：读 `diagram-design/references/semantic-patterns.md`，必要时先选一个行为模式。
2. **选图型**：按 `diagram-design/SKILL.md` §3 视觉类型表选最接近的图型（架构/流程图/时序/状态机/ER/甘特/象限/雷达/桑基/鱼骨/Wardley/看板/部署/UML 类/数据库 schema 等 45 种）。
3. **加载类型参考（必读）**：`Read diagram-design/references/type-<图型>.md`，照其布局语法画。
4. **设四旋钮**：Format(html/svg/png) × Size(10 种预设) × Detail(≤24/≤12/≤7 节点) × Audience(工程师/混合/高管)——详见 `diagram-design/references/output-spec.md`。
5. **复制模板**：从 `diagram-design/assets/template.html`（浅）/ `template-dark.html`（深）/ `template-full.html`（完整）/ `template-terminal.html`（终端）复制，替换 eyebrow/h1/SVG 体，解析 `style-guide.md` 里的 `{ink}`/`{accent}` 等占位符。
6. **跑审美闸门**：按 `diagram-design/SKILL.md` §9 清单过一遍（删减测试、accent≤2、4px 网格、连线 6 规则、无障碍 SVG 契约、自检查 `python3 diagram-design/scripts/self_check.py <file>`）。
7. **交付**：单文件 HTML，双击即看。要 SVG/PNG 走 `references/export.md`（PNG 需 Playwright）。

## 品牌入驻（首次在某项目画图前）

开 `diagram-design/references/style-guide.md` 看是否还是出厂默认（paper `#f5f5f5` / ink `#2d3142` / accent `#bf4520`）。若是，先暂停询问是否做品牌适配（网址 / 本地设计系统 / 粘贴 token / 保存 profile），流程见 `diagram-design/references/onboarding.md`。多品牌并行项目用 `.diagram-design` 标记 + `references/profiles.md`。

## 与 archify 的分工

- “画好看点 / 跟我们品牌一致 / 做 PPT 配图” → **本命令（diagram-design）**
- “别画错 / 先校验结构 / 系统到底怎么跑” → `/cht-arch`（archify）

## 参考总览

详见 `references/15-diagram-design.md`（引擎说明、文件地图、反模式速记）。上游图库示例：https://cathrynlavery.github.io/diagram-design/ （本库未搬运示例 HTML，避免臃肿）。
