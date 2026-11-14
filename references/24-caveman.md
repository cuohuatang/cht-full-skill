# caveman · 会话输出压缩（Julius Brussee，Apache-2.0）

> 来源：[`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) v4.1.0
> 版权：**Julius Brussee**｜许可：**Apache-2.0**（3.0.0 起全仓库转 Apache-2.0；`LICENSE-MIT` 仅为 3.0 前历史贡献保留）｜星标：约 12 万
> 三档技能已整包嫁入 `skills/caveman/`、`skills/ultracave/`、`skills/megacave/`。本文件是"它是什么 + **在 cht 里的边界** + 许可"的指针。

## 先纠正两个流传很广的误传

| 说法 | 实际情况 |
|---|---|
| "**省 65% token**" | 那是它的 **proxy / engine 压缩层**的数字，**不是这个 skill**。官方 README 写明的 skill 实测（3.1.0 文本、10 条 prompt、单次运行、仅测输出长度）：**caveman 默认档 3%**（在噪声内）、**ultracave 35%**、**megacave 9%**，且**没有发布质量等价声明** |
| "**MIT 协议**" | 3.0.0 之前是 MIT，之后**全仓库 Apache-2.0**。当前 4.1.0 按 Apache-2.0 处理 |

**所以别为了省 token 而装它**——默认档几乎不省。它真正有价值的是**输出纪律**：answer first、砍客套、payload 逐字保留、一句一意。这恰好和 cht 的"反模式清单"里"没有证据的断言 = 撒谎""别写小作文"同源。

## 三档

| 技能 | 命令 | 压缩程度 | 触发方式 |
|---|---|---|---|
| `caveman` | `/cht-caveman` | 温和：去客套/填充词，冠词可省，**技术事实全留** | 显式开启 |
| `ultracave` | `/cht-caveman ultra` | 极限：语法剥离、片段化、一个词够就一个词 | `disable-model-invocation: true`，**只认命令，agent 不会自己切** |
| `megacave` | `/cht-caveman wenyan` | 文言文，术语逐字保留 | 同上 |

持久到会话结束，直到 `stop caveman` 或 `normal mode`。`/caveman status` 只报状态、不改状态。

## ⚠️ 与 cht 三条铁律的冲突 — 必须在 cht 里划死的边界

caveman 是**压缩会话输出**的，而 cht 第 3 条铁律要求"**跑命令、贴完整输出、读完完整输出**才能说完成"。二者直接冲突。**因此在 cht 里一律按下面执行**：

| 内容 | 是否压缩 |
|---|---|
| 会话旁白、解释、进度说明、状态汇报 | ✅ 可压缩 |
| **命令的完整输出 / 测试日志 / 报错栈 / 验证证据** | ❌ **原样保留，一个字符不动** |
| **`docs/cht/` 下所有产出物**（SPEC / PLAN / REVIEW / QA-REPORT / RETRO / LEDGER） | ❌ **正常散文全文，绝不压缩** |
| 代码、代码注释、commit message、PR、issue、memory 文件 | ❌ 正常散文 |
| 安全警告、不可逆操作确认、步骤顺序、用户困惑时、提问/给选项 | ❌ 正常散文 |

这**不是我们加的限制**，正是上游 SKILL.md 自己的 7 条「When to break the rules」+ 规则 6「Payload verbatim」写的——cht 只是把它显式化、提高优先级。**冲突时，cht 三条铁律 > caveman 压缩规则**，永远如此。

> 换句话说：caveman 在 cht 里是"**嘴变小**"，不是"证据变少"。`Brain still big. Mouth small.` 这句上游定位仍然成立，但 cht 额外要求：**该贴的证据一个字都不能少**。

## 默认关闭，显式开启

caveman 上游是"加载即常驻、直到关闭"。但它若默认生效会污染 cht 的产出物标准。**在 cht 里默认 off**：只有用户明确说 `/cht-caveman`（或"caveman 模式 / 简短点 / 少废话"）才开启，且**开启时先声明边界**（上表）。`ultracave` / `megacave` 上游自带 `disable-model-invocation: true`，天然不会擅自触发——这个设计正好。

## 上游九条规则速记（详见 `skills/caveman/SKILL.md`）

1. Answer first — 先答案，再理由，再下一步
2. Kill ceremony — 无问候/对冲/客套/复述/收尾
3. Short word — 用短词，但不自造缩写
4. Articles optional — 冠词可省，**否定词 not/never/no/only/except 永不省**
5. One idea per sentence — ≤20 词、主动语态、指令用祈使
6. **Payload verbatim** — 代码块、命令、路径、API 名、错误串逐字保留
7. Tool runs bounded status — 多步运行：开头一行 + 阶段变化一行 + 结果一行
8. User's language — 只压缩风格，**不切换语言**（cht 要求简体中文，此条正好契合）
9. Never perform caveman — 不说"caveman mode on"、不加"me think"、不用装饰表格/emoji 装腔

**Pre-send check**：首句是不是在宣布要做什么（删）？末句是不是在复述或提供帮助（删）？否定词/数字/路径/错误串是否全在？有没有歧义句（改回完整句）？

## 文件地图

| 路径 | 作用 |
|---|---|
| `skills/caveman/SKILL.md` | 主档（4.7KB）：九条规则 + 7 条破例 + pre-send check |
| `skills/caveman/README.md` | 三档对照、调用方式、**官方实测数据** |
| `skills/ultracave/SKILL.md` | 极限压缩档 |
| `skills/megacave/SKILL.md` | 文言文档 |
| `skills/caveman/LICENSE` | **Apache-2.0 全文 —— 保留** |
| `skills/caveman/NOTICE` | **上游 NOTICE（版权行 + 第三方归因）—— Apache-2.0 要求随附，保留** |
| `skills/caveman/LICENSE-MIT` | 3.0.0 前历史 MIT 文本（上游为历史贡献保留，一并带入） |

**未嫁**（以下均为**上游仓库内**的路径，本仓库不存在、也不需要）：`activation-rule.mjs`（Node hook）、`caveman-compress/scripts/compress.py`（60KB Python 压缩引擎）、`caveman-proxy` / `engine` / `browse` / `mcp` / Docker / CI / 各 agent 的 `compile.mjs` —— 全是运行时，会摧毁 cht「纯 Markdown + POSIX shell、0 运行时依赖」的立身之本。本仓库只取**纯文本规则**。

## 许可（区别于本仓库其余 MIT 来源）

caveman 是 **Apache-2.0**，与 skill-creator 同级、非 MIT。Apache-2.0 要求：
1. **保留** `LICENSE` 与 `NOTICE`（已随 `skills/caveman/` 带入，勿删）；
2. 对原文件的**修改要标注**（本仓库对三个 SKILL.md **未作任何修改**，原样带入）；
3. 再分发时附带许可证文本。

商标注意：上游 `TRADEMARKS.md` 声明 "Caveman" 及 logo 为商标，Apache-2.0 不授予商标权；本仓库仅作**署名性引用**（"嫁接自 JuliusBrussee/caveman"），不暗示背书或赞助。

本仓库主许可仍为 **MIT**，凡含 caveman 的部分以 **Apache-2.0** 为准。`NOTICE.md` 已单列该来源。
