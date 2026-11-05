# F 故障 · kubernetes

首次使用本环境或工具不匹配时读 [kubernetes](../../tools/kubernetes.md)。缺输入才读 [Helper](../../helpers.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `KUBERNETES/pod-events`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" get events --field-selector "involvedObject.uid=$uid" -o json` | 读取指定 Pod UID 的事件 | uid: Kubernetes.PodUID；缺失→[H-pod](../../helpers.md#h-pod) | 事件有保留期；空结果不证明无故障 |
| `KUBERNETES/pod-describe`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" describe pod "$pod"` | 读取 Pod 状态、条件和关联事件 | context、namespace、pod；缺失→[H-pod](../../helpers.md#h-pod) | 人类输出随版本变化；UID 由 pods 查询核对 |
| `KUBERNETES/container-logs`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" logs "$pod" -c "$container" --since-time="$start" --timestamps=true` | 读取当前容器实例的日志 | context、namespace、pod、container、RFC3339 start | 非 follow；受日志保留范围限制；不含前一实例 |
| `KUBERNETES/previous-logs`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" logs "$pod" -c "$container" --previous --timestamps=true` | 读取前一容器实例的日志 | context、namespace、pod、container | 无前一实例可返回错误；不等于权限错误 |
