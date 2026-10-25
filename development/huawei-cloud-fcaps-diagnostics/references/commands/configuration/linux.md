# C 配置 · linux

首次使用本环境或工具不匹配时读 [linux](../../tools/linux.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/linux.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LINUX/units`<br>`systemctl list-units --type=service --all --no-pager` | 列出服务单元及状态 | 目标主机 | 需 systemd；包含已加载单元，不等于所有 unit 文件 |
| `LINUX/block-devices`<br>`lsblk --json --output NAME,KNAME,PATH,TYPE,SIZE,FSTYPE,MOUNTPOINTS,SERIAL` | 读取块设备、挂载点和序列号 | 目标主机 | 列支持随 util-linux 版本变化；路径不等于 EVS ID |
| `LINUX/mounts`<br>`findmnt --json --output TARGET,SOURCE,FSTYPE,OPTIONS` | 读取当前挂载关系 | 目标主机 | 需 util-linux；挂载来源不直接等于云盘标识 |
| `LINUX/addresses`<br>`ip -json address show` | 读取接口、MAC 和地址 | 目标主机 | 需 iproute2；接口到云网卡的绑定见 H-interface |
| `LINUX/routes`<br>`ip -json route show table all` | 读取 IPv4 路由表 | 目标主机 | 含多路由表；策略规则和 IPv6 需分别查询 |
| `LINUX/rules`<br>`ip -json rule show` | 读取 IPv4 策略路由规则 | 目标主机 | 规则与路由表联合解释；不证明端到端可达 |
| `LINUX/modules`<br>`lsmod` | 读取已加载内核模块 | 目标主机 | 未列出不等于功能不存在，可能内建于内核 |
| `LINUX/timers`<br>`systemctl list-timers --all --no-pager` | 读取 systemd 定时器 | 目标主机 | 需 systemd；不覆盖 cron 等其他调度器 |
| `LINUX/connections`<br>`ss -H -antp` | 读取 TCP 连接及可见进程关联 | 目标主机 | 进程信息受权限影响；是瞬时快照 |
| `LINUX/disk-by-id`<br>`ls -l /dev/disk/by-id/` | 读取磁盘稳定名称到设备路径的链接 | 目标主机 | 磁盘与分区链接分开；文件系统 UUID、序列号、EVS ID 不混用 |
| `LINUX/udev-device`<br>`udevadm info --query=property --name="$blockDevice"` | 读取块设备的 udev 属性及序列号 | blockDevice: Linux.BlockDevice；来自 block-devices | 查询整盘时排除分区；云盘绑定见 H-device |
| `LINUX/filesystem-id`<br>`blkid -o export "$device"` | 读取设备的文件系统 UUID、类型和分区属性 | device: 已确认磁盘或分区路径 | 文件系统 UUID 不是 EVS ID；克隆文件系统可出现重复 UUID |
| `LINUX/partition-table`<br>`fdisk -l "$blockDevice"` | 读取指定整盘的分区表 | blockDevice: Linux.BlockDevice；来自 block-devices | 仅 -l 查询；不得进入交互式分区编辑 |
| `LINUX/kernel-setting`<br>`sysctl "$key"` | 读取指定内核参数的当前值 | key: Linux.SysctlKey；来自待核验配置项 | 仅键名，拒绝 =、-w、-p；旧内核参数可能已删除；枚举不当布尔值 |
| `LINUX/service-enabled`<br>`systemctl is-enabled "$unit"` | 读取服务启用状态 | unit: Linux.UnitName；缺失→[H-unit](../../helpers.md#h-unit) | 启用不等于运行；disabled 等状态可非零退出；保留状态文本 |
| `LINUX/network-manager`<br>`nmcli -t device status` | 读取 NetworkManager 管理的设备状态 | 目标主机 | 依赖 NetworkManager；未运行不等于主机无网络 |
| `LINUX/chrony-sources`<br>`chronyc sources -v` | 读取 chronyd 的时间源及选择状态 | 目标主机 | 需 chrony 及守护进程；选中源不证明所有时段时间精度 |
| `LINUX/ntp-peers`<br>`ntpq -pn` | 读取本机 ntpd 的时间对等节点 | 目标主机 | 仅适用于 ntpd；无响应与无配置分别记录 |
