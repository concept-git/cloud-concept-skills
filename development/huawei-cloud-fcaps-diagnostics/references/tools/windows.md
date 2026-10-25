# Windows

- 在目标 Windows 会话检查 `$PSVersionTable` 和 `Get-Command`，再用 `Get-Help <cmdlet> -Full` 核验参数。macOS 上的 PowerShell 不证明 Windows 模块可用。
- PowerShell 使用命名参数和对象属性；原生 exe 查自身帮助并检查 `$LASTEXITCODE`，不套用 `-ErrorAction`。时间窗明确时区。`Get-Counter` 路径从目标主机发现，不硬编码英文计数器。
- 本机名、服务名、显示名、磁盘编号及 EVS ID 分别处理。错误使用 `-ErrorAction Stop`；无匹配记录与权限错误分别判断。
- 当前仅在线查询。离线挂盘、加载注册表配置单元或修复不由这些契约隐含授权。本批无 Windows 目标，所有条目保留受阻状态，首次使用必须核验。

## 契约入口

[共享查询](../commands/common/windows.md) · [C 配置](../commands/configuration/windows.md) · [F 故障](../commands/fault/windows.md) · [P 性能](../commands/performance/windows.md) · [S 安全](../commands/security/windows.md)

需远程执行时读[通道](../execution.md)；核验范围见[验证摘要](../verification/windows.md)。
