# S 安全 · kubernetes

首次使用本环境或工具不匹配时读 [kubernetes](../../tools/kubernetes.md)。缺输入才读 [Helper](../../helpers.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `KUBERNETES/networkpolicy`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" get networkpolicies -o json` | 读取命名空间网络策略声明 | context、namespace | 实际生效依赖网络插件；无策略不等于所有路径畅通 |
| `KUBERNETES/permission`<br>`kubectl --context "$context" --request-timeout=15s auth can-i get pods -n "$namespace"` | 检查当前身份是否获准读取 Pod | context、namespace | 仅此身份、动作和作用域；no 可返回非零 |
