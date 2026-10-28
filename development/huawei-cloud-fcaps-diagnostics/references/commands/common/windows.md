# 共享查询 · windows

首次使用本环境或工具不匹配时读 [windows](../../tools/windows.md)。缺输入才读 [Helper](../../helpers.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WINDOWS/os`<br>`Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop` | 读取 Windows 版本和启动时间 | 目标 Windows 主机 | 需 CIM；不用管理机 OS 推断目标 OS |
| `WINDOWS/powershell`<br>`$PSVersionTable` | 读取当前 PowerShell 版本与平台 | 目标会话 | PowerShell 版本不证明所有 Windows 模块可用 |
