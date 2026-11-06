# 安全 S

核对访问控制和安全结果。规则配置与实际命中证据分别判断。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[AAD](hcloud.md#aad) · [Anti-DDoS](hcloud.md#anti-ddos) · [BSS](hcloud.md#bss) · [CFW](hcloud.md#cfw) · [Config](hcloud.md#config) · [IAM](hcloud.md#iam) · [IAMAccessAnalyzer](hcloud.md#iamaccessanalyzer) · [RMS](hcloud.md#rms) · [SecMaster](hcloud.md#secmaster) · [WAF](hcloud.md#waf)

## AAD

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `AAD/ListBlockIps/v1` | 读取租户封堵列表 | — | — |
| `AAD/ListDDoSAttackEvent/v2` | 读取DDoS攻击事件列表 | `instance_id` | — |
| `AAD/ListDDoSBlackHoleEvent/v2` | 读取黑洞事件列表 | — | — |
| `AAD/ListDDoSConnectionNumber/v2` | 读取新建连接数和并发连接数 | `instance_id` | — |
| `AAD/ListDDoSFlow/v2` | 读取DDoS攻击防护BPS/PPS流量 | `instance_id` | — |
| `AAD/ListDomain/v1` | 读取域名列表 | — | — |
| `AAD/ListFrequencyControlRule/v2` | 读取频率控制规则列表 | — | — |
| `AAD/ListInstance/v1` | 读取高防实例列表 | — | — |
| `AAD/ListInstanceDomains/v2` | 读取实例关联的域名信息 | `instance_id` | — |
| `AAD/ListInstanceId/v1` | 读取域名关联的实例ID | — | — |
| `AAD/ListInstanceIpRule/v1` | 读取高防实例IP的转发规则列表 | `instance_id`、`ip` | — |
| `AAD/ListPackage/v1` | 读取实例列表 | — | — |
| `AAD/ListPeak/v1` | 读取流量峰值、攻击计数 | `instance_id`、`ip` | — |
| `AAD/ListPolicy/v1` | 读取策略列表 | — | — |
| `AAD/ListProtectedIp/v1` | 读取防护对象列表 | — | — |
| `AAD/ListSourceIp/v2` | 读取回源ip列表 | — | — |
| `AAD/ListSourceIps/v1` | 读取高防回源IP段列表 | — | — |
| `AAD/ListUnblockQuotaStatistics/v1` | 读取解封配额 | — | — |
| `AAD/ListWafAttackEvent/v2` | 读取攻击事件列表 | — | — |
| `AAD/ListWafBandwidth/v2` | 读取带宽曲线 | — | — |
| `AAD/ListWafCustomRule/v2` | 读取精准防护规则 | — | — |
| `AAD/ListWafGeoIpRule/v2` | 读取区域封禁规则 | — | — |
| `AAD/ListWafQps/v2` | 读取请求QPS | — | — |
| `AAD/ListWafWhiteIpRule/v2` | 读取防护策略web-cc黑白名单-查询黑白名单规则 | — | — |
| `AAD/ListWhiteBlackIpRule/v2` | 读取DDoS攻击防护的黑白名单列表 | `instance_id` | — |
| `AAD/ShowBlockStatistics/v1` | 读取封堵统计数据 | — | — |
| `AAD/ShowDDoSPeak/v2` | 读取高防入流量峰值、攻击流量峰值、DDoS攻击次数 | `instance_id` | — |
| `AAD/ShowDomainDetail/v2` | 读取域名详情 | — | — |
| `AAD/ShowDomainNameConfig/v2` | 读取域名配置 | — | — |
| `AAD/ShowFlowBlock/v2` | 读取流量封禁信息 | `instance_id` | — |
| `AAD/ShowInstanceByInstanceId/v2` | 读取实例详情 | `instance_id` | — |
| `AAD/ShowLtsConfig/v1` | 读取日志配置 | — | — |
| `AAD/ShowPolicy/v1` | 读取策略详情 | `policy_id` | — |
| `AAD/ShowUnblockRecord/v1` | 读取租户解封记录 | — | — |
| `AAD/ShowWafPolicy/v2` | 读取WEB防护策略配置 | — | — |
| `AAD/ShowWafQps/v2` | 读取CC攻击防护请求QPS | — | — |

## Anti-DDoS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `Anti-DDoS/ListDDosStatus/v1` | 读取EIP防护状态列表 | — | — |
| `Anti-DDoS/ListDDosStatus/v2` | 读取EIP防护状态列表 | — | — |
| `Anti-DDoS/ListDailyLog/v1` | 读取指定EIP异常事件 | `floating_ip_id` | — |
| `Anti-DDoS/ListDailyReport/v1` | 读取指定EIP防护流量 | `floating_ip_id` | — |
| `Anti-DDoS/ListQuota/v1` | 读取配额 | — | — |
| `Anti-DDoS/ListWeeklyReports/v1` | 读取周防护统计情况 | — | — |
| `Anti-DDoS/ShowAlertConfig/v2` | 读取告警配置信息 | — | — |
| `Anti-DDoS/ShowDDos/v1` | 读取Anti-DDoS服务 | `floating_ip_id` | — |
| `Anti-DDoS/ShowDDosStatus/v1` | 读取指定EIP防护状态 | `floating_ip_id` | — |
| `Anti-DDoS/ShowDefaultConfig/v1` | 读取Ani-DDoS默认防护策略 | — | — |
| `Anti-DDoS/ShowLogConfig/v1` | 读取全量日志设置 | `enterprise_project_id` | — |
| `Anti-DDoS/ShowNewTaskStatus/v2` | 读取Anti-DDoS任务 | `task_id` | 复用已有任务标识 |

## BSS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `BSS/ShowRealNameAuthStatus/v2` | 读取实名认证状态 | — | — |

## CFW

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CFW/CreateCaptureTask/v1` | 创建抓包任务 | `fw_instance_id` | — |
| `CFW/ListAccessControlLogs/v1` | 读取访问控制日志 | `fw_instance_id` | — |
| `CFW/ListAclRuleHitCount/v1` | 读取规则击中次数 | — | — |
| `CFW/ListAclRuleHitStatus/v1` | 读取规则的命中次数和最后一次命中时间 | `fw_instance_id` | — |
| `CFW/ListAclRules/v1` | 读取防护规则 | `object_id` | — |
| `CFW/ListAddressItems/v1` | 读取地址组成员 | `set_id` | — |
| `CFW/ListAddressSetDetail/v1` | 读取地址组详细信息 | `set_id` | — |
| `CFW/ListAddressSets/v1` | 读取地址组列表 | `object_id` | — |
| `CFW/ListAdvancedIpsRules/v1` | 读取频率IPS规则信息 | `object_id` | — |
| `CFW/ListAlarmWhitelist/v1` | 读取EIP告警白名单 | `fw_instance_id` | — |
| `CFW/ListAttackLogs/v1` | 读取攻击日志 | `fw_instance_id` | — |
| `CFW/ListAttackStatistic/v1` | 读取攻击统计 | `fw_instance_id` | — |
| `CFW/ListBlackWhiteLists/v1` | 读取黑白名单列表 | `object_id` | — |
| `CFW/ListCaptureResult/v1` | 读取抓包任务结果 | `fw_instance_id`、`task_id` | 复用已有任务标识 |
| `CFW/ListCaptureTask/v1` | 读取抓包任务 | `fw_instance_id` | — |
| `CFW/ListCustomerIps/v1` | 读取自定义IPS规则列表 | `fw_instance_id` | — |
| `CFW/ListDnsServers/v1` | 读取DNS服务器列表 | — | — |
| `CFW/ListDomainParseDetail/v1` | 读取域名解析IP地址 | `domain_name` | — |
| `CFW/ListDomainParseIp/v1` | 读取域名地址解析结果 | `domain_address_id`、`domain_set_id`、`fw_instance_id` | — |
| `CFW/ListDomainResolveIp/v1` | 读取域名解析结果 | `domain_address_id`、`fw_instance_id` | — |
| `CFW/ListDomainSets/v1` | 读取域名组列表 | `fw_instance_id`、`object_id` | — |
| `CFW/ListDomains/v1` | 读取域名组下域名列表 | `domain_set_id`、`fw_instance_id` | — |
| `CFW/ListEastWestFirewall/v1` | 读取东西向防火墙信息 | `fw_instance_id` | — |
| `CFW/ListEipCount/v1` | 读取EIP数量 | `object_id` | — |
| `CFW/ListEips/v1` | 读取 EIP；可触发同步 | — | 只查询已有数据时用 `sync=0`；1 同步租户 EIP |
| `CFW/ListFirewallDetail/v1` | 读取防火墙详细信息 | — | — |
| `CFW/ListFirewallList/v1` | 读取防火墙列表 | — | — |
| `CFW/ListFlowLogs/v1` | 读取流日志 | `fw_instance_id` | — |
| `CFW/ListFlowStatistic/v1` | 读取流量日志统计 | `fw_instance_id` | — |
| `CFW/ListIpBlacklist/v1` | 读取导入的IP黑名单列表信息 | `fw_instance_id` | — |
| `CFW/ListIpBlacklistSwitch/v1` | 读取流量过滤功能的开关信息 | `fw_instance_id` | — |
| `CFW/ListIpsProtectMode/v1` | 读取防护模式 | `object_id` | — |
| `CFW/ListIpsRules/v1` | 读取IPS规则列表 | `object_id` | — |
| `CFW/ListIpsSwitchStatus/v1` | 读取IPS特性开关状态 | `object_id` | — |
| `CFW/ListIpsWhitelists/v1` | 读取IPS白名单列表详情 | `fw_instance_id` | — |
| `CFW/ListJob/v1` | 读取CFW任务执行状态 | `job_id` | 复用已有任务标识 |
| `CFW/ListLogConfig/v1` | 读取日志配置 | `fw_instance_id` | — |
| `CFW/ListLogs/v1` | 读取防火墙日志 | `fw_instance_id` | — |
| `CFW/ListPrivateNetworkSegments/v1` | 读取私网网段的信息 | `fw_instance_id` | — |
| `CFW/ListProtectedVpcs/v1` | 读取防护VPC数 | `object_id` | — |
| `CFW/ListSchedules/v1` | 读取时间表列表 | `object_id` | — |
| `CFW/ListServiceItems/v1` | 读取服务成员列表 | `set_id` | — |
| `CFW/ListServiceSetDetail/v1` | 读取服务组详情 | `set_id` | — |
| `CFW/ListServiceSets/v1` | 读取服务组列表 | `object_id` | — |
| `CFW/ShowAccessDetail/v1` | 读取访问控制统计详情 | `fw_instance_id`、`item_id` | — |
| `CFW/ShowAccessTop/v1` | 读取访问日志统计信息 | `fw_instance_id` | — |
| `CFW/ShowAlarmConfig/v1` | 读取告警配置信息 | `fw_instance_id` | — |
| `CFW/ShowAntiVirusRule/v1` | 读取防火墙反病毒规则信息 | `object_id` | — |
| `CFW/ShowAntiVirusSwitch/v1` | 读取反病毒开关 | `object_id` | — |
| `CFW/ShowAttackDetail/v1` | 读取攻击日志统计详情 | `fw_instance_id` | — |
| `CFW/ShowAttackTop/v1` | 读取攻击日志TOP统计 | `fw_instance_id` | — |
| `CFW/ShowAttackTotal/v1` | 读取攻击概览 | `fw_instance_id` | — |
| `CFW/ShowAttackTrend/v1` | 读取攻击趋势 | `fw_instance_id` | — |
| `CFW/ShowAutoProtectStatus/v1` | 读取EIP自动防护状态信息 | `object_id` | — |
| `CFW/ShowConfigQuota/v1` | 读取防火墙配额信息 | `fw_instance_id` | — |
| `CFW/ShowCustomerIpsInfo/v1` | 读取自定义IPS规则详情 | `ips_cfw_id`、`fw_instance_id` | — |
| `CFW/ShowDomainSetDetail/v1` | 读取域名组详情 | `domain_set_id`、`fw_instance_id` | — |
| `CFW/ShowEwAssociatedEr/v1` | 读取VPC间防火墙使用的企业路由器信息 | `fw_instance_id` | — |
| `CFW/ShowEwAssociatedVpc/v1` | 读取VPC边界防火墙使用的引流VPC信息 | `fw_instance_id` | — |
| `CFW/ShowFlowDetail/v1` | 读取流量日志统计详情 | `fw_instance_id` | — |
| `CFW/ShowFlowTop/v1` | 读取流量TOP统计 | `fw_instance_id` | — |
| `CFW/ShowFlowTrend/v1` | 读取会话趋势 | `fw_instance_id` | — |
| `CFW/ShowIpsUpdateTime/v1` | 读取IPS规则细节 | `fw_instance_id` | — |
| `CFW/ShowLogsCount/v1` | 读取日志数量 | `fw_instance_id` | — |
| `CFW/ShowSnFirewallProtectionStatus/v1` | 读取南北向防火墙防护状态 | `fw_instance_id` | — |
| `CFW/ShowTrafficTrend/v1` | 读取流量趋势 | `fw_instance_id` | — |

## Config

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `Config/ListPolicyAssignments/v1` | 读取列出合规规则 | — | — |
| `Config/ListPolicyStatesByResourceId/v1` | 读取资源的合规结果 | `resource_id` | — |
| `Config/ListRemediationExecutionStatuses/v1` | 读取修正执行结果 | `policy_assignment_id` | — |
| `Config/ShowEvaluationStateByAssignmentId/v1` | 读取规则的评估状态 | `policy_assignment_id` | — |
| `Config/ShowRemediationConfiguration/v1` | 读取修正配置 | `policy_assignment_id` | — |

## IAM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `IAM/GetAccountSummaryV5/v5` | 读取此账号中IAM实体使用情况和IAM配额的摘要信息 | — | — |
| `IAM/GetFeatureStatusV5/v5` | 读取此账号的功能状态 | `feature_name` | — |
| `IAM/GetPolicyV5/v5` | 读取通过身份策略ID获取身份策略 | `policy_id` | — |
| `IAM/GetPolicyVersionV5/v5` | 读取指定身份策略版本 | `policy_id`、`version_id` | — |
| `IAM/KeystoneListAllProjectPermissionsForGroup/v3` | 读取用户组的所有项目权限列表 | `group_id` | — |
| `IAM/KeystoneListDomainPermissionsForGroup/v3` | 读取全局服务中的用户组权限 | `group_id` | — |
| `IAM/KeystoneListGroupsForUser/v3` | 读取IAM用户所属用户组 | `user_id` | — |
| `IAM/KeystoneListProjectPermissionsForGroup/v3` | 读取项目服务中的用户组权限 | `group_id` | — |
| `IAM/ListAgencies/v3` | 读取指定条件下的委托列表 | — | — |
| `IAM/ListAllProjectsPermissionsForAgency/v3` | 读取委托下的所有项目服务权限列表 | `agency_id` | — |
| `IAM/ListAttachedAgencyPoliciesV5/v5` | 读取指定委托或信任委托附加的所有身份策略 | `agency_id` | — |
| `IAM/ListAttachedGroupPoliciesV5/v5` | 读取指定用户组附加的所有身份策略 | `group_id` | — |
| `IAM/ListAttachedUserPoliciesV5/v5` | 读取指定IAM用户附加的所有身份策略 | `user_id` | — |
| `IAM/ListCustomPolicies/v3` | 读取自定义策略列表 | — | — |
| `IAM/ListDomainPermissionsForAgency/v3` | 读取全局服务中的委托权限 | `agency_id` | — |
| `IAM/ListEnterpriseProjectsForUser/v3` | 读取用户直接关联的企业项目 | `user_id` | — |
| `IAM/ListPermanentAccessKeys/v3` | 读取所有永久访问密钥 | — | — |
| `IAM/ListProjectPermissionsForAgency/v3` | 读取项目服务中的委托权限 | `agency_id` | — |
| `IAM/ListRolesForUserOnEnterpriseProject/v3` | 读取企业项目直接关联用户的权限 | `enterprise_project_id`、`user_id` | — |
| `IAM/ShowAccessKeyLastUsedV5/v5` | 读取指定永久访问密钥最后使用时间 | `access_key_id`、`user_id` | — |
| `IAM/ShowAgency/v3` | 读取委托详情 | `agency_id` | — |
| `IAM/ShowCustomPolicy/v3` | 读取自定义策略详情 | `role_id` | — |
| `IAM/ShowDomainApiAclPolicy/v3` | 读取账号接口访问策略 | — | — |
| `IAM/ShowDomainConsoleAclPolicy/v3` | 读取账号控制台访问策略 | — | — |
| `IAM/ShowDomainQuota/v3` | 读取账号配额 | — | — |
| `IAM/ShowDomainRoleAssignments/v3` | 读取指定账号中的授权记录 | — | — |
| `IAM/ShowPermanentAccessKey/v3` | 读取指定永久访问密钥 | `access_key` | — |
| `IAM/ShowProjectQuota/v3` | 读取项目配额 | — | — |
| `IAM/ShowUser/v3` | 读取IAM用户详情(推荐) | `user_id` | — |
| `IAM/ShowUserLoginProtect/v3` | 读取指定IAM用户的登录保护状态信息 | `user_id` | — |
| `IAM/ShowUserV5/v5` | 读取IAM用户详情 | `user_id` | — |

## IAMAccessAnalyzer

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `IAMAccessAnalyzer/CheckNoNewAccess/v1` | 校验策略是否有新访问权限 | — | — |
| `IAMAccessAnalyzer/CreateAccessPreview/v1` | 创建分析：创建访问预览 | `analyzer_id`、`resource_urn` | — |
| `IAMAccessAnalyzer/ListAccessPreviewFindings/v1` | 读取相关预览生成的分析结果 | `access_preview_id`、`analyzer_id` | — |
| `IAMAccessAnalyzer/ListAccessPreviews/v1` | 读取所有访问预览 | `analyzer_id` | — |
| `IAMAccessAnalyzer/ListAnalyzers/v1` | 读取检索分析器的列表 | — | — |
| `IAMAccessAnalyzer/ListArchiveRules/v1` | 读取检索为指定分析器创建的存档规则的列表 | `analyzer_id` | — |
| `IAMAccessAnalyzer/ListFindings/v1` | 读取检索指定分析器生成的访问分析结果列表 | `analyzer_id` | — |
| `IAMAccessAnalyzer/ListNotificationSettings/v1` | 读取消息通知配置列表 | — | — |
| `IAMAccessAnalyzer/ListResourceConfigurations/v1` | 读取列举资源分析配置 | `analyzer_id` | — |
| `IAMAccessAnalyzer/ShowAccessPreview/v1` | 读取相关访问预览的信息 | `access_preview_id`、`analyzer_id` | — |
| `IAMAccessAnalyzer/ShowAnalyzer/v1` | 读取显示指定的分析器 | `analyzer_id` | — |
| `IAMAccessAnalyzer/ShowArchiveRule/v1` | 读取检索有关存档规则的信息 | `analyzer_id`、`archive_rule_id` | — |
| `IAMAccessAnalyzer/ShowFinding/v1` | 读取检索有关指定结果的信息 | `analyzer_id`、`finding_id` | — |
| `IAMAccessAnalyzer/ShowNotificationSetting/v1` | 读取消息通知配置 | `notification_setting_id` | — |
| `IAMAccessAnalyzer/StartResourceScan/v1` | 策略扫描：立即开始扫描应用于指定资源的策略 | `analyzer_id`、`resource_urn` | — |
| `IAMAccessAnalyzer/ValidatePolicy/v1` | 校验策略 | — | — |

## RMS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `RMS/ListPolicyAssignments/v1` | 读取列出合规规则 | — | — |
| `RMS/ListPolicyStatesByResourceId/v1` | 读取资源的合规结果 | `resource_id` | — |
| `RMS/ShowEvaluationStateByAssignmentId/v1` | 读取规则的评估状态 | `policy_assignment_id` | — |

## SecMaster

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `SecMaster/ChangeAlert/v1` | 更新告警 | `alert_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ChangeIncident/v1` | 更新事件 | `incident_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ChangePlaybookInstance/v1` | 操作剧本实例 | `instance_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/CreateAdhocQuery/v2` | 查询任务：创建adhoc查询 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/CreateAlertRuleSimulation/v1` | 模拟任务：模拟告警规则 | `workspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/CreateSearchAnalysis/v1` | 分析任务：执行分析 | `workspace_id`、`dataspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/CreateTableAnalysis/v2` | 分析任务：创建安全分析查询 | `table_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/CreateWorkflowInstance/v1` | 执行流程：创建流程实例 | `workflow_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListAlerts/v1` | 读取搜索告警列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListAopWorkflowInstance/v1` | 读取流程实例的列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListCloudLogResources/v1` | 读取列出云日志资源 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListCollectConfig/v1` | 读取云服务采集配置 | — | — |
| `SecMaster/ListCollectConfig/v2` | 读取云服务采集配置 | — | — |
| `SecMaster/ListCollectorChannels/v1` | 读取列出采集通道列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListCollectorConnections/v1` | 读取列表采集连接 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListCollectorInstances/v1` | 读取列出采集通道实例 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListCollectorNode/v1` | 读取列出采集节点 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListDataobjectRelations/v1` | 读取关联数据对象列表 | `data_object_id`、`dataclass_type`、`related_dataclass_type`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListDataobjects/v1` | 读取列出所有数据对象 | `dataclass_name`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListDataspaces/v1` | 读取数据空间列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListIncidents/v1` | 读取搜索事件列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListIndicators/v1` | 读取威胁情报列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListNotes/v1` | 读取搜索评论列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListPipes/v1` | 读取数据管道列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListPipes/v2` | 读取管道列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListPlaybookAuditLogs/v1` | 读取剧本实例审计日志 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListPlaybookInstances/v1` | 读取剧本实例列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListPlaybooks/v1` | 读取剧本列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListReports/v1` | 读取报告列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListResources/v1` | 读取搜索资产列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListSearchConditions/v1` | 读取检索条件列表 | `workspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListSearchHistograms/v1` | 读取数据分布直方图 | `workspace_id`、`dataspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListSearchLogs/v1` | 读取检索数据 | `workspace_id`、`dataspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListShippers/v1` | 读取投递信息 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListTableHistograms/v2` | 读取检索表直方图 | `table_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListTableLogs/v2` | 读取检索表日志 | `table_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListTables/v2` | 读取表列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListTasks/v1` | 读取待办列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListVulnerabilities/v1` | 读取漏洞列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ListWorkspaces/v1` | 读取工作空间列表 | — | — |
| `SecMaster/SearchBaseline/v2` | 读取搜索基线检查结果列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/SearchCheckitems/v2` | 读取检查项列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/SearchCompliancePackages/v2` | 读取遵从包列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/SearchPolicy/v1` | 读取策略视图列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/SearchPolicyRecord/v1` | 读取任务视图列表 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/SearchPolicyRecordByPolicyId/v1` | 读取根据策略ID查询历史记录列表 | `policy_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowAdhocResult/v2` | 读取adhoc查询结果 | `query_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowAlert/v1` | 读取告警详情 | `alert_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowAopWorkflowInstance/v1` | 读取流程实例的详情 | `instance_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowCheckitemDetail/v2` | 读取检查项详情 | `checkitem_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowCompliancePackageDetail/v2` | 读取遵从包详情 | `compliance_packages_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowDataobject/v1` | 读取数据对象 | `data_object_id`、`dataclass_name`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowDataspace/v1` | 读取数据空间详情 | `dataspace_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowIncident/v1` | 读取事件详情 | `incident_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowIndicatorDetail/v1` | 读取威胁情报详情 | `indicator_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowMoniterMetricStats/v1` | 读取指标统计数据 | `workspace_id`、`dataspace_id`、`pipe_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowMonitorStats/v2` | 读取监控统计信息 | `table_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPipe/v1` | 读取数据管道详情 | `pipe_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPipe/v2` | 读取管道详情 | `pipe_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPlaybook/v1` | 读取剧本详情 | `playbook_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPlaybookInstance/v1` | 读取剧本实例详情 | `instance_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPlaybookMonitors/v1` | 读取剧本运行监控 | `playbook_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPlaybookStatistics/v1` | 读取剧本数据统计 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPlaybookTopology/v1` | 读取剧本拓扑关系 | `instance_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowPolicy/v1` | 读取策略视图对象 | `policy_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowReportInfo/v1` | 读取报告详情 | `report_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowResource/v1` | 读取资产详情 | `id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowSearchCondition/v1` | 读取检索条件详情 | `condition_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowShipper/v1` | 读取投递规则详情 | `shipper_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowTable/v2` | 读取表详情 | `table_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowTask/v1` | 读取待办的详情 | `task_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | 复用已有任务标识 |
| `SecMaster/ShowVulnerability/v1` | 读取漏洞详情 | `vul_id`、`workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |
| `SecMaster/ShowWorkspace/v1` | 读取工作空间详情 | `workspace_id`；缺 `workspace_id` → [SecMaster/ListWorkspaces/v1](hcloud.md#secmaster) | — |

## WAF

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WAF/CheckAgency/v1` | 读取独享引擎代理 | — | — |
| `WAF/ConfirmAsyncJob/v1` | 读取异步任务详情 | `job_id` | 复用已有任务标识 |
| `WAF/ConfirmDnsDomain/v1` | 读取用户托管在云解析上的域名 | — | — |
| `WAF/ConfirmIpReputationRule/v1` | 读取根据Id查询威胁情报访问控制规则 | `policy_id`、`rule_id` | — |
| `WAF/ListAntiTamperPolicyRules/v1` | 读取所有策略网页防篡改 | — | — |
| `WAF/ListAnticrawlerRules/v1` | 读取JS脚本反爬虫规则列表 | `policy_id` | — |
| `WAF/ListAntileakagePolicyRules/v1` | 读取所有策略防敏感信息泄露规则 | — | — |
| `WAF/ListAntileakageRules/v1` | 读取防敏感信息泄露规则列表 | `policy_id` | — |
| `WAF/ListAntitamperRule/v1` | 读取防篡改规则列表 | `policy_id` | — |
| `WAF/ListAttackActionTypes/v1` | 读取攻击防护类型 | — | — |
| `WAF/ListBandwidthTimeline/v1` | 读取安全统计带宽数据 | — | — |
| `WAF/ListCcPolicyRules/v1` | 读取所有策略CC规则 | — | — |
| `WAF/ListCcRules/v1` | 读取cc规则列表 | `policy_id` | — |
| `WAF/ListCertificates/v1` | 读取证书列表 | — | — |
| `WAF/ListCompositeHosts/v1` | 读取全部防护域名列表 | — | — |
| `WAF/ListCustomPolicyRules/v1` | 读取所有策略精准防护规则 | — | — |
| `WAF/ListCustomRules/v1` | 读取精准防护规则列表 | `policy_id` | — |
| `WAF/ListEvent/v1` | 读取攻击事件列表 | — | — |
| `WAF/ListEventLog/v1` | 读取下载地址：查询事件日志下载的url | — | — |
| `WAF/ListGeoIpPolicyRules/v1` | 读取所有策略地理位置访问控制 | — | — |
| `WAF/ListGeoipRule/v1` | 读取地理位置访问控制规则列表 | `policy_id` | — |
| `WAF/ListHost/v1` | 读取云模式防护域名列表 | — | — |
| `WAF/ListHostRoute/v1` | 读取云模式域名路由信息 | `instance_id` | — |
| `WAF/ListIgnorePolicyRules/v1` | 读取所有策略全局白名单 | — | — |
| `WAF/ListIgnoreRule/v1` | 读取全局白名单(原误报屏蔽)规则列表 | `policy_id` | — |
| `WAF/ListInstance/v1` | 读取WAF独享引擎列表 | — | — |
| `WAF/ListInstancePools/v1` | 读取实例组列表 | — | — |
| `WAF/ListInstanceStatus/v1` | 读取WAF独享引擎状态列表 | — | — |
| `WAF/ListIpGroup/v1` | 读取地址组列表 | — | — |
| `WAF/ListIpReputationPolicyRules/v1` | 读取所有策略威胁情报控制规则 | — | — |
| `WAF/ListIpReputationRules/v1` | 读取威胁情报规则列表 | `policy_id` | — |
| `WAF/ListOverviewsClassification/v1` | 读取安全总览分类统计top信息 | — | — |
| `WAF/ListOverviewsHostDomains/v1` | 读取泛域名的防护事件中的子域名,仅泛域名存在子域名 | `host_id` | — |
| `WAF/ListPolicy/v1` | 读取防护策略列表 | — | — |
| `WAF/ListPolicyProtectRules/v1` | 读取所有策略指定类型的防护规则 | `rule_type` | — |
| `WAF/ListPremiumHost/v1` | 读取独享模式域名列表 | — | — |
| `WAF/ListPrivacyPolicyRules/v1` | 读取所有策略隐私屏蔽防护规则 | — | — |
| `WAF/ListPrivacyRule/v1` | 读取隐私屏蔽防护规则列表 | `policy_id` | — |
| `WAF/ListPunishmentRules/v1` | 读取攻击惩罚规则列表 | `policy_id` | — |
| `WAF/ListQpsTimeline/v1` | 读取安全统计qps次数 | — | — |
| `WAF/ListRequestTimeline/v1` | 读取安全总览中请求次数时间线统计数据 | — | — |
| `WAF/ListResponseCodeTimeline/v1` | 读取安全统计响应码数据 | — | — |
| `WAF/ListSourceIpTop5/v1` | 读取攻击源ip | — | — |
| `WAF/ListStatistics/v1` | 读取安全总览请求与攻击数量 | — | — |
| `WAF/ListThreats/v1` | 读取攻击事件分布类型 | — | — |
| `WAF/ListTopAbnormal/v1` | 读取业务异常数量 | — | — |
| `WAF/ListTopDomains/v1` | 读取top受攻击域名 | — | — |
| `WAF/ListTopIp/v1` | 读取攻击源ip | — | — |
| `WAF/ListTopUrl/v1` | 读取被攻击url | — | — |
| `WAF/ListUrl/v1` | 读取事件日志中的url | — | — |
| `WAF/ListValueList/v1` | 读取引用表列表 | — | — |
| `WAF/ListWebBasicProtectionRules/v1` | 读取web基础防护内置规则列表 | — | — |
| `WAF/ListWhiteblackipPolicyRules/v1` | 读取所有策略黑白名单防护规则 | — | — |
| `WAF/ListWhiteblackipRule/v1` | 读取黑白名单规则列表 | `policy_id` | — |
| `WAF/ShowAnticrawlerRule/v1` | 读取JS脚本反爬虫防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowAntileakageRule/v1` | 读取防敏感信息泄露防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowAntitamperRule/v1` | 读取防篡改防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowCcRule/v1` | 读取根据Id查询cc防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowCompositeHost/v1` | 读取根据Id查询防护域名 | `host_id` | — |
| `WAF/ShowConsoleConfig/v1` | 读取局点支持特性查询 | — | — |
| `WAF/ShowCustomRule/v1` | 读取根据Id查询精准防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowEvent/v1` | 读取指定事件id的防护事件详情 | `eventid` | — |
| `WAF/ShowGeoipRule/v1` | 读取地理位置控制防护规则详情 | `policy_id`、`rule_id` | — |
| `WAF/ShowHost/v1` | 读取根据防护域名Id查询云模式防护域名详细信息 | `instance_id` | — |
| `WAF/ShowHostStatus/v1` | 读取域名运行状态 | `host_id` | — |
| `WAF/ShowIgnoreRule/v1` | 读取全局白名单(原误报屏蔽)防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowInstance/v1` | 读取WAF独享引擎信息 | `instance_id` | — |
| `WAF/ShowIpGroup/v1` | 读取ip地址组明细 | `id` | — |
| `WAF/ShowLtsInfoConfig/v1` | 读取lts配置信息 | — | — |
| `WAF/ShowPolicy/v1` | 读取根据Id查询防护策略 | `policy_id` | — |
| `WAF/ShowPool/v1` | 读取实例组详情 | `pool_id` | — |
| `WAF/ShowPremiumHost/v1` | 读取独享模式域名配置 | `host_id` | — |
| `WAF/ShowPrivacyRule/v1` | 读取隐私屏蔽防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowPunishmentRule/v1` | 读取根据Id查询攻击惩罚防护规则 | `policy_id`、`rule_id` | — |
| `WAF/ShowSourceIp/v1` | 读取WAF回源Ip信息 | — | — |
| `WAF/ShowValueList/v1` | 读取引用表 | `valuelistid` | — |
| `WAF/ShowWebProtectionRule/v1` | 读取根据Id查询Web防护规则 | `rule_id` | — |
| `WAF/ShowWhiteBlackIpRule/v1` | 读取黑白名单防护规则 | `policy_id`、`rule_id` | — |
