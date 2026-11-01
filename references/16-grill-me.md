---
title: grill-me / grilling · 决策护栏（防止 AI 擅自做主）
---

# grill-me + grilling · 决策护栏

> 来源：[mattpocock/skills](https://github.com/mattpocock/skills)（Matt Pocock，MIT）。
> `grill-me` 是用户触发的**入口**，`grilling` 是真正的"盘问"**引擎**。本仓库把两者一并嫁接入
> `skills/grill-me/` 与 `skills/grilling/`（`grill-me` 内部 `Call the Skill tool with "grilling"`，缺了引擎就成死链）。

## 它解决什么问题

AI 最容易翻车的不是"不会做"，而是**稀里糊涂就替你做了决定、擅自改了东西**：

- 需求还没问清，就列出一整套技术方案；
- 你觉得"差不多"它就开干，方向偏了还一路推进；
- 把"我猜你想要这样"当成"你确认了"，改完才告诉你。

`grill-me` / `grilling` 用**一轮轮的追问**（设计树 + frontier）把含糊想法逼成可执行的共识——每轮都给你推荐答案、等你拍板，
**在你说"达成共识"之前绝不动手**。

## 何时用

- 你说 "grill me / 盘问我 / 先确认再动手 / 别急着做，先问我"；
- 一个想法值得认真做，但还没想清楚（功能方向、产品取舍、技术选型、要写的东西）；
- cht-full-skill 进入阶段 0（Think）前，需求还很模糊时，优先用它逼出真需求。

> 它是**用户驱动**的护栏：上游 `grill-me` 设了 `disable-model-invocation: true`（对应 `agents/openai.yaml` 里 `allow_implicit_invocation: false`），
> 即 agent **不会自己偷偷调用**，必须由你或本仓库的流程显式触发——这正好把"擅自做主"关进笼子。

## 调用

```
/cht-grill <用大白话描述你的想法>
```

agent 会加载 `skills/grilling/SKILL.md` 的盘问协议，按"设计树 + frontier + 轮次"进行访谈。

## grilling 访谈协议（引擎逻辑，摘录自 skills/grilling/SKILL.md）

1. **设计树（design tree）**：把"要做的事"拆成决策树，每个决策挂在其依赖的决策之下。
2. **轮次（rounds）**：每一轮只问**前沿（frontier）**——即"前置依赖已确定的那些问题"，一轮把整片 frontier 一起问完，逐条编号并给出**推荐答案**。
3. **格式**：
   ```
   ❓ Q1 - 标题：问题正文（可含多段与多个选项）
   ➡️ 你的推荐答案
   ---
   ❓ Q2 - ...
   ```
4. **推荐答案写成"是就接受"**：让用户说"是"即采纳你的推荐，降低决策成本。
5. **每轮答案重塑树**：已定的决策把 frontier 往外推，解锁依赖它们的问题；依赖本轮还没回答的问题，留到下一轮。
6. **事实归 agent，决定归用户**：需要查环境/文件的"事实"由 agent 派子代理去查，**不要让用户回答 agent 能查到的东西**；需要拍板的"决定"才抛给用户。
7. **frontier 空了 = 访谈结束**：每根分支都走到，没有留任何"默认假设"。结束前**不行动**，等用户确认达成共识。

## 与本仓库纪律的关系

cht-full-skill 的**三条铁律**第一条就是"没有 spec 不写计划；没有计划不写代码"。
`grill-me` 是这条纪律在"动手前"的具象化工具——它把"六问逼出真需求"（阶段 0）变成可操作的连续访谈，
防止 agent 在需求没确认时就替你下判断。

| 反模式 | grill 怎么治 |
|---|---|
| 需求没问清就开写 | 先 `/cht-grill`，frontier 空了才动手 |
| 把"猜你想要"当"你确认" | 每轮必须你拍板，推荐答案"是即采纳" |
| 一路推进不回头 | 设计树每轮重塑，偏差立刻暴露 |

## 文件地图

- `skills/grill-me/SKILL.md` — 入口技能（用户触发 → 调用 grilling）
- `skills/grill-me/agents/openai.yaml` — 代理接口声明（display "Grill Me"，禁止隐式调用）
- `skills/grill-me/docs.md` — 上游完整说明（驱动器/可盘问性/常见问答等）
- `skills/grilling/SKILL.md` — 盘问引擎逻辑（设计树 / frontier / 轮次）
- `skills/grilling/agents/openai.yaml` — 引擎接口声明

调用与协议细节见 `commands/cht-grill.md`。
