# 共享查询 · kubernetes

首次使用本环境或工具不匹配时读 [kubernetes](../../tools/kubernetes.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/kubernetes.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `KUBERNETES/context`<br>`kubectl config current-context` | 读取当前 kubeconfig 上下文名称 | 现有 kubeconfig | 仅本地配置；不证明集群可访问 |
