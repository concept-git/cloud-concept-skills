# Linux

- 在目标主机读取 OS 和内核；工具存在不代表选项兼容。查 `command -v`、所选工具帮助及版本。
- systemd、procps、iproute2、util-linux、sysstat 分别核验；缺工具记录缺口，不自动安装。RPM 与 Debian 查询分支按发行版选择。
- `$unit`、`$iface`、`$pid`、`$path` 均属于当前主机。PID 可重用；云盘 ID 不等于设备名。采样必须有次数或时限。
- 本机或 SSH 查询须确认目标主机、账号、端口和主机密钥；在目标内执行并保留退出状态与错误。历史实测仅覆盖 Ubuntu 24.04，其他发行版需重新核验。

## 契约入口

[共享查询](../commands/common/linux.md) · [C 配置](../commands/configuration/linux.md) · [F 故障](../commands/fault/linux.md) · [P 性能](../commands/performance/linux.md) · [S 安全](../commands/security/linux.md)
