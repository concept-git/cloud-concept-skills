# C 配置 · windows

首次使用本环境或工具不匹配时读 [windows](../../tools/windows.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/windows.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WINDOWS/services`<br>`Get-Service -ErrorAction Stop` | 列出 Windows 服务名与状态 | 目标 Windows 主机 | Name 与 DisplayName 分开；输出范围受权限影响 |
| `WINDOWS/disks`<br>`Get-Disk -ErrorAction Stop` | 读取磁盘编号、标识和状态 | 目标 Windows 主机 | 需 Storage 模块；磁盘编号不是 EVS ID |
| `WINDOWS/partitions`<br>`Get-Partition -ErrorAction Stop` | 读取磁盘分区及访问路径 | 目标 Windows 主机 | 需 Storage 模块；按 DiskNumber 和 PartitionNumber 绑定 |
| `WINDOWS/volumes`<br>`Get-Volume -ErrorAction Stop` | 读取卷、文件系统和容量 | 目标 Windows 主机 | 需 Storage 模块；无盘符的卷仍可能存在 |
| `WINDOWS/adapters`<br>`Get-NetAdapter -ErrorAction Stop` | 读取网卡名称、索引及 MAC | 目标 Windows 主机 | 需 NetAdapter 模块；云网卡绑定按 MAC 核验 |
| `WINDOWS/routes`<br>`Get-NetRoute -ErrorAction Stop` | 读取 IP 路由 | 目标 Windows 主机 | 保留 AddressFamily 和接口索引 |
| `WINDOWS/connections`<br>`Get-NetTCPConnection -ErrorAction Stop` | 读取 TCP 连接及 OwningProcess | 目标 Windows 主机 | 连接瞬时变化；PID 需同主机同时间核验；端口按 LocalPort 数值匹配，不做文本包含匹配 |
| `WINDOWS/counter-discovery`<br>`Get-Counter -ListSet * -ErrorAction Stop` | 发现目标主机计数器集合与路径 | 目标 Windows 主机 | 按所需集合选路径；可用项受组件和语言影响 |
| `WINDOWS/logical-disk-links`<br>`Get-CimInstance -ClassName Win32_LogicalDiskToPartition -ErrorAction Stop` | 读取 Windows 逻辑卷与分区的关联 | 目标 Windows 主机 | Antecedent／Dependent 是对象路径；需结合磁盘编号和序列号 |
| `WINDOWS/disk-identity`<br>`Get-CimInstance -ClassName Win32_DiskDrive -ErrorAction Stop` | 读取磁盘设备名称、序列号和型号 | 目标 Windows 主机 | 按设备类型解释序列号；不把磁盘编号当 EVS ID |
| `WINDOWS/signed-drivers`<br>`Get-CimInstance -ClassName Win32_PnPSignedDriver -Filter "DeviceClass = 'NET'" -ErrorAction Stop` | 读取已登记网卡驱动的设备、版本和日期 | 目标 Windows 主机 | 按目标设备核验；名称包含 virtio 不足以证明发生文档中的驱动故障 |
