# 分诊

复用已知目标和时间窗。只有歧义会改变查询路径时才询问。

| 已知现象 | 首选事实 | 下一步条件 |
| --- | --- | --- |
| 无法登录、启动失败 | F：云状态、主机日志 | SSH 不通先查云侧网络；不把端口通当登录成功 |
| 配置、资源关系不明 | C：目标资源和系统配置 | 云与主机标识不同则查 Helper |
| 高负载、慢、容量不足 | P：同时间窗指标和有限采样 | df/du 差异先查打开的已删除文件；抓包、跟踪和压测另核执行影响 |
| 权限、异常访问 | S：策略、连接、事件 | 保留实际执行身份；异常迹象不是已确认入侵 |
| 用量或费用异常 | A：同范围计量、账单 | 系统利用率只作辅助证据 |
| Pod 重启、挂载或调度失败 | 可选 Kubernetes 的 F/C/P | 绑定 context、namespace、UID；进入节点前识别 OS |

按 [FCAPS 地图](commands/index.md) 选册。场景配方仍仅为[规划](recipes/boot.md)。其他规划：[登录](recipes/login.md)、[网络](recipes/network.md)、[存储](recipes/storage.md)、[性能](recipes/performance.md)、[崩溃](recipes/crash.md)、[配置](recipes/configuration.md)、[安全](recipes/security.md)、[恢复](recipes/recovery.md)。
