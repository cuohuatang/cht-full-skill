---
name: cht-caveman
description: 会话输出压缩一键入口（caveman，Apache-2.0）。默认/极限/文言三档切换，砍掉客套与填充词但技术事实逐字保留。在 cht 里默认关闭、显式开启，且只压缩会话旁白——docs/cht/ 产出物与验证证据永不压缩。
version: "0.0.10"
license: Apache-2.0
---

# /cht-caveman · 会话输出压缩

> 引擎来自 [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) v4.1.0（约 12 万★，**Apache-2.0**，Julius Brussee）。
> 三档技能已嫁入 `skills/caveman/`、`skills/ultracave/`、`skills/megacave/`。
> 边界与实测数据见 `references/24-caveman.md`。

## 什么时候用

- 用户说"**caveman 模式 / 说话简短点 / 少废话 / 别写小作文 / be brief**"
- 长会话想减少旁白占用上下文
- 明确要 `/cht-caveman status` 查当前档位

**默认不生效**。cht 是方法论仓库，产出物要求完整表达；只有显式调用才开启。

## 调用形态

| 命令 | 加载 | 效果 |
|---|---|---|
| `/cht-caveman` | `skills/caveman/SKILL.md` | 默认档：去客套/填充词，技术事实全留 |
| `/cht-caveman ultra` | `skills/ultracave/SKILL.md` | 极限压缩：语法剥离、片段化 |
| `/cht-caveman wenyan` | `skills/megacave/SKILL.md` | 文言文，术语逐字保留 |
| `/cht-caveman status` | — | 只报当前档位，不改状态 |
| `stop caveman` / `normal mode` | — | 关闭，恢复完整散文（一行确认） |

> `ultracave` / `megacave` 上游设 `disable-model-invocation: true`：**agent 不会自己切档**，必须用户显式指定。

## 开启时必须先声明的边界（红牌，违反即停）

caveman 压缩会话输出，cht 第 3 条铁律要求"跑命令、贴完整输出"。**冲突时 cht 铁律优先**：

| 内容 | 压缩？ |
|---|---|
| 会话旁白、解释、进度、状态 | ✅ 可 |
| **命令完整输出 / 测试日志 / 报错栈 / 验证证据** | ❌ **原样，一字不动** |
| **`docs/cht/` 产出物**（SPEC/PLAN/REVIEW/QA-REPORT/RETRO/LEDGER） | ❌ **正常散文全文** |
| 代码、注释、commit、PR、issue、memory 文件 | ❌ 正常散文 |
| 安全警告、不可逆操作确认、步骤顺序、用户困惑、提问/给选项 | ❌ 正常散文 |

其他红牌：
- 删 `skills/caveman/LICENSE` 或 `NOTICE` → Apache-2.0 侵权，**必须保留**
- 为了"更 caveman"而丢掉 `not` / `never` / `no` / `only` / `except`、改数字、改路径、改错误串 → 上游规则 4/6 明禁，直接违规
- 说 "caveman mode on"、"me think"、加装饰表格/emoji 装腔 → 上游规则 9 明禁
- 拿"省 65% token"当卖点 → **不实**；官方 skill 实测默认档仅 3%（见 `references/24-caveman.md`）
- 用文言文/英文改写用户要求的简体中文回复 → 上游规则 8「只压缩风格，不切换语言」

## 输出模板（开启时）

```
Caveman: <caveman / ultracave / megacave / off>
边界：产出物与验证证据保持原样；仅会话旁白压缩。
```

## 与 cht-full-skill 的关系

- **同源**：上游的 "answer first / kill ceremony / payload verbatim" 与 cht 反模式清单里"没有证据的断言 = 撒谎""别写小作文"是一回事，只是把它做成了可切换的语气层。
- **不冲突**：上游 7 条「When to break the rules」本就要求落盘产物用正常散文——cht 把它显式化并提高优先级。
- **定位**：`嘴变小，证据不变`。它不改变任何门禁、不改变产出物标准、不替代 `/cht-review` 或 `/cht-qa`。
