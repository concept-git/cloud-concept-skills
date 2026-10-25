# 网络配置 C

核对实际路径中的网络配置。配置正常不等于端到端可达。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[CC](hcloud-network.md#cc) · [DNS](hcloud-network.md#dns) · [EIP](hcloud-network.md#eip) · [ELB](hcloud-network.md#elb) · [ER](hcloud-network.md#er) · [NAT](hcloud-network.md#nat) · [VPC](hcloud-network.md#vpc) · [VPCEP](hcloud-network.md#vpcep) · [VPN](hcloud-network.md#vpn)

## CC

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CC/ListAuthorisations/v3` | 读取授权列表 | — | — |
| `CC/ListBandwidthPackages/v3` | 读取带宽包列表 | — | — |
| `CC/ListCentralNetworkAttachments/v3` | 读取中心网络附件列表 | `central_network_id` | — |
| `CC/ListCentralNetworkConnections/v3` | 读取中心网络连接列表 | `central_network_id` | — |
| `CC/ListCentralNetworkErRouteTableAttachments/v3` | 读取中心网络ER路由表附件列表 | `central_network_id` | — |
| `CC/ListCentralNetworkGdgwAttachments/v3` | 读取中心网络GDGW附件列表 | `central_network_id` | — |
| `CC/ListCentralNetworkPolicies/v3` | 读取所有版本的中心网络策略列表 | `central_network_id` | — |
| `CC/ListCentralNetworkPolicyChangeSet/v3` | 读取中心网络策略变化集 | `central_network_id`、`policy_id` | — |
| `CC/ListCentralNetworkQuotas/v3` | 读取中心网络配额 | — | — |
| `CC/ListCentralNetworks/v3` | 读取中心网络列表 | — | — |
| `CC/ListCloudConnectionQuotas/v3` | 读取云连接配额 | — | — |
| `CC/ListCloudConnectionRoutes/v3` | 读取云连接路由条目列表 | — | — |
| `CC/ListCloudConnections/v3` | 读取云连接列表 | — | — |
| `CC/ListGlobalConnectionBandwidthConfigs/v3` | 读取全域互联带宽租户配置信息 | — | — |
| `CC/ListGlobalConnectionBandwidths/v3` | 读取全域互联带宽列表 | — | — |
| `CC/ListInterRegionBandwidths/v3` | 读取域间带宽列表 | — | — |
| `CC/ListNetworkInstances/v3` | 读取网络实例列表 | — | — |
| `CC/ListPermissions/v3` | 读取权限列表 | — | — |
| `CC/ListSiteNetworkQuotas/v3` | 读取分支网络配额 | — | — |
| `CC/ListSiteNetworks/v3` | 读取分支网络列表 | — | — |
| `CC/ShowBandwidthPackage/v3` | 读取带宽包实例 | `id` | — |
| `CC/ShowCentralNetwork/v3` | 读取中心网络详情 | `central_network_id` | — |
| `CC/ShowCentralNetworkErRouteTableAttachment/v3` | 读取中心网络ER路由表附件详情 | `central_network_id`、`er_route_table_attachment_id` | — |
| `CC/ShowCentralNetworkGdgwAttachment/v3` | 读取中心网络GDGW附件详情 | `central_network_id`、`gdgw_attachment_id` | — |
| `CC/ShowCloudConnection/v3` | 读取云连接实例 | `id` | — |
| `CC/ShowCloudConnectionRoutes/v3` | 读取云连接路由条目详情 | `id` | — |
| `CC/ShowGlobalConnectionBandwidth/v3` | 读取全域互联带宽详情 | `id` | — |
| `CC/ShowInterRegionBandwidth/v3` | 读取域间带宽实例 | `id` | — |
| `CC/ShowNetworkInstance/v3` | 读取网络实例 | `id` | — |
| `CC/ShowSiteNetwork/v3` | 读取分支网络详情 | `site_network_id` | — |

## DNS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `DNS/ListBatchOperationTasks/v2` | 读取批量操作任务列表 | — | — |
| `DNS/ListCustomLine/v2` | 读取自定义线路 | — | — |
| `DNS/ListEndpointIpaddresses/v2` | 读取IP地址列表 | `endpoint_id` | — |
| `DNS/ListEndpointVpcs/v2` | 读取终端节点VPC列表 | — | — |
| `DNS/ListEndpoints/v2` | 读取终端节点列表 | — | — |
| `DNS/ListInstances/v2` | 读取批量查询DNS解析量统计相关的资源 | — | — |
| `DNS/ListLineGroups/v2` | 读取线路分组列表 | — | — |
| `DNS/ListNameServers/v2` | 读取名称服务器列表 | — | — |
| `DNS/ListPrivateZones/v2` | 读取内网域名列表 | — | — |
| `DNS/ListPtrRecords/v2` | 读取弹性公网IP的反向解析记录列表 | — | — |
| `DNS/ListPtrs/v2` | 读取弹性公网IP的反向解析记录列表 | — | — |
| `DNS/ListPublicZoneLines/v2` | 读取公网域名的线路列表 | `zone_id` | — |
| `DNS/ListPublicZones/v2` | 读取公网域名列表 | — | — |
| `DNS/ListRecordSets/v2` | 读取租户记录集列表 | — | — |
| `DNS/ListRecordSetsByZone/v2` | 读取域名下的记录集列表 | `zone_id` | — |
| `DNS/ListRecordSetsWithLine/v2` | 读取租户记录集列表 | — | — |
| `DNS/ListResolverQueryLogConfigs/v2` | 读取解析器访问日志列表 | — | — |
| `DNS/ListResolverRules/v2` | 读取解析器转发规则列表 | — | — |
| `DNS/ListSystemLines/v2` | 读取系统线路 | — | — |
| `DNS/ShowBatchCreateRecordSetsTask/v2` | 读取批量创建记录集任务 | `zone_id` | — |
| `DNS/ShowBatchOperationTask/v2` | 读取批量操作任务 | `task_id` | 复用已有任务标识 |
| `DNS/ShowDnssecConfig/v2` | 读取DNSSEC | `zone_id` | — |
| `DNS/ShowDomainQuota/v2` | 读取租户配额 | — | — |
| `DNS/ShowEmailRecordSet/v2` | 读取公网域名的邮箱域名 | `zone_id` | — |
| `DNS/ShowEndpoint/v2` | 读取终端节点 | `endpoint_id` | — |
| `DNS/ShowLineGroup/v2` | 读取线路分组 | `linegroup_id` | — |
| `DNS/ShowPrivateZone/v2` | 读取单个内网Zone | `zone_id` | — |
| `DNS/ShowPrivateZoneNameServer/v2` | 读取内网域名的名称服务器 | `zone_id` | — |
| `DNS/ShowPtr/v2` | 读取弹性公网IP的反向解析记录 | `ptr_id` | — |
| `DNS/ShowPtrRecordSet/v2` | 读取弹性公网IP的反向解析记录 | `floatingip_id`、`region` | — |
| `DNS/ShowPublicZone/v2` | 读取公网域名 | `zone_id` | — |
| `DNS/ShowPublicZoneNameServer/v2` | 读取公网域名的名称服务器 | `zone_id` | — |
| `DNS/ShowRecordSet/v2` | 读取记录集 | `recordset_id`、`zone_id` | — |
| `DNS/ShowRecordSetByZone/v2` | 读取域名下的记录集列表 | `zone_id` | — |
| `DNS/ShowRecordSetWithLine/v2` | 读取记录集 | `recordset_id`、`zone_id` | — |
| `DNS/ShowResolverQueryLogConfig/v2` | 读取解析器访问日志 | `id` | — |
| `DNS/ShowResolverRule/v2` | 读取解析器转发规则 | `resolverrule_id` | — |
| `DNS/ShowWebsiteRecordSet/v2` | 读取公网域名的网站域名 | `zone_id` | — |
| `DNS/ShowZoneNameServer/v2` | 读取公网域名的DNS服务器地址 | `domain_name` | — |

## EIP

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EIP/CountEipAvailableResources/v3` | 读取弹性公网IP可用数 | — | — |
| `EIP/ListBandwidth/v3` | 读取带宽列表 | — | — |
| `EIP/ListBandwidthPkg/v2` | 读取带宽加油包列表 | — | — |
| `EIP/ListBandwidthRule/v3` | 读取全量查询带宽规则列表 | `bandwidth_id: EIP.BandwidthId` | — |
| `EIP/ListBandwidths/v2` | 读取带宽列表 | — | — |
| `EIP/ListBandwidthsLimit/v3` | 读取租户带宽限制 | — | — |
| `EIP/ListEipBandwidths/v3` | 读取带宽列表 | — | — |
| `EIP/ListProjectGeipBindings/v3` | 读取GEIP与实例绑定关系的租户列表 | — | — |
| `EIP/ListPublicipPool/v3` | 读取公网IP池列表 | — | — |
| `EIP/ListPublicips/v2` | 读取弹性公网IP列表 | — | — |
| `EIP/ListPublicips/v3` | 读取全量查询弹性公网IP列表 | — | — |
| `EIP/ListQuotas/v2` | 读取配额接口 | — | — |
| `EIP/ListTenantVpcIgws/v3` | 读取指定租户下的虚拟igw列表 | — | — |
| `EIP/NeutronListFloatingIps/v2` | 读取浮动IP列表 | — | — |
| `EIP/NeutronShowFloatingIp/v2` | 读取浮动IP | `floatingip_id` | — |
| `EIP/ShowBandwidth/v2` | 读取带宽 | `bandwidth_id: EIP.BandwidthId`；缺失 → [H-eip](../../helpers.md#h-eip) | — |
| `EIP/ShowBandwidthRule/v3` | 读取带宽规则 | `bandwidth_id: EIP.BandwidthId`、`bandwidth_rules_id` | — |
| `EIP/ShowInternalVpcIgw/v3` | 读取虚拟igw详情 | `vpc_igw_id` | — |
| `EIP/ShowPublicip/v2` | 读取弹性公网IP | `publicip_id: EIP.PublicipId` | — |
| `EIP/ShowPublicip/v3` | 读取弹性公网IP详情 | `publicip_id: EIP.PublicipId`；缺失 → [H-eip](../../helpers.md#h-eip) | — |
| `EIP/ShowPublicipPool/v3` | 读取公网IP池详情 | `publicip_pool_id` | — |

## ELB

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ELB/ListAllL7Rules/v3` | 读取转发规则全局列表 | — | — |
| `ELB/ListAllMembers/v3` | 读取后端服务器全局列表 | — | — |
| `ELB/ListCertificates/v2` | 读取SSL证书列表 | — | — |
| `ELB/ListCertificates/v3` | 读取证书列表 | — | — |
| `ELB/ListDomainIPs/v3` | 读取负载均衡器IP地址的域名解析配置 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ListFeatureConfigs/v3` | 读取当前租户ELB服务的特性配置 | — | — |
| `ELB/ListFlavors/v3` | 读取规格列表 | — | — |
| `ELB/ListHealthMonitors/v2` | 读取健康检查列表 | — | — |
| `ELB/ListHealthMonitors/v3` | 读取健康检查列表 | — | — |
| `ELB/ListIpGroups/v3` | 读取IP地址组列表 | — | — |
| `ELB/ListL7Policies/v2` | 读取转发策略列表 | — | — |
| `ELB/ListL7Policies/v3` | 读取转发策略列表 | — | — |
| `ELB/ListL7Rules/v2` | 读取转发规则列表 | `l7policy_id` | — |
| `ELB/ListL7Rules/v3` | 读取转发规则列表 | `l7policy_id` | — |
| `ELB/ListListeners/v2` | 读取监听器列表 | — | — |
| `ELB/ListListeners/v3` | 读取监听器列表 | — | — |
| `ELB/ListLoadBalancers/v2` | 读取负载均衡列表 | — | — |
| `ELB/ListLoadBalancers/v3` | 读取负载均衡器列表 | — | — |
| `ELB/ListLoadbalancerFeature/v3` | 读取指定ELB实例的特性配置 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ListLogtanks/v3` | 读取云日志列表 | — | — |
| `ELB/ListMasterSlavePools/v3` | 读取主备后端服务器组列表 | — | — |
| `ELB/ListMembers/v2` | 读取后端云服务器列表 | `pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ListMembers/v3` | 读取后端服务器列表 | `pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ListPools/v2` | 读取后端云服务器组列表 | — | — |
| `ELB/ListPools/v3` | 读取后端服务器组列表 | — | — |
| `ELB/ListQuotaDetails/v3` | 读取配额使用详情 | — | — |
| `ELB/ListSecurityPolicies/v3` | 读取自定义安全策略列表 | — | — |
| `ELB/ListSystemSecurityPolicies/v3` | 读取系统安全策略列表 | — | — |
| `ELB/ListWhitelists/v2` | 读取白名单列表 | — | — |
| `ELB/ShowFlavor/v3` | 读取规格详情 | `flavor_id` | — |
| `ELB/ShowHealthMonitor/v3` | 读取健康检查详情 | `healthmonitor_id` | — |
| `ELB/ShowHealthmonitors/v2` | 读取健康检查详情 | `healthmonitor_id` | — |
| `ELB/ShowIpGroup/v3` | 读取IP地址组详情 | `ipgroup_id` | — |
| `ELB/ShowIpGroupRelatedListeners/v3` | 读取IP地址组关联的监听器列表 | `ipgroup_id` | — |
| `ELB/ShowL7Policy/v2` | 读取转发策略详情 | `l7policy_id` | — |
| `ELB/ShowL7Policy/v3` | 读取转发策略详情 | `l7policy_id` | — |
| `ELB/ShowL7Rule/v2` | 读取转发规则详情 | `l7policy_id`、`l7rule_id` | — |
| `ELB/ShowL7Rule/v3` | 读取转发规则详情 | `l7policy_id`、`l7rule_id` | — |
| `ELB/ShowListener/v2` | 读取监听器详情 | `listener_id`；缺 `listener_id` → [ELB/ListListeners/v3](hcloud-network.md#elb) | — |
| `ELB/ShowListener/v3` | 读取监听器详情 | `listener_id`；缺 `listener_id` → [ELB/ListListeners/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadBalancer/v2` | 读取负载均衡详情 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadBalancer/v3` | 读取负载均衡器详情 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadBalancerPorts/v3` | 读取负载均衡内部转发用的IP | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadBalancerStatus/v3` | 读取负载均衡器状态树 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadBalancerTopology/v3` | 读取负载均衡器拓扑 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLoadbalancersStatus/v2` | 读取负载均衡状态树 | `loadbalancer_id`；缺 `loadbalancer_id` → [ELB/ListLoadBalancers/v3](hcloud-network.md#elb) | — |
| `ELB/ShowLogtank/v3` | 读取云日志详情 | `logtank_id` | — |
| `ELB/ShowMasterSlavePool/v3` | 读取主备后端服务器组详情 | `pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ShowMember/v2` | 读取后端云服务器详情 | `member_id`、`pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ShowMember/v3` | 读取后端服务器详情 | `member_id`、`pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ShowPool/v2` | 读取后端云服务器组详情 | `pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ShowPool/v3` | 读取后端服务器组详情 | `pool_id`；缺 `pool_id` → [ELB/ListPools/v3](hcloud-network.md#elb) | — |
| `ELB/ShowQuota/v3` | 读取配额详情 | — | — |
| `ELB/ShowSecurityPolicy/v3` | 读取自定义安全策略详情 | `security_policy_id` | — |
| `ELB/ShowWhitelist/v2` | 读取白名单详情 | `whitelist_id` | — |

## ER

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ER/CreateFlowLog/v3` | 创建流日志 | `er_id`、`flow_log.log_group_id`、`flow_log.log_stream_id`、`flow_log.resource_id` | — |
| `ER/EnableFlowLog/v3` | 开启流日志 | `er_id`、`flow_log_id` | — |
| `ER/ListAssociations/v3` | 读取路由关联列表 | `er_id`、`route_table_id` | — |
| `ER/ListAttachments/v3` | 读取连接列表 | `er_id` | — |
| `ER/ListEffectiveRoutes/v3` | 读取有效路由列表 | `route_table_id` | — |
| `ER/ListEnterpriseRouters/v3` | 读取企业路由器列表 | — | — |
| `ER/ListFlowLogs/v3` | 读取流日志列表 | `er_id` | — |
| `ER/ListPropagations/v3` | 读取路由传播列表 | `er_id`、`route_table_id` | — |
| `ER/ListRouteTables/v3` | 读取路由表列表 | `er_id` | — |
| `ER/ListStaticRoutes/v3` | 读取静态路由列表 | `route_table_id` | — |
| `ER/ListVpcAttachments/v3` | 读取VPC连接列表 | `er_id` | — |
| `ER/ShowAttachment/v3` | 读取连接详情 | `attachment_id`、`er_id` | — |
| `ER/ShowEnterpriseRouter/v3` | 读取企业路由器详情 | `er_id` | — |
| `ER/ShowFlowLog/v3` | 读取流日志详情 | `er_id`、`flow_log_id` | — |
| `ER/ShowQuotas/v3` | 读取配额 | — | — |
| `ER/ShowRouteTable/v3` | 读取路由表详情 | `er_id`、`route_table_id` | — |
| `ER/ShowStaticRoute/v3` | 读取静态路由详情 | `route_id`、`route_table_id` | — |
| `ER/ShowVpcAttachment/v3` | 读取VPC连接详情 | `er_id`、`vpc_attachment_id` | — |

## NAT

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `NAT/ListNatGatewayDnatRules/v2` | 读取DNAT规则列表 | — | — |
| `NAT/ListNatGatewaySnatRules/v2` | 读取SNAT规则列表 | — | — |
| `NAT/ListNatGatewaySpecs/v2` | 读取支持创建的NAT网关规格列表 | — | — |
| `NAT/ListNatGateways/v2` | 读取公网NAT网关列表 | — | — |
| `NAT/ListPrivateDnats/v2` | 读取DNAT规则列表 | — | — |
| `NAT/ListPrivateNats/v2` | 读取私网NAT网关列表 | — | — |
| `NAT/ListPrivateSnats/v2` | 读取SNAT规则列表 | — | — |
| `NAT/ListSpecs/v2` | 读取项目支持的网关规格列表 | — | — |
| `NAT/ListTransitIps/v2` | 读取中转IP列表 | — | — |
| `NAT/ListTransitSubnet/v2` | 读取中转子网列表 | — | — |
| `NAT/ShowNatGateway/v2` | 读取指定的公网NAT网关详情 | `nat_gateway_id` | — |
| `NAT/ShowNatGatewayDnatRule/v2` | 读取指定的DNAT规则详情 | `dnat_rule_id` | — |
| `NAT/ShowNatGatewaySnatRule/v2` | 读取指定的SNAT规则详情 | `snat_rule_id` | — |
| `NAT/ShowPrivateDnat/v2` | 读取指定的DNAT规则详情 | `dnat_rule_id` | — |
| `NAT/ShowPrivateNat/v2` | 读取指定的私网NAT网关详情 | `gateway_id` | — |
| `NAT/ShowPrivateSnat/v2` | 读取指定的SNAT规则详情 | `snat_rule_id` | — |
| `NAT/ShowTransitIp/v2` | 读取指定的中转IP详情 | `transit_ip_id` | — |
| `NAT/ShowTransitSubnet/v2` | 读取指定的中转子网详情 | `transit_subnet_id` | — |

## VPC

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `VPC/CreateFlowLog/v2` | 创建流日志 | `flow_log.log_group_id`、`flow_log.log_topic_id`、`flow_log.resource_id` | — |
| `VPC/CreateTrafficMirrorSession/v3` | 创建流量镜像会话 | `traffic_mirror_session.traffic_mirror_filter_id`、`traffic_mirror_session.traffic_mirror_target_id` | — |
| `VPC/ListAddressGroup/v3` | 读取地址组列表 | — | — |
| `VPC/ListAddressGroupsDependency/v3` | 读取IP地址组的关联资源 | — | — |
| `VPC/ListFirewall/v3` | 读取网络ACL列表 | — | — |
| `VPC/ListFlowLogs/v2` | 读取流日志列表 | — | — |
| `VPC/ListPorts/v2` | 读取端口列表 | — | — |
| `VPC/ListPorts/v3` | 读取端口列表 | — | — |
| `VPC/ListPrivateips/v2` | 读取私有IP列表 | `subnet_id` | — |
| `VPC/ListRouteTables/v2` | 读取路由表列表 | — | — |
| `VPC/ListSecurityGroupRules/v2` | 读取安全组规则列表 | — | — |
| `VPC/ListSecurityGroupRules/v3` | 读取安全组规则列表 | 目标端口或已有配置中的 `VPC.SecurityGroupId` | 按安全组 ID 筛选 |
| `VPC/ListSecurityGroups/v2` | 读取安全组列表 | — | — |
| `VPC/ListSecurityGroups/v3` | 读取安全组列表 | — | — |
| `VPC/ListSubNetworkInterfaces/v3` | 读取租户下辅助弹性网卡列表 | — | — |
| `VPC/ListSubnets/v2` | 读取子网列表 | 已知 `vpc_id: VPC.VpcId` 时按该值筛选 | — |
| `VPC/ListTrafficMirrorFilterRules/v3` | 读取流量镜像筛选规则列表 | — | — |
| `VPC/ListTrafficMirrorFilters/v3` | 读取流量镜像筛选条件列表 | — | — |
| `VPC/ListTrafficMirrorSessions/v3` | 读取流量镜像会话列表 | — | — |
| `VPC/ListVirsubnetCidrReservations/v3` | 读取子网预留网段列表 | — | — |
| `VPC/ListVirsubnets/v3` | 读取虚拟子网列表 | — | — |
| `VPC/ListVpcPeerings/v2` | 读取对等连接列表 | — | — |
| `VPC/ListVpcRoutes/v2` | 读取VPC路由列表 | — | — |
| `VPC/ListVpcs/v2` | 读取VPC列表 | — | — |
| `VPC/ListVpcs/v3` | 读取VPC列表 | — | — |
| `VPC/NeutronListFirewallGroups/v2` | 读取所有网络ACL组 | — | — |
| `VPC/NeutronListFirewallPolicies/v2` | 读取所有网络ACL策略 | — | — |
| `VPC/NeutronListFirewallRules/v2` | 读取所有网络ACL规则 | — | — |
| `VPC/NeutronListNetworks/v2` | 读取网络列表 | — | — |
| `VPC/NeutronListPorts/v2` | 读取端口列表 | — | — |
| `VPC/NeutronListRouters/v2` | 读取路由器列表 | — | — |
| `VPC/NeutronListSecurityGroupRules/v2` | 读取安全组规则列表 | — | — |
| `VPC/NeutronListSecurityGroups/v2` | 读取安全组列表 | — | — |
| `VPC/NeutronListSubnets/v2` | 读取子网列表 | — | — |
| `VPC/NeutronShowFirewallGroup/v2` | 读取特定网络ACL组详情 | `firewall_group_id` | — |
| `VPC/NeutronShowFirewallPolicy/v2` | 读取特定网络ACL策略详情 | `firewall_policy_id` | — |
| `VPC/NeutronShowFirewallRule/v2` | 读取特定网络ACL规则 | `firewall_rule_id` | — |
| `VPC/NeutronShowNetwork/v2` | 读取网络 | `network_id` | — |
| `VPC/NeutronShowPort/v2` | 读取端口 | `port_id` | — |
| `VPC/NeutronShowRouter/v2` | 读取路由器 | `router_id` | — |
| `VPC/NeutronShowSecurityGroup/v2` | 读取安全组 | `security_group_id: VPC.SecurityGroupId`；缺 `security_group_id` → [VPC/ListSecurityGroups/v3](hcloud-network.md#vpc) | — |
| `VPC/NeutronShowSecurityGroupRule/v2` | 读取安全组规则 | `security_group_rule_id: VPC.SecurityGroupRuleId`；缺 `security_group_rule_id` → [VPC/ListSecurityGroupRules/v3](hcloud-network.md#vpc) | — |
| `VPC/NeutronShowSubnet/v2` | 读取子网 | `subnet_id` | — |
| `VPC/ShowAddressGroup/v3` | 读取地址组 | `address_group_id` | — |
| `VPC/ShowFirewall/v3` | 读取网络ACL详情 | `firewall_id` | — |
| `VPC/ShowFlowLog/v2` | 读取流日志 | `flowlog_id` | — |
| `VPC/ShowNetworkIpAvailabilities/v2` | 读取网络IP使用情况 | `network_id` | — |
| `VPC/ShowPort/v2` | 读取端口 | `port_id: VPC.PortId`；缺失 → [H-port](../../helpers.md#h-port) | — |
| `VPC/ShowPort/v3` | 读取端口详情 | `port_id: VPC.PortId`；缺失 → [H-port](../../helpers.md#h-port) | — |
| `VPC/ShowPrivateip/v2` | 读取私有IP | `privateip_id` | — |
| `VPC/ShowQuota/v2` | 读取配额 | — | — |
| `VPC/ShowQuota/v3` | 读取配额 | — | — |
| `VPC/ShowRouteTable/v2` | 读取路由表 | `routetable_id`；缺 `routetable_id` → [VPC/ListRouteTables/v2](hcloud-network.md#vpc) | — |
| `VPC/ShowSecurityGroup/v2` | 读取安全组 | `security_group_id: VPC.SecurityGroupId`；缺 `security_group_id` → [VPC/ListSecurityGroups/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowSecurityGroup/v3` | 读取安全组 | `security_group_id: VPC.SecurityGroupId`；缺 `security_group_id` → [VPC/ListSecurityGroups/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowSecurityGroupRule/v2` | 读取安全组规则 | `security_group_rule_id: VPC.SecurityGroupRuleId`；缺 `security_group_rule_id` → [VPC/ListSecurityGroupRules/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowSecurityGroupRule/v3` | 读取安全组规则 | `security_group_rule_id: VPC.SecurityGroupRuleId`；缺 `security_group_rule_id` → [VPC/ListSecurityGroupRules/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowSubNetworkInterface/v3` | 读取租户下辅助弹性网卡 | `sub_network_interface_id` | — |
| `VPC/ShowSubNetworkInterfacesQuantity/v3` | 读取租户下辅助弹性网卡数目 | — | — |
| `VPC/ShowSubnet/v2` | 读取子网 | `subnet_id: VPC.SubnetId`；缺失 → [H-subnet](../../helpers.md#h-subnet) | 不直接使用 Neutron 子网 ID |
| `VPC/ShowTrafficMirrorFilter/v3` | 读取流量镜像筛选条件详情 | `traffic_mirror_filter_id` | — |
| `VPC/ShowTrafficMirrorFilterRule/v3` | 读取流量镜像筛选规则详情 | `traffic_mirror_filter_rule_id` | — |
| `VPC/ShowTrafficMirrorSession/v3` | 读取流量镜像会话详情 | `traffic_mirror_session_id` | — |
| `VPC/ShowVirsubnet/v3` | 读取虚拟子网详情 | `virsubnet_id` | — |
| `VPC/ShowVirsubnetCidrReservation/v3` | 读取子网预留网段 | `virsubnet_cidr_reservation_id` | — |
| `VPC/ShowVpc/v2` | 读取VPC | `vpc_id: VPC.VpcId`；缺 `vpc_id` → [VPC/ListVpcs/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowVpc/v3` | 读取VPC详情 | `vpc_id: VPC.VpcId`；缺 `vpc_id` → [VPC/ListVpcs/v3](hcloud-network.md#vpc) | — |
| `VPC/ShowVpcPeering/v2` | 读取对等连接 | `peering_id` | — |
| `VPC/ShowVpcRoute/v2` | 读取VPC路由 | `route_id` | — |
| `VPC/UpdateFlowLog/v2` | 更新流日志 | `flowlog_id` | — |

## VPCEP

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `VPCEP/ListEndpointInfoDetails/v1` | 读取终端节点详情 | `vpc_endpoint_id` | — |
| `VPCEP/ListEndpointService/v1` | 读取终端节点服务列表 | — | — |
| `VPCEP/ListEndpoints/v1` | 读取终端节点列表 | — | — |
| `VPCEP/ListQuotaDetails/v1` | 读取配额 | — | — |
| `VPCEP/ListServiceConnections/v1` | 读取连接终端节点服务的连接列表 | `vpc_endpoint_service_id` | — |
| `VPCEP/ListServiceDescribeDetails/v1` | 读取终端节点服务概要 | — | — |
| `VPCEP/ListServiceDetails/v1` | 读取终端节点服务详情 | `vpc_endpoint_service_id` | — |
| `VPCEP/ListServicePermissionsDetails/v1` | 读取终端节点服务的白名单列表 | `vpc_endpoint_service_id` | — |
| `VPCEP/ListServicePublicDetails/v1` | 读取公共终端节点服务列表 | — | — |

## VPN

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `VPN/ListCgws/v5` | 读取对端网关列表 | — | — |
| `VPN/ListConnectionIpsecSa/v5` | 读取VPN连接网段协商信息 | `vpn_connection_id` | — |
| `VPN/ListP2cVgwConnections/v5` | 读取P2C VPN网关连接信息列表 | `p2c_vgw_id` | — |
| `VPN/ListP2cVgws/v5` | 读取P2C VPN网关列表 | — | — |
| `VPN/ListVgws/v5` | 读取VPN网关列表 | — | KooCLI 7.2.12 帮助没有 `limit` 参数 |
| `VPN/ListVpnAccessPolicies/v5` | 读取VPN访问策略列表 | `vpn_server_id` | — |
| `VPN/ListVpnConnections/v5` | 读取VPN连接列表 | — | — |
| `VPN/ListVpnServersByProject/v5` | 读取租户下的所有服务端信息 | — | — |
| `VPN/ListVpnServersByVgw/v5` | 读取一个网关下的服务端信息 | `p2c_vgw_id` | — |
| `VPN/ShowCgw/v5` | 读取对端网关 | `customer_gateway_id` | — |
| `VPN/ShowP2cVgw/v5` | 读取P2C VPN网关 | `p2c_vgw_id` | — |
| `VPN/ShowQuotasInfo/v5` | 读取指定租户配额 | — | — |
| `VPN/ShowVgw/v5` | 读取VPN网关 | `vgw_id` | — |
| `VPN/ShowVpnAccessPolicy/v5` | 读取VPN访问策略 | `policy_id`、`vpn_server_id` | — |
| `VPN/ShowVpnConnection/v5` | 读取VPN连接 | `vpn_connection_id` | — |
| `VPN/ShowVpnConnectionLog/v5` | 读取VPN连接日志 | `vpn_connection_id` | — |
| `VPN/ShowVpnConnectionsLogConfig/v5` | 读取VPN连接日志配置 | `p2c_vgw_id` | — |
| `VPN/ShowVpnGatewayRoutingTable/v5` | 读取VPN网关路由表 | `vgw_id` | — |
