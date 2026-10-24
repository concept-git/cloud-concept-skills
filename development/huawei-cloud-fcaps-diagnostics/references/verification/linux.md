# linux 验证

范围：Huawei ECS / Ubuntu 24.04.4 LTS / root；不外推其他发行版。

帮助与运行分开。受阻、未执行和空结果不是取得完整数据。按 ID 查所需行；[返回地图](../commands/index.md)。

| 命令 ID | 帮助 | 运行 | 日期 | 边界 |
| --- | --- | --- | --- | --- |
| `LINUX/os-release` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/kernel` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/identity` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/units` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/block-devices` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/mounts` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/addresses` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/routes` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/rules` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/modules` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/timers` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/connections` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/disk-by-id` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/udev-device` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/filesystem-id` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/partition-table` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/kernel-setting` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/service-enabled` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/network-manager` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/chrony-sources` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |
| `LINUX/ntp-peers` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |
| `LINUX/service-status` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/unit-journal` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/kernel-journal` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/kernel-ring` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/dns-query` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/icmp-probe` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/mtr-report` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/trace-route` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |
| `LINUX/deleted-open-files` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/metadata-http` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/process-snapshot` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/memory` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/vm-sample` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/disk-sample` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/process-io` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/cpu-sample` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/filesystem-space` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/filesystem-inodes` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/nic-statistics` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/driver-statistics` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/packet-capture` | 通过 | 未执行 | 2026-10-22 | 有条件采集或扫描；未执行业务操作 |
| `LINUX/syscall-trace` | 通过 | 未执行 | 2026-10-22 | 有条件采集或扫描；未执行业务操作 |
| `LINUX/perf-sample` | 通过 | 未执行 | 2026-10-22 | 有条件采集或扫描；未执行业务操作 |
| `LINUX/directory-usage` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/run-queue` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/thread-inventory` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/conntrack-capacity` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/recent-logins` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/failed-logins` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/cron` | 通过 | 成功空结果 | 2026-10-22 | 仅本次范围为空 |
| `LINUX/rpm-verify` | 工具缺失 | 未执行 | 2026-10-22 | 有条件采集或扫描；未执行业务操作 |
| `LINUX/deb-verify` | 工具缺失 | 未执行 | 2026-10-22 | 有条件采集或扫描；未执行业务操作 |
| `LINUX/cpu-mitigation` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/iptables-filter` | 通过 | 取得数据 | 2026-10-22 | 仅上述环境与参数 |
| `LINUX/firewalld-state` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |
| `LINUX/firewalld-zones` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |
| `LINUX/firewalld-rules` | 工具缺失 | 受阻 | 2026-10-22 | 缺依赖或权限；见本地证据 |

## H-device

2026-10-22：当前 ECS 的 virtio/VBD 整盘按序列号前缀、实例内唯一性及 PCI 地址验证通过。SCSI、WWN、XEN 和其他环境未验证。
