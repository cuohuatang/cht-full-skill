---
name: cht-grill
description: 用 grill-me / grilling（mattpocock/skills，MIT）在动手前对用户连续盘问、逼出真实需求与共识、防止 AI 擅自做主。当用户说"grill me / 盘问我 / 先确认再动手 / 别急着做先问我"，或需求模糊、agent 即将替用户拍板时使用。
---

# /cht-grill · 决策护栏（grill-me / grilling）

在动手前把含糊想法逼成共识，**防止 AI 擅自做主、稀里糊涂就跑任务或改东西**。

## 用法

```
/cht-grill <用大白话描述你的想法>
```

例如：
- `/cht-grill 我想做一个把会议录音变成行动项的工具` → 进入轮次访谈，每轮给推荐答案，等你拍板
- `/cht-grill 这个需求到底该不该做` → 逼出真实场景与范围，而不是列方案
- 在 cht-full-skill 阶段 0（Think）前，需求还很模糊时直接 `/cht-grill` 逼问

## 执行步骤

1. 加载盘问引擎：`Read skills/grilling/SKILL.md`（设计树 + frontier + 轮次协议）。
2. 把用户的想法拆成**设计树**，找出前置已定的**前沿（frontier）**。
3. 一轮问完整片 frontier：每条编号、给**推荐答案**（"是即采纳"），等用户回答。
4. 按回答重塑树、解锁下一轮；需要查环境/文件的事实用子代理去查，只把"决定"抛给用户。
5. frontier 空了即结束，**在用户确认达成共识前不行动**。

## 与 cht-full-skill 的配合

- 它是"三条铁律"第一条（无 spec 不写计划）在动手前的具象化工具。
- 与阶段 0 `/cht-spec --discover` 同源：一个偏"连续访谈逼共识"，一个偏"落 SPEC 文档"。先用 `/cht-grill` 想清楚，再 `/cht-spec` 落文档。

## 细节

详见 `references/16-grill-me.md`。上游出处：https://github.com/mattpocock/skills
（`skills/productivity/grill-me` 与 `skills/productivity/grilling`，MIT）。
