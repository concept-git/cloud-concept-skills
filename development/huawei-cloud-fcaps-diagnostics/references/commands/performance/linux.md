# P 性能 · linux

首次使用本环境或工具不匹配时读 [linux](../../tools/linux.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/linux.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LINUX/process-snapshot`<br>`top -b -n 1` | 读取一次进程和系统资源快照 | 目标主机 | 需 procps；首帧 CPU 统计口径须结合工具版本解释 |
| `LINUX/memory`<br>`free -b` | 读取内存与交换空间统计 | 目标主机 | 字节；available 与 free 含义不同 |
| `LINUX/vm-sample`<br>`vmstat -w 1 5` | 每秒采样系统统计，共 5 行报告 | 目标主机 | 首行通常为启动以来平均值；后续为间隔值 |
| `LINUX/disk-sample`<br>`iostat -x -y 1 5` | 每秒采样磁盘扩展统计，共 5 次 | 目标主机；关联 EVS 需 [H-device](../../helpers.md#h-device) | 需 sysstat；-y 跳过启动累计报告；单一 util 值不能证明磁盘饱和 |
| `LINUX/process-io`<br>`pidstat -d 1 5` | 每秒采样进程 I/O，共 5 次 | 目标主机 | 需 sysstat；进程退出可导致记录消失 |
| `LINUX/cpu-sample`<br>`mpstat -P ALL 1 5` | 每秒采样各 CPU，共 5 次 | 目标主机 | 需 sysstat；采样窗口不代表长期趋势 |
| `LINUX/filesystem-space`<br>`df -B1 -- "$path"` | 读取目标路径所在文件系统的容量 | path: 已确认存在的路径 | 字节；容量不等于 EVS 计费容量；与 du 不同口径，差异需查 deleted-open-files |
| `LINUX/filesystem-inodes`<br>`df -i -- "$path"` | 读取目标文件系统的 inode 使用 | path: 已确认存在的路径 | 部分文件系统的 inode 统计不适用 |
| `LINUX/nic-statistics`<br>`ip -statistics -json link show dev "$iface"` | 读取接口累计收发及错误计数 | iface: Linux.InterfaceName；缺失→[H-interface](../../helpers.md#h-interface) | 累计值需两次采样及时间差才能计算速率 |
| `LINUX/driver-statistics`<br>`ethtool -S "$iface"` | 读取网卡驱动统计 | iface: Linux.InterfaceName；缺失→[H-interface](../../helpers.md#h-interface) | 字段依赖驱动；不支持统计与计数为零分别处理 |
| `LINUX/packet-capture`<br>`timeout "$seconds" tcpdump -i "$iface" -nn -c "$count" "$filter"` | 按接口和过滤条件采集报文摘要 | iface、seconds、count、BPF filter；来自已确认连接 | 有条件采集；有权限与开销要求；timeout 的 124 与采集错误分别记录 |
| `LINUX/syscall-trace`<br>`timeout "$seconds" strace -p "$pid" -f -c` | 附加进程并统计系统调用 | pid: Linux.Pid；seconds: 正整数秒 | 有条件采集；ptrace 权限；可扰动进程；超时后确认已脱离 |
| `LINUX/perf-sample`<br>`perf stat -p "$pid" -- sleep "$seconds"` | 采样进程性能计数器 | pid: Linux.Pid；seconds: 正整数秒 | 有条件采集；perf 与内核及权限须兼容；输出含 stderr |
| `LINUX/directory-usage`<br>`timeout 15s du -x -B1 --max-depth=1 -- "$path"` | 统计指定目录一层的已分配空间 | path: 已限定诊断目录 | 遍历有 I/O 开销；不跨文件系统；超时结果不完整；不等于 df 容量口径 |
| `LINUX/run-queue`<br>`sar -q 1 5` | 每秒采样运行队列与负载，共 5 次 | 目标主机 | 需 sysstat；显式间隔读取当前采样，不混用历史归档 |
| `LINUX/thread-inventory`<br>`ps -eLo pid,lwp,stat,comm --no-headers` | 读取进程／线程标识及状态 | 目标主机 | 线程行数不同于进程数；不将 fork 失败单独归因于 PID 上限 |
| `LINUX/conntrack-capacity`<br>`sysctl net.netfilter.nf_conntrack_count net.netfilter.nf_conntrack_max` | 读取连接跟踪当前条目数与容量上限 | 目标主机 | 需内核连接跟踪支持；仅采样现值，不调参；需结合丢包日志解释 |
