# F 故障 · windows

首次使用本环境或工具不匹配时读 [windows](../../tools/windows.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/windows.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WINDOWS/service-status`<br>`Get-Service -Name $service -ErrorAction Stop` | 读取指定服务运行状态 | service: Windows.ServiceName；缺失→[H-win-service](../../helpers.md#h-win-service) | 按单个目标查询时拒绝通配符；Running 不证明业务可用 |
| `WINDOWS/events`<br>`Get-WinEvent -FilterHashtable $filter -ErrorAction Stop` | 读取匹配的 Windows 事件 | filter: LogName、StartTime、EndTime；来自事件通道和时间窗 | 使用带时区时间对象；无匹配事件可产生错误记录，需区别权限错误 |
| `WINDOWS/dns`<br>`Resolve-DnsName -Name $name -Type A -ErrorAction Stop` | 主动查询 A 记录 | name: DNS 名称；来自目标依赖 | 发起网络请求；缓存与解析路径影响结果 |
| `WINDOWS/tcp-probe`<br>`Test-NetConnection -ComputerName $hostName -Port $port -InformationLevel Detailed` | 主动测试目标 TCP 端口 | hostName、port；来自已确认的依赖 | 检查 TcpTestSucceeded；端口连通不证明应用健康 |
| `WINDOWS/pid-services`<br>`tasklist.exe /svc /fi "PID eq $targetPid" /fo table` | 读取指定 PID 承载的 Windows 服务 | targetPid: Windows.ProcessId；来自连接或进程查询 | 仅正整数；PID 可重用；/svc 使用 table 格式；检查原生命令退出状态 |
