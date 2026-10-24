# Helper

只补齐缺少的标识。类型用于区分资源，不是 CLI 参数。多项匹配时按目标选择；无法唯一确定时先澄清目标。

## H-port

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| `server_id: ECS.ServerId` | [ECS/ListServerInterfaces/v2](commands/configuration/hcloud.md#ecs) | 按目标 IP 或 MAC 选择网卡 | `interfaceAttachments[].port_id` → `VPC.PortId` |
| `port_id: VPC.PortId` | [VPC/ShowPort/v3](commands/configuration/hcloud-network.md#vpc) | 返回端口 ID 与请求一致 | `port.security_groups[]` → `VPC.SecurityGroupId` |

## H-subnet

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| 网卡 `fixed_ips[].subnet_id: Neutron.SubnetId`、目标 `VPC.VpcId` | [VPC/ListSubnets/v2](commands/configuration/hcloud-network.md#vpc) | 按目标 VPC 筛选；`subnets[].neutron_subnet_id` 等于网卡子网 ID | 同项 `subnets[].id` → `VPC.SubnetId`，用于 [VPC/ShowSubnet/v2](commands/configuration/hcloud-network.md#vpc) |

## H-volume

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| `server_id: ECS.ServerId` | [ECS/ShowServer/v2](commands/configuration/hcloud.md#ecs) | 确认目标系统盘或数据盘；多盘时按目标选择 | `server["os-extended-volumes:volumes_attached"][].id` → `EVS.VolumeId`，用于 [EVS/ShowVolume/v2](commands/configuration/hcloud.md#evs) |

## H-eip

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| `port_id: VPC.PortId` | [EIP/ListPublicips/v2](commands/configuration/hcloud-network.md#eip) | `publicips[].port_id` 等于目标端口 ID | 同项 `id` → `EIP.PublicipId`；同项 `bandwidth_id` → `EIP.BandwidthId` |

公网 IP 用于 [EIP/ShowPublicip/v3](commands/configuration/hcloud-network.md#eip)，带宽用于 [EIP/ShowBandwidth/v2](commands/configuration/hcloud-network.md#eip)。绑定关系不证明公网服务可达。

需要确认这些衔接的实测范围时，读[验证记录](verification/cloud.md)。

## H-unit

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| 目标服务用途或已知进程 | [LINUX/units](commands/configuration/linux.md) | 按目标服务核对单元名；多项匹配不默认取首项 | 单元名称 → Linux.UnitName |

## H-interface

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| 目标实例网卡 MAC／IP | [ECS/ListServerInterfaces/v2](commands/configuration/hcloud.md#ecs)、[LINUX/addresses](commands/configuration/linux.md) | 同一实例；按 MAC 比对，IP 辅助核验；唯一匹配才绑定 | Linux 接口 ifname → Linux.InterfaceName |

## H-device

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| 已确认实例及 EVS.VolumeId | [ECS/ListServerBlockDevices/v2](commands/configuration/hcloud.md#ecs)、[LINUX/udev-device](commands/configuration/linux.md)、[LINUX/disk-by-id](commands/configuration/linux.md) | 同一实例；云端 volumeId 匹配目标，bus=virtio；按下述 VBD 分支比对且唯一 | DEVNAME → Linux.BlockDevice；分区由父盘关系另选 |

- 已核验分支：VBD／virtio。保留 UUID 连字符，取 volumeId 前 20 字符，与整盘的 ID_SERIAL 严格相等；该前缀在实例全部挂载盘中必须唯一。
- 主机 DEVTYPE 必须为 disk，设备父链须包含 virtio。云端 pciAddress 非空时，与主机 PCI 路径再核对；by-id 链接只作辅助，分区链接不能充当整盘。
- SCSI／WWN、XEN、缺字段、前缀冲突或多匹配保持未解析；不按容量、设备顺序或文件系统 UUID 猜测。克隆文件系统可拥有相同 UUID。
- 依据：[华为云磁盘映射说明](https://support.huaweicloud.com/ecs_faq/zh-cn_topic_0103285575.html)。本分支的实际覆盖见 [Linux 验证](verification/linux.md)。

## H-win-service

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| 已确认服务用途或显示名 | [WINDOWS/services](commands/configuration/windows.md) | 核对 Name 与 DisplayName；唯一匹配后选择 | Name → Windows.ServiceName |

## H-pod

| 输入 | 获取命令 | 选择条件 | 输出绑定 |
| --- | --- | --- | --- |
| context、namespace、目标工作负载 | [KUBERNETES/pods](commands/configuration/kubernetes.md) | 按 ownerReferences、标签与目标名称定位；多副本显式选择 | metadata.name／uid、spec.containers[].name → Pod 名／UID／容器名 |
