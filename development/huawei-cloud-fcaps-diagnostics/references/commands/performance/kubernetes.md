# P 性能 · kubernetes

首次使用本环境或工具不匹配时读 [kubernetes](../../tools/kubernetes.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/kubernetes.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `KUBERNETES/pod-usage`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" top pod "$pod" --containers` | 读取容器当前 CPU 与内存使用 | context、namespace、pod | 依赖 metrics API；缺指标不等于零使用 |
| `KUBERNETES/node-usage`<br>`kubectl --context "$context" --request-timeout=15s top nodes` | 读取节点当前资源使用 | context | 依赖 metrics API；不是账单数据 |
