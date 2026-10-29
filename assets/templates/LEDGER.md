# LEDGER

> 一行一条，不写叙事。跨上下文唯一的记忆。
> 类型：`RED` `GREEN` `RULING` `BLOCKED` `DEBUG`

```
[T1] YYYY-MM-DD HH:MM RED    <test file>::<case> → 断言失败（预期原因：<X>）
[T1] YYYY-MM-DD HH:MM GREEN  实现 N 行，通过，commit <sha>
[T2] YYYY-MM-DD HH:MM RULING 选同步调用而非队列 —— 量级不需要异步，出错代价是延迟 +200ms
[T3] YYYY-MM-DD HH:MM BLOCKED <现象>，当前假设：<X>，缺的证据：<Y>
[T3] YYYY-MM-DD HH:MM DEBUG  根因 <X> / 修复 <文件:行> / 回归 <test>::<case> / 同类检查 <结论>
```

## 当前进度

- 任务：T<N> / 共 <M>
- 阻塞：<无 / 列表>
- 下一步：<一个动作>
