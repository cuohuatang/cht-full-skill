---
name: cht-status
description: 读 docs/cht/ 下的产出，报告当前处于流水线哪一阶段、缺什么、下一步做什么。
version: "0.0.1"
---

# /cht-status — 状态盘点

## 执行

1. **读文件**（有则读，无则记缺失）：
   ```
   docs/cht/SPEC.md
   docs/cht/PLAN.md
   docs/cht/LEDGER.md      （只看最近 20 行）
   docs/cht/REVIEW.md
   docs/cht/QA-REPORT.md
   docs/cht/RELEASES.md
   ```
2. **判阶段**（八阶段表反查，取最靠后且已满足门禁的那个）：

   | 阶段 | 满足条件 |
   |---|---|
   | Think | 六问有记录 |
   | Spec | SPEC 四块齐全且用户批准 |
   | Plan | PLAN 任务四要素齐全且批准 |
   | Build | ledger 有全部任务 RED+GREEN |
   | Review | P0/P1 清零 |
   | Test | QA 报告无未关闭 P0/P1 |
   | Ship | 已合并且观察期通过 |
   | Reflect | RETRO 四条已填 |

3. **报告**（严格三行 + 一张缺口表）：

```
上次做到：<最后一条 ledger / 最后一个已完成阶段>
当前状态：阶段 <N> <名称>，<绿灯数量>/13 门禁
下一步：<一个具体动作，带命令>
```

| 缺口 | 影响 | 补法 |
|---|---|---|

## 禁止

- 凭记忆汇报（必须读文件）
- 说"基本完成了"（门禁要么满足要么不满足）
- 一次列出十个下一步（只给一个）

## 判据

用户读完这三行，能知道要不要现在动手、动哪一下。
