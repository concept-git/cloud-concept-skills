# F 故障 · linux

首次使用本环境或工具不匹配时读 [linux](../../tools/linux.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/linux.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LINUX/service-status`<br>`systemctl status "$unit" --no-pager --lines=20` | 读取服务状态及末尾日志 | unit: Linux.UnitName；缺失→[H-unit](../../helpers.md#h-unit) | 需 systemd；退出码 3 可表示未运行；日志最多 20 行 |
| `LINUX/unit-journal`<br>`journalctl --unit "$unit" --since "$start" --until "$end" --no-pager --output=json` | 读取指定服务在时间窗内的事件 | unit: Linux.UnitName；start/end: 带时区时间 | 需 journal；权限、保留期和服务名影响覆盖；空结果不证明无故障 |
| `LINUX/kernel-journal`<br>`journalctl --dmesg --since "$start" --until "$end" --no-pager --output=json` | 读取当前启动的内核事件 | start/end: 带时区时间 | 需 journal；仅当前启动；历史启动需另选 boot |
| `LINUX/kernel-ring`<br>`dmesg --color=never` | 读取当前内核环形日志 | 目标主机 | 可能需 root；可能覆盖旧记录；时间不直接视为墙钟时间 |
| `LINUX/dns-query`<br>`dig +time=2 +tries=1 "$name" A` | 主动查询指定名称的 A 记录 | name: DNS 名称；来自目标依赖 | 发起 DNS 请求；检查 DNS status，不能仅看退出码 |
| `LINUX/icmp-probe`<br>`ping -n -c 3 -W 2 -w 8 "$target"` | 向目标发送 3 次 ICMP 探测，读取应答与丢包 | target: 已确认 IP／主机名 | 主动发包；无应答可能是过滤或限速，不能直接判定主机宕机 |
| `LINUX/mtr-report`<br>`timeout 15s mtr --report --report-cycles 3 --no-dns --json "$target"` | 读取有限轮次的逐跳探测报告 | target: 已确认 IP／主机名 | 主动发包；中间跳不响应不等于转发丢包；超时报告可能不完整 |
| `LINUX/trace-route`<br>`timeout 20s traceroute -n -m 16 -q 1 -w 1 "$target"` | 探测至目标的有限跳数路径 | target: 已确认 IP／主机名 | 主动探测；星号不是故障证明；协议及工具实现需核验 |
| `LINUX/deleted-open-files`<br>`timeout 15s lsof -nP +L1 -F pcftn` | 读取链接数小于 1 的打开文件及持有进程 | 目标主机 | 有扫描开销；无匹配可返回 1；与 df/du 差异联合解释，勿直接杀进程 |
| `LINUX/metadata-http`<br>`curl --noproxy "*" --connect-timeout 2 --max-time 5 --silent --show-error --output /dev/null --write-out "%{http_code}" http://169.254.169.254/` | 读取华为云元数据根目录的 HTTP 状态 | 在已确认的 ECS 内执行 | 主动请求；绕过代理；不读取正文或凭据路径；状态成功不证明所有元数据路径可用 |
