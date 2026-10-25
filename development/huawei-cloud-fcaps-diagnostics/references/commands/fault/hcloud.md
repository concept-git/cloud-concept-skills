# 故障 F

查询事件、诊断任务和结果。执行类操作按当前授权范围选择。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[AOM](hcloud.md#aom) · [APM](hcloud.md#apm) · [CBR](hcloud.md#cbr) · [CES](hcloud.md#ces) · [COC](hcloud.md#coc) · [DNS](hcloud.md#dns) · [ECS](hcloud.md#ecs) · [EIP](hcloud.md#eip) · [ELB](hcloud.md#elb) · [EVS](hcloud.md#evs) · [IMS](hcloud.md#ims) · [LTS](hcloud.md#lts) · [SMN](hcloud.md#smn) · [VPN](hcloud.md#vpn)

## AOM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `AOM/CountEvents/v2` | 读取事件告警统计 | — | — |
| `AOM/ExecuteWorkflow/v1` | 执行工作流 | `workflow_id` | — |
| `AOM/ListActionRule/v2` | 读取告警行动规则列表 | — | — |
| `AOM/ListAlarmRule/v2` | 读取阈值规则列表 | — | — |
| `AOM/ListAlarmRuleTemplate/v2` | 读取告警模板列表 | — | — |
| `AOM/ListAllJobByName/v1` | 读取作业管理主页模糊查询 | — | — |
| `AOM/ListAllScriptByName/v1` | 读取脚本查询 | `script_id` | — |
| `AOM/ListEvent2alarmRule/v2` | 读取事件类告警规则列表 | — | — |
| `AOM/ListEvents/v2` | 读取事件告警信息 | — | — |
| `AOM/ListMetricOrEventAlarmRule/v2` | 读取指标类或者事件类告警规则列表 | — | — |
| `AOM/ListMuteRule/v2` | 读取静默规则列表 | — | — |
| `AOM/ListNotificationTemplateByName/v2` | 读取根据消息通知模板名称查询消息通知模板 | `name` | — |
| `AOM/ListNotificationTemplates/v2` | 读取消息通知模板列表 | — | — |
| `AOM/ListNotifiedHistories/v2` | 读取告警发送结果 | — | — |
| `AOM/ListTemplateByJobId/v1` | 读取根据作业id查询方案(自定义模板)列表 | `job_id` | 复用已有任务标识 |
| `AOM/ListWorkflow/v1` | 读取任务列表 | — | — |
| `AOM/ListWorkflowExecutions/v1` | 读取任务执行历史 | `workflow_id` | — |
| `AOM/SearchTemplateById/v1` | 读取方案信息 | `template_id` | — |
| `AOM/SearchWorkflowExecutionDetail/v1` | 读取工作流执行中的执行详情 | `execution_id`、`workflow_id` | 复用已有任务标识 |
| `AOM/ShowActionRule/v2` | 读取通过规则名称获取告警行动规则 | `rule_name` | — |
| `AOM/ShowAlarmRule/v2` | 读取单条阈值规则 | `alarm_rule_id` | — |

## APM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `APM/ListAlarmData/v1` | 读取告警列表 | `x-business-id`、`business_id` | — |
| `APM/ListAlarmNotify/v1` | 读取告警消息列表 | `x-business-id`、`alarm_data_id` | — |

## CBR

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CBR/CheckAgent/v1` | 主动检查：查询Agent状态 | `agent_status.[N].resource_id` | — |
| `CBR/ListOpLogs/v1` | 读取任务列表 | — | — |
| `CBR/RestoreBackup/v1` | 恢复数据：备份恢复 | `backup_id`；缺 `backup_id` → [CBR/ListBackups/v1](../configuration/hcloud.md#cbr) | — |
| `CBR/ShowOpLog/v1` | 读取单个任务 | `operation_log_id`；缺 `operation_log_id` → [CBR/ListOpLogs/v1](hcloud.md#cbr) | — |

## CES

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CES/BatchEnableAlarmRules/v2` | 批量启停告警规则 | — | — |
| `CES/CreateAlarmRules/v2` | 创建告警规则(推荐) | — | — |
| `CES/CreateOneClickAlarm/v2` | 创建一键告警 | `one_click_alarm_id` | — |
| `CES/ListAlarmHistories/v1` | 读取告警历史 | — | — |
| `CES/ListAlarmHistories/v2` | 读取告警记录列表 | 目标资源 | `from/to` 使用 ISO 8601 字符串 |
| `CES/ListAlarmRulePolicies/v2` | 读取告警规则策略列表 | `alarm_id` | — |
| `CES/ListAlarmRuleResources/v2` | 读取告警规则资源列表 | `alarm_id` | — |
| `CES/ListAlarmRules/v2` | 读取告警规则列表(推荐) | — | — |
| `CES/ListAlarmTemplateAssociationAlarms/v2` | 读取告警模板关联的告警规则列表 | `template_id` | — |
| `CES/ListAlarmTemplates/v1` | 读取自定义告警模板列表 | — | — |
| `CES/ListAlarmTemplates/v2` | 读取告警模板列表 | — | — |
| `CES/ListAlarms/v1` | 读取告警规则列表(V1) | — | — |
| `CES/ListEventDetail/v1` | 读取某一事件监控详情 | `event_name` | — |
| `CES/ListEvents/v1` | 读取事件监控列表 | — | — |
| `CES/ListNotificationMaskResources/v2` | 读取告警通知屏蔽资源列表 | `notification_mask_id` | — |
| `CES/ListNotificationMasks/v2` | 读取告警通知屏蔽列表 | — | — |
| `CES/ListOneClickAlarmRules/v2` | 读取一键告警关联告警规则列表 | `one_click_alarm_id` | — |
| `CES/ListOneClickAlarms/v2` | 读取一键告警列表 | — | — |
| `CES/ShowAlarm/v1` | 读取单条告警规则信息 | `alarm_id` | — |
| `CES/ShowAlarmTemplate/v2` | 读取告警模板详情 | `template_id` | — |
| `CES/ShowEventData/v1` | 读取主机配置数据 | — | 仅适用于 SAP HANA 的 SAP Monitor |
| `CES/UpdateAlarm/v1` | 修改告警规则 | `alarm_id` | — |

## COC

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `COC/CancelDiagnosisTask/v1` | 取消诊断任务 | `task_id` | 复用已有任务标识 |
| `COC/CreateDiagnosisTask/v1` | 安装 Holmes 并采集主机诊断数据 | 已纳管的目标实例 | UniAgent 在线且具备采集授权；ECS 用 `type=ECS` |
| `COC/CreateScheduledTask/v1` | 新建定时运维 | `associated_task_id` | — |
| `COC/DisableScheduledTask/v1` | 禁用ScheduledTask | `task_id` | 复用已有任务标识 |
| `COC/EnableScheduledTask/v1` | 启用ScheduledTask | `task_id` | 复用已有任务标识 |
| `COC/ExecuteDocument/v1` | 执行作业：执行自定义作业 | `document_id` | — |
| `COC/ExecutePublicScript/v1` | 主机执行：执行公共脚本 | `script_uuid`、`execute_batches.[N].target_instances.[N].region_id`、`execute_batches.[N].target_instances.[N].resource_id` | — |
| `COC/ExecuteScript/v1` | 主机执行：执行自定义脚本 | `script_uuid`、`execute_batches.[N].target_instances.[N].region_id`、`execute_batches.[N].target_instances.[N].resource_id` | — |
| `COC/GetDocument/v1` | 读取自定义作业详情 | `document_id` | — |
| `COC/GetDocumentAtomicInfo/v1` | 读取原子能力详情 | `atomic_unique_key` | — |
| `COC/GetExecution/v1` | 读取作业工单详情 | `execution_id` | 复用已有任务标识 |
| `COC/GetPublicScript/v1` | 读取展示公共脚本详情 | `script_uuid` | — |
| `COC/GetScript/v1` | 读取自定义脚本详情 | `script_uuid` | — |
| `COC/GetScriptJobBatch/v1` | 读取展示批次详情 | `batch_index`、`execute_uuid` | — |
| `COC/GetScriptJobInfo/v1` | 读取展示脚本工单基本信息 | `execute_uuid` | — |
| `COC/GetScriptJobStatistics/v1` | 读取展示实例状态统计信息 | `execute_uuid` | — |
| `COC/ListAlarmHandleHistories/v1` | 读取告警工单历史 | `alarm_id` | — |
| `COC/ListCocTicketOperationHistories/v1` | 读取GetCocTicketOperationHistories 获取事件单历史 | `ticket_type` | — |
| `COC/ListDiagnosisTasks/v1` | 读取诊断记录 | — | 需 `page_index`、`page_size`；按 `type`、`region` 限定 |
| `COC/ListDocumentAtomics/v1` | 读取原子能力列表 | — | — |
| `COC/ListDocuments/v1` | 读取自定义作业列表 | — | — |
| `COC/ListExecutionInstances/v1` | 读取工单步骤批次实例 | — | — |
| `COC/ListExecutionSteps/v1` | 读取工单步骤详情 | `execution_id` | 复用已有任务标识 |
| `COC/ListExecutions/v1` | 读取作业工单列表 | — | — |
| `COC/ListIncidentSimpleTickets/v1` | 读取简易版事件单列表 | — | — |
| `COC/ListIncidents/v1` | 读取ListIncidents 查询事件单列表 | — | — |
| `COC/ListIncidentsHistories/v1` | 读取ListIncidentsHistories 获取事件单历史 | `incident_id` | — |
| `COC/ListInstancesBatch/v1` | 计算分批：获取自动分批结果 | `target_instances.[N].region_id`、`target_instances.[N].resource_id` | — |
| `COC/ListPublicScripts/v1` | 读取公共脚本列表 | — | — |
| `COC/ListScheduledTask/v1` | 读取ScheduledTask列表 | — | — |
| `COC/ListScheduledTaskHistory/v1` | 读取定时运维历史记录 | `task_id` | 复用已有任务标识 |
| `COC/ListScriptJobBatches/v1` | 读取展示批次列表 | `execute_uuid` | — |
| `COC/ListScriptJobs/v1` | 读取展示工单列表 | — | — |
| `COC/ListScripts/v1` | 读取脚本列表 | — | — |
| `COC/OperateExecution/v1` | 操作工单 | `execution_id` | 复用已有任务标识 |
| `COC/OperateScriptJob/v1` | 操作脚本工单 | `execute_uuid` | — |
| `COC/ResetAccountPassword/v1` | 主机密码重置 | — | — |
| `COC/RetryDiagnosisTask/v1` | 重试诊断任务 | `task_id` | 复用已有任务标识 |
| `COC/ShowAlarm/v1` | 读取Alarm | `alarm_id` | — |
| `COC/ShowCocIncidentDetail/v1` | 读取GetCocIncidentDetail 获取事件单详情 | `incident_num` | — |
| `COC/ShowCocIssuesDetail/v1` | 读取GetCocIssuesDetail 获取问题单详情 | `ticket_id` | — |
| `COC/ShowDiagnosisNode/v1` | 读取指定诊断记录下的指定诊断步骤的详情 | `task_id`、`instance_id`、`code` | 步骤名以 help 为准 |
| `COC/ShowDiagnosisSummary/v1` | 读取批量诊断任务的结果概要 | 已有 `task_id`；缺失 → [COC/ListDiagnosisTasks/v1](hcloud.md#coc) | 复用已有任务 |
| `COC/ShowDiagnosisTask/v1` | 读取单个诊断任务详情 | `task_id`、`instance_id` | 复用已有诊断任务 |
| `COC/ShowIncidentTask/v1` | 读取ShowIncidentTask 获取事件任务 | `incident_id` | — |
| `COC/ShowJobDetail/v1` | 读取任务详情 | `job_id` | 复用已有任务标识 |
| `COC/ShowScheduledTask/v1` | 读取ScheduledTask | `task_id` | 复用已有任务标识 |

## DNS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `DNS/ShowDomainDetection/v2` | 查询诊断：查询公网域名的域名诊断 | `zone_id` | — |

## ECS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ECS/AcceptScheduledEvent/v2` | 接受并授权执行计划事件操作 | `id` | — |
| `ECS/BatchRebootServers/v2` | 批量重启云服务器 | `reboot.servers.[N].id` | — |
| `ECS/BatchResetServersPassword/v2` | 批量重置弹性云服务器密码 | `servers.[N].id` | — |
| `ECS/BatchStartServers/v2` | 批量启动云服务器 | `os-start.servers.[N].id` | — |
| `ECS/BatchStopServers/v2` | 批量关闭云服务器 | `os-stop.servers.[N].id` | — |
| `ECS/ChangeServerOsWithCloudInit/v2` | 切换弹性云服务器操作系统(安装Cloud init) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ChangeServerOsWithoutCloudInit/v2` | 切换弹性云服务器操作系统(未安装Cloud init) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ExecuteServerDump/v2` | 触发云服务器内核转储 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ExecuteServerRedeploy/v2` | 重部署云服务器 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ListScheduledEvents/v2` | 读取计划事件列表 | — | — |
| `ECS/MigrateServer/v2` | 冷迁移云服务器 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/NovaListServerActions/v2` | 读取云服务器操作行为列表 | `server_id: ECS.ServerId` | 历史接口；操作审计优先 [CTS/ListTraces/v3](../common/hcloud.md#cts) |
| `ECS/NovaRebootServer/v2` | 重启云服务器 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/NovaShowServerAction/v2` | 读取指定请求的云服务器操作详情 | `server_id: ECS.ServerId`、`request_id`；缺请求标识 → [ECS/NovaListServerActions/v2](hcloud.md#ecs) | 历史接口 |
| `ECS/NovaStartServer/v2` | 启动云服务器 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/NovaStopServer/v2` | 关闭云服务器 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ReinstallServerWithCloudInit/v2` | 重装弹性云服务器操作系统(安装Cloud-init) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ReinstallServerWithoutCloudInit/v2` | 重装弹性云服务器操作系统(未安装Cloud init) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ResetServerPassword/v2` | 一键重置弹性云服务器密码(企业项目) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ShowJob/v2` | 读取任务的执行状态 | `job_id` | 复用已有任务标识 |
| `ECS/ShowResetPasswordFlag/v2` | 读取是否支持一键重置密码 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ShowSerialConsoleActions/v2` | 生成串口控制台登录地址 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ShowServerConsoleOutput/v2` | 读取弹性云服务器的控制台日志 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ShowServerRemoteConsole/v2` | 生成远程控制台登录地址 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/UpdateScheduledEvent/v2` | 更新计划事件 | `id` | — |
| `ECS/UpdateSerialConsoleOptions/v2` | 设置云服务器云主机串口登录 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |

## EIP

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EIP/ShowResourcesJobDetail/v2` | 读取Job状态接口 | `job_id` | 复用已有任务标识 |

## ELB

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ELB/CreateMemberHealthCheckJob/v3` | 创建后端服务器检测任务 | `member_id` | — |
| `ELB/ListJobs/v3` | 读取异步任务的job列表 | — | — |
| `ELB/ShowJob/v3` | 读取异步任务的job状态 | `job_id` | 复用已有任务标识 |
| `ELB/ShowMemberHealthCheckJob/v3` | 读取后端服务器检测任务的结果 | `job_id` | 复用已有任务标识 |

## EVS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EVS/RollbackSnapshot/v2` | 回滚数据：回滚快照到云硬盘 | `snapshot_id: EVS.SnapshotId`、`rollback.volume_id`；缺 `snapshot_id` → [EVS/ListSnapshots/v2](../configuration/hcloud.md#evs) | — |
| `EVS/ShowJob/v2` | 读取job的状态 | `job_id` | 复用已有任务标识 |

## IMS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `IMS/ShowJob/v2` | 读取异步任务查询 | `job_id` | 复用已有任务标识 |
| `IMS/ShowJobProgress/v2` | 读取异步任务进度查询 | `job_id` | 复用已有任务标识 |

## LTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LTS/ListActiveOrHistoryAlarms/v2` | 读取活动或历史告警列表 | — | — |
| `LTS/ListKeywordsAlarmRules/v2` | 读取关键词告警规则 | — | — |
| `LTS/ListNotificationTemplates/v2` | 读取消息模板 | — | — |
| `LTS/ListNotificationTopics/v2` | 读取SMN主题 | — | — |
| `LTS/ListSqlAlarmRules/v2` | 读取SQL告警规则 | — | — |
| `LTS/ShowNotificationTemplate/v2` | 读取单个消息模板 | `template_name` | — |

## SMN

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `SMN/ListTopicMessageStatistics/v2` | 读取主题的发送详情 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](../configuration/hcloud.md#smn) | — |
| `SMN/PublishHttpDetect/v2` | 发送探测消息：发布探测消息 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](../configuration/hcloud.md#smn) | — |
| `SMN/PublishMessage/v2` | 发送消息：消息发布 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](../configuration/hcloud.md#smn) | — |
| `SMN/ShowHttpDetectResult/v2` | 读取http探测结果 | `task_id`、`topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](../configuration/hcloud.md#smn) | 复用已有任务标识 |
| `SMN/ShowNotifyPolicy/v2` | 读取通知策略 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](../configuration/hcloud.md#smn) | — |

## VPN

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `VPN/CreateConnectionMonitor/v5` | 创建VPN连接监控 | `connection_monitor.vpn_connection_id` | — |
| `VPN/ListConnectionMonitors/v5` | 读取VPN连接监控列表 | — | — |
| `VPN/ListP2cVpnGatewayJobs/v5` | 读取资源任务列表 | — | — |
| `VPN/ListVpnGatewayJobs/v5` | 读取资源任务列表 | — | — |
| `VPN/ShowConnectionMonitor/v5` | 读取VPN连接监控 | `connection_monitor_id` | — |
