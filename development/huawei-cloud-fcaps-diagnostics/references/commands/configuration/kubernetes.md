# C 配置 · kubernetes

首次使用本环境或工具不匹配时读 [kubernetes](../../tools/kubernetes.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/kubernetes.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `KUBERNETES/nodes`<br>`kubectl --context "$context" --request-timeout=15s get nodes -o json` | 读取节点及 OS 标签 | context: 已确认集群 | 集群级查询；节点 OS 不等于每个容器 OS |
| `KUBERNETES/pods`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" get pods -o json` | 读取命名空间内 Pod 状态和 UID | context、namespace | 记录 UID；同名 Pod 重建后不是同一对象 |
| `KUBERNETES/storage`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" get pvc -o json` | 读取 PVC 绑定和请求容量 | context、namespace | PVC 为命名空间对象；PV 另按 volumeName 查询 |
| `KUBERNETES/pv`<br>`kubectl --context "$context" --request-timeout=15s get pv "$pv" -o json` | 读取指定 PV 和后端标识 | pv: Kubernetes.PVName；来自 PVC spec.volumeName | 集群级对象；未绑定 PVC 不产生 PVName |
| `KUBERNETES/storageclasses`<br>`kubectl --context "$context" --request-timeout=15s get storageclasses -o json` | 读取存储类和 provisioner | context | 驱动由集群决定；不能沿用 GKE 驱动名称 |
| `KUBERNETES/endpoints`<br>`kubectl --context "$context" --request-timeout=15s -n "$namespace" get endpointslices -l "kubernetes.io/service-name=$service" -o json` | 读取 Service 的端点切片和就绪条件 | context、namespace、service: ServiceName | 查询全部匹配切片；存在地址不证明业务可达 |
