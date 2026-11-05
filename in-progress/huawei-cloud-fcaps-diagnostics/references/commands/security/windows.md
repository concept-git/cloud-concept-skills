# S 安全 · windows

首次使用本环境或工具不匹配时读 [windows](../../tools/windows.md)。缺输入才读 [Helper](../../helpers.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WINDOWS/firewall`<br>`Get-NetFirewallRule -PolicyStore ActiveStore -ErrorAction Stop` | 读取有效策略存储的防火墙规则 | 目标 Windows 主机 | 端口和地址条件需关联过滤器；启用规则不等于最终放行 |
| `WINDOWS/firewall-ports`<br>`Get-NetFirewallRule -Name $rule -PolicyStore ActiveStore -ErrorAction Stop \| Get-NetFirewallPortFilter -ErrorAction Stop` | 读取指定防火墙规则的端口条件 | rule: 规则 Name；来自规则查询 | 规则名按单目标解析；地址、程序等条件另查 |
| `WINDOWS/acl`<br>`Get-Acl -LiteralPath $path -ErrorAction Stop` | 读取目标对象 ACL | path: 已确认路径 | ACL 不等于所有访问机制计算后的有效权限 |
| `WINDOWS/local-users`<br>`Get-LocalUser -ErrorAction Stop` | 读取本地用户状态 | 目标 Windows 主机 | 需 LocalAccounts 模块；不等于域用户清单 |
| `WINDOWS/local-group`<br>`Get-LocalGroupMember -Group $group -ErrorAction Stop` | 读取本地组直接成员 | group: 已确认本地组名 | 需 LocalAccounts 模块；不展开所有嵌套域成员 |
| `WINDOWS/firewall-profile-state`<br>`netsh.exe advfirewall show currentprofile state` | 读取当前网络配置文件的防火墙状态 | 目标 Windows 主机 | 原生命令检查 LASTEXITCODE；不替代规则、端口和地址条件查询 |
