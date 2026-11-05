# Kubernetes

- 可选环境。先用 `kubectl version --client`、所选子命令 `--help` 核验；确认目标 context 和权限后再查集群。
- 每次集群查询显式指定 context；命名空间对象另指定 namespace。节点、PV、StorageClass 是集群级对象。
- 记录 Pod UID 和容器名；Pod 名称可重用。容器内执行时还需识别容器 OS；当前契约不包含 exec 或调试容器。
- 通用 kubectl 不要求 GKE 前置步骤。华为云 CCE 的认证、CSI、网络插件和指标能力按实际集群核验；本地 kind 结果不等于 CCE 验证。
- `top` 依赖 metrics API；没有指标不能报告使用率为零。

- 查询使用已配置的 Kubernetes API 通道；修改 kubeconfig、创建资源或安装组件须另核影响与授权。

## 契约入口

[共享查询](../commands/common/kubernetes.md) · [C 配置](../commands/configuration/kubernetes.md) · [F 故障](../commands/fault/kubernetes.md) · [P 性能](../commands/performance/kubernetes.md) · [S 安全](../commands/security/kubernetes.md)
