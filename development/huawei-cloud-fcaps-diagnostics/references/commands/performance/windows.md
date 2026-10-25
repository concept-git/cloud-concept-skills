# P 性能 · windows

首次使用本环境或工具不匹配时读 [windows](../../tools/windows.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/windows.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WINDOWS/counter`<br>`Get-Counter -Counter $counter -SampleInterval 1 -MaxSamples 5 -ErrorAction Stop` | 每秒读取指定计数器，共 5 次 | counter: 目标主机已发现的计数器路径 | 需计数器支持；路径可能本地化；不硬编码英文路径 |
| `WINDOWS/processes`<br>`Get-Process -ErrorAction Stop` | 读取进程及可见资源统计 | 目标 Windows 主机 | CPU 属性为累计处理器时间，不是瞬时百分比 |
| `WINDOWS/nic-statistics`<br>`Get-NetAdapterStatistics -Name $adapter -ErrorAction Stop` | 读取网卡累计计数 | adapter: Windows.AdapterName；来自网卡查询 | 速率需两次采样及时间差；模块与驱动影响字段 |
