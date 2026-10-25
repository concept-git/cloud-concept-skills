# FCAPS 地图

先选问题类别，再选事实所在环境。已知完整 ID 时直接搜索命中行，不必读取整张地图。

| 类别 | hcloud | Linux | Windows | Kubernetes（可选） | 文档指引 |
| --- | --- | --- | --- | --- | --- |
| F 故障 | [hcloud](fault/hcloud.md) | [linux](fault/linux.md) | [windows](fault/windows.md) | [kubernetes](fault/kubernetes.md) | [官方主题](../documents/huaweicloud.md#f-故障) |
| C 配置 | [hcloud-network](configuration/hcloud-network.md) · [hcloud](configuration/hcloud.md) | [linux](configuration/linux.md) | [windows](configuration/windows.md) | [kubernetes](configuration/kubernetes.md) | [官方主题](../documents/huaweicloud.md#c-配置) |
| A 计量计费 | [hcloud](accounting/hcloud.md) | — | — | — | [官方主题](../documents/huaweicloud.md#a-计量计费) |
| P 性能 | [hcloud](performance/hcloud.md) | [linux](performance/linux.md) | [windows](performance/windows.md) | [kubernetes](performance/kubernetes.md) | [官方主题](../documents/huaweicloud.md#p-性能) |
| S 安全 | [hcloud-host](security/hcloud-host.md) · [hcloud](security/hcloud.md) | [linux](security/linux.md) | [windows](security/windows.md) | [kubernetes](security/kubernetes.md) | [官方主题](../documents/huaweicloud.md#s-安全) |
| 共享查询 | [hcloud](common/hcloud.md) | [linux](common/linux.md) | [windows](common/windows.md) | [kubernetes](common/kubernetes.md) | — |
| 扩展 | [hcloud](extensions/hcloud.md) | — | — | — | — |

F：事件、故障状态；C：配置、对象关系；A：实际计量和费用；P：指标与采样；S：访问控制和安全观测。共享查询仅放跨类别的身份、发现与日志入口；扩展保留既有边界项目。一个命令模式只有一个定义，其他用途引用它。

命令四列：完整操作或模式、直接取得的事实、关键输入及缺失来源、必要约束。hcloud ID 保留服务／操作／版本；系统 ID 区分环境和操作模式。详细参数查帮助；决定范围、采样口径或影响的参数保留在契约中。

按工具维护：[hcloud](../tools/hcloud.md) · [Linux](../tools/linux.md) · [Windows](../tools/windows.md) · [Kubernetes](../tools/kubernetes.md)。执行遵守[主入口规则](../../SKILL.md#安全规则)；依赖绑定只在 [Helper](../helpers.md) 定义。
