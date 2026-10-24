# 华为云文档指引

只定位依据，不复制原文步骤或命令。读取规则见[文档入口](index.md)。按条件选择下列主题；未覆盖时搜索[元数据索引](catalog.jsonl)。OS、地域和版本是适用条件；跨类别主题共用同一来源。

## F 故障

| 读取条件 | 官方文档 | 关联契约 |
| --- | --- | --- |
| Linux 网络探测出现无应答、时延或丢包，需要解释逐跳结果 | [链路测试](https://support.huaweicloud.com/trouble-ecs/zh-cn_topic_0191526703.md) | [LINUX/icmp-probe](../commands/fault/linux.md)、[LINUX/mtr-report](../commands/fault/linux.md) |
| Linux 磁盘空间不足，df 与目录占用不一致 | [磁盘空间不足](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_1552.md) | [LINUX/deleted-open-files](../commands/fault/linux.md)、[LINUX/directory-usage](../commands/performance/linux.md) |
| Windows 无法取得元数据，需检查目标路由 | [Windows 元数据访问](https://support.huaweicloud.com/ecs_faq/ecs_faq_1322.md) | [WINDOWS/routes](../commands/configuration/windows.md) |
| ECS API 报错，或实例状态与异步任务结果不一致 | [错误码](https://support.huaweicloud.com/api-ecs/ecs_07_0002.html)、[实例状态](https://support.huaweicloud.com/api-ecs/ecs_08_0002.html) | [ECS/ShowJob/v2](../commands/fault/hcloud.md)、[ECS/ShowServer/v2](../commands/configuration/hcloud.md) |
| 需解释 LTS 日志检索语法或索引条件 | [管道符方式搜索](https://support.huaweicloud.com/usermanual-lts/lts_07_0086.html) | [日志查询](../commands/common/hcloud.md#lts)；先核对当前搜索方式，控制台语法不直接当 API 参数 |
| 需使用 COC 的 ECS 深度诊断 | [ECS 诊断条件](https://support.huaweicloud.com/usermanual-coc/coc_um_06_08_01.html) | [COC 契约](../commands/fault/hcloud.md#coc)；先核对 OS、UniAgent 版本及插件安装、采集影响 |
| 已使用独享型 ELB，后端健康检查异常 | [健康检查排查（国际站）](https://support.huaweicloud.com/intl/zh-cn/elb_faq/zh-cn_topic_0018127975.html) | [ELB 配置](../commands/configuration/hcloud-network.md#elb)；核对目标站点和产品类型 |
| 目标为 CCE，节点异常或状态 Unknown | [节点异常排查](https://support.huaweicloud.com/cce_faq/cce_faq_00468.html) | [Kubernetes 故障观测](../commands/fault/kubernetes.md)；本地 kind 验证不代表 CCE 通过 |
| 拟用 CBR 云硬盘备份恢复数据，需要核对影响 | [云硬盘恢复边界](https://support.huaweicloud.com/usermanual-cbr/cbr_03_0033.html) | [备份清单](../commands/configuration/hcloud.md#cbr)；核对停机、解除挂载和数据覆盖影响；执行须有恢复授权 |

## C 配置

| 读取条件 | 官方文档 | 关联契约 |
| --- | --- | --- |
| 云盘标识与主机设备无法对应，需要区分虚拟化或设备类型 | [磁盘映射](https://support.huaweicloud.com/ecs_faq/zh-cn_topic_0103285575.md) | [H-device](../helpers.md#h-device)、[LINUX/udev-device](../commands/configuration/linux.md) |
| CentOS 7 重启后 DHCP 或 NetworkManager 状态异常 | [dhclient 未运行](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0313.md) | [LINUX/network-manager](../commands/configuration/linux.md)、[LINUX/service-enabled](../commands/configuration/linux.md) |
| Windows virtio 网卡异常，需要核对驱动版本是否适用 | [网卡驱动场景](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0278.md) | [WINDOWS/signed-drivers](../commands/configuration/windows.md) |
| 需解释安全组连接跟踪或 VPC 流日志状态 | [安全组规则](https://support.huaweicloud.com/usermanual-vpc/zh-cn_topic_0073379079.html)、[流日志](https://support.huaweicloud.com/usermanual-vpc/FlowLog_0002.html) | [VPC 配置](../commands/configuration/hcloud-network.md#vpc)；NODATA 结合采集类型解释 |
| 已使用 DNS，解析结果与记录集不一致 | [解析生效测试](https://support.huaweicloud.com/dns_faq/dns_faq_015.html) | [DNS 配置](../commands/configuration/hcloud-network.md#dns)；区分权威结果、本地缓存及 TTL |

## A 计量计费

| 读取条件 | 官方文档 | 关联契约 |
| --- | --- | --- |
| 需要解释包年包月与按需计费的区别 | [计费模式](https://support.huaweicloud.com/ecs_faq/ecs_faq_0308.md) | [计量计费命令分册](../commands/accounting/hcloud.md)；金额以实际账单为准 |
| 实例故障后需要解释是否继续计费 | [故障状态计费](https://support.huaweicloud.com/ecs_faq/ecs_faq_2308.md) | [计量计费命令分册](../commands/accounting/hcloud.md)；先核对计费模式 |
| 需将资源与实际账单对应 | [按资源名称或 ID 查账单](https://support.huaweicloud.com/billing_faq/billing_faq_5100079.html) | [计量计费契约](../commands/accounting/hcloud.md)；资源 ID 与账期共同限定查询 |

## P 性能

| 读取条件 | 官方文档 | 关联契约 |
| --- | --- | --- |
| Linux 磁盘 I/O 高，需要区分设备和进程采样 | [I/O 负载](https://support.huaweicloud.com/ecs_faq/ecs_faq_2607.md) | [LINUX/disk-sample](../commands/performance/linux.md)、[LINUX/process-io](../commands/performance/linux.md) |
| Linux 报 Cannot allocate memory，但常规内存统计不足以解释 | [分配内存失败场景](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0372.md) | [LINUX/thread-inventory](../commands/performance/linux.md)、[LINUX/run-queue](../commands/performance/linux.md)；原文原因不是当前根因 |
| 日志含连接跟踪表满，需解释容量与丢包关系 | [连接跟踪场景](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0324.md) | [LINUX/conntrack-capacity](../commands/performance/linux.md) |
| 内核更新后性能变化，怀疑与 CPU 缓解措施有关 | [内核性能变化](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_1790.md) | [LINUX/cpu-mitigation](../commands/security/linux.md)；读取状态不授权关闭缓解 |
| CES 指标与主机采样不一致，或缺少指标 | [Agent 指标口径](https://support.huaweicloud.com/ces_faq/ces_faq_2513.html) | [CES 指标查询](../commands/performance/hcloud.md#ces)；核对 OS、Agent 版本、单位及采样周期 |
| 需判断云盘 IOPS、吞吐量或时延是否异常 | [EVS 类型与性能](https://support.huaweicloud.com/productdesc-evs/zh-cn_topic_0014580744.html) | [EVS 配置](../commands/configuration/hcloud.md#evs)、[主机 I/O](../commands/performance/linux.md)；按目标规格核对限制 |
| 已绑定 EIP，公网卡顿或丢包疑似带宽超限 | [EIP 事件说明](https://support.huaweicloud.com/usermanual-eip/monitor_0007.html) | [EIP 配置](../commands/configuration/hcloud-network.md#eip)、[CES 指标](../commands/performance/hcloud.md#ces)；核对事件与指标的统计口径 |

## S 安全

| 读取条件 | 官方文档 | 关联契约 |
| --- | --- | --- |
| 需要解释 Linux 防火墙运行状态、区域和端口规则 | [防火墙场景](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0402.md) | [LINUX/firewalld-state](../commands/security/linux.md)、[LINUX/firewalld-rules](../commands/security/linux.md)；只选查询模式 |
| 需追溯资源变更，或 CTS 查不到预期事件 | [事件缺失排查](https://support.huaweicloud.com/cts_faq/cts_faq_0918.html)、[账号事件查询](https://support.huaweicloud.com/usermanual-cts/cts_03_5121.html) | [CTS/ListTraces/v3](../commands/common/hcloud.md)；高级查询另核对开通与索引条件 |
| 鉴权失败或授权后仍不能查看目标资源 | [IAM 权限排查](https://support.huaweicloud.com/iam_faq/iam_01_0609.html) | [IAM 发现](../commands/common/hcloud.md#iam)；核对授权范围与当前身份 |
| HSS Agent、主机防护与风险结果看似矛盾 | [主机防护状态](https://support.huaweicloud.com/usermanual-hss2.0/hss_01_0003.html) | [HSS/ListHostStatus/v5](../commands/security/hcloud-host.md)；未检测不等于无风险 |

CPU 缓解状态与性能的关联共用 [P 性能](#p-性能) 中的文档。CCE 指引仅用于 CCE；其他 Kubernetes 环境使用对应平台来源。
