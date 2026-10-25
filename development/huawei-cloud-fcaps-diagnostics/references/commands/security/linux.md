# S 安全 · linux

首次使用本环境或工具不匹配时读 [linux](../../tools/linux.md)。缺输入才读 [Helper](../../helpers.md)；核验适用范围时读 [验证记录](../../verification/linux.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LINUX/recent-logins`<br>`last -n 20` | 读取最近登录记录 | 目标主机 | 只覆盖当前 wtmp 保留范围；最多 20 条 |
| `LINUX/failed-logins`<br>`lastb -n 20` | 读取最近失败登录记录 | 目标主机 | 通常需 root；btmp 缺失不等于无失败；最多 20 条 |
| `LINUX/cron`<br>`crontab -l` | 读取当前用户的 cron 配置 | 当前执行用户 | 无 crontab 可返回非零；不覆盖其他用户或 systemd timers |
| `LINUX/rpm-verify`<br>`rpm -Va` | 扫描已安装 RPM 软件包文件差异 | RPM 系统 | 有扫描开销；差异不直接证明入侵 |
| `LINUX/deb-verify`<br>`debsums -c` | 扫描 Debian 软件包文件校验差异 | Debian 系统 | 需 debsums；有扫描开销；不覆盖所有文件 |
| `LINUX/cpu-mitigation`<br>`grep -H . "/sys/devices/system/cpu/vulnerabilities/$vulnerability"` | 读取指定 CPU 漏洞的内核缓解状态 | vulnerability: 该目录已有条目名 | 仅单个文件名；Not affected 不等于已关闭缓解；不修改启动参数 |
| `LINUX/iptables-filter`<br>`iptables -t filter -n -v -L --line-numbers` | 读取 IPv4 filter 表规则、默认策略和计数 | 目标主机 | 仅本机此表和协议族；后端可能为 nft；不代表云安全组或全部防火墙规则 |
| `LINUX/firewalld-state`<br>`firewall-cmd --state` | 读取 firewalld 运行状态 | 目标主机 | 需 firewalld；not running 的非零退出是状态，不是无防火墙规则 |
| `LINUX/firewalld-zones`<br>`firewall-cmd --get-active-zones` | 读取活动区域与接口／来源关联 | 目标主机 | 需运行中的 firewalld；区域不可默认猜 public |
| `LINUX/firewalld-rules`<br>`firewall-cmd --zone="$zone" --list-all` | 读取指定区域运行时规则 | zone: 来自 firewalld-zones 的目标区域 | 运行时与永久配置分开；区域规则不等于全局最终放行 |
