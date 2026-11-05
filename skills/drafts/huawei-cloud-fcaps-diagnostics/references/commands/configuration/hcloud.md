# 配置 C

查询资源状态、配置和关系。ACTIVE 仅表示平台实例状态。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[AOM](hcloud.md#aom) · [CBR](hcloud.md#cbr) · [COC](hcloud.md#coc) · [CTS](hcloud.md#cts) · [Config](hcloud.md#config) · [ECS](hcloud.md#ecs) · [EPS](hcloud.md#eps) · [EVS](hcloud.md#evs) · [IMS](hcloud.md#ims) · [LTS](hcloud.md#lts) · [RMS](hcloud.md#rms) · [SMN](hcloud.md#smn)

## AOM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `AOM/BatchImportAgent/v4` | 安装 Agent：下发批量安装UniAgent任务 | `installer_agent_id`、`proxy_region_id` | — |
| `AOM/BatchUpdateAgent/v4` | 升级 Agent：下发批量升级UniAgent任务 | `agent_list.[N].agent_id` | — |
| `AOM/ListAgents/v2` | 读取主机安装的ICAgent信息 | `cluster_id`、`namespace` | — |
| `AOM/ListPermissions/v2` | 读取aom2.0相关云服务授权信息 | — | — |
| `AOM/ListResourceUnderNode/v3` | 读取绑定在节点上的资源列表 | `rf_resource_type`、`type` | — |
| `AOM/ListServiceDiscoveryRules/v2` | 读取系统中已有服务发现规则 | — | — |
| `AOM/ShowAgentInfos/v4` | 读取UniAgent主机列表信息 | — | — |
| `AOM/ShowApp/v3` | 读取应用详情 | `application_id` | — |
| `AOM/ShowAppByName/v3` | 读取根据应用名称查询应用详情 | — | — |
| `AOM/ShowComponent/v3` | 读取组件详情 | `component_id` | — |
| `AOM/ShowComponentByName/v3` | 读取根据组件名称查询组件详情 | `application_id`、`component_name` | — |
| `AOM/ShowEnv/v3` | 读取环境详情 | `environment_id` | — |
| `AOM/ShowEnvByName/v3` | 读取根据环境名称查询环境详情 | `environment_name`、`component_id` | — |

## CBR

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CBR/CopyBackup/v1` | 复制备份 | `backup_id`、`replicate.destination_project_id`、`replicate.destination_vault_id`；缺 `backup_id` → [CBR/ListBackups/v1](hcloud.md#cbr) | — |
| `CBR/CopyCheckpoint/v1` | 复制备份还原点 | `replicate.destination_project_id`、`replicate.destination_vault_id`、`replicate.vault_id` | — |
| `CBR/CreateCheckpoint/v1` | 创建备份还原点 | `checkpoint.vault_id` | — |
| `CBR/DeleteVault/v1` | 删除存储库 | `vault_id`；缺 `vault_id` → [CBR/ListVault/v1](hcloud.md#cbr) | — |
| `CBR/ListAgent/v1` | 读取客户端列表 | — | — |
| `CBR/ListBackups/v1` | 读取所有备份 | — | — |
| `CBR/ListDomainProjects/v1` | 读取租户项目列表 | `domain_name` | — |
| `CBR/ListExternalVault/v1` | 读取其他区域存储库列表 | `external_project_id`、`region_id` | — |
| `CBR/ListFeatures/v1` | 读取服务支持的特性列表 | — | — |
| `CBR/ListOrganizationPolicies/v1` | 读取组织策略列表 | — | — |
| `CBR/ListOrganizationPolicyDetail/v1` | 读取组织策略部署状态列表 | `organization_policy_id` | — |
| `CBR/ListPolicies/v1` | 读取策略列表 | — | — |
| `CBR/ListProjects/v1` | 读取租户的项目信息 | — | — |
| `CBR/ListProtectable/v1` | 读取可保护资源 | `protectable_type` | — |
| `CBR/ListVault/v1` | 读取存储库列表 | — | — |
| `CBR/RegisterAgent/v1` | 注册客户端 | `agent.agent_id` | — |
| `CBR/ShowAgent/v1` | 读取指定客户端 | `agent_id` | — |
| `CBR/ShowBackup/v1` | 读取指定备份 | `backup_id`；缺 `backup_id` → [CBR/ListBackups/v1](hcloud.md#cbr) | — |
| `CBR/ShowCheckpoint/v1` | 读取备份还原点 | `checkpoint_id` | — |
| `CBR/ShowDomain/v1` | 读取租户信息 | `source_project_id` | — |
| `CBR/ShowFeature/v1` | 读取指定特性 | `feature_key` | — |
| `CBR/ShowMemberDetail/v1` | 读取备份成员详情 | `backup_id`、`member_id`；缺 `backup_id` → [CBR/ListBackups/v1](hcloud.md#cbr) | — |
| `CBR/ShowMembersDetail/v1` | 读取备份成员列表 | `backup_id`；缺 `backup_id` → [CBR/ListBackups/v1](hcloud.md#cbr) | — |
| `CBR/ShowMetadata/v1` | 读取备份元数据 | `backup_id`；缺 `backup_id` → [CBR/ListBackups/v1](hcloud.md#cbr) | — |
| `CBR/ShowMigrateStatus/v1` | 读取迁移 | — | — |
| `CBR/ShowOrganizationPolicy/v1` | 读取指定组织策略 | `organization_policy_id` | — |
| `CBR/ShowPolicy/v1` | 读取单个策略 | `policy_id` | — |
| `CBR/ShowProtectable/v1` | 读取指定可保护资源 | `instance_id`、`protectable_type` | — |
| `CBR/ShowReplicationCapabilities/v1` | 读取复制能力 | — | — |
| `CBR/ShowStorageUsage/v1` | 读取容量统计 | — | — |
| `CBR/ShowSummary/v1` | 读取存储库容量总览 | — | — |
| `CBR/ShowVault/v1` | 读取指定存储库 | `vault_id`；缺 `vault_id` → [CBR/ListVault/v1](hcloud.md#cbr) | — |
| `CBR/ShowVaultProjectTag/v1` | 读取存储库项目标签 | — | — |
| `CBR/ShowVaultResourceInstances/v1` | 读取存储库资源实例 | — | — |
| `CBR/ShowVaultTag/v1` | 读取存储库资源标签 | `vault_id`；缺 `vault_id` → [CBR/ListVault/v1](hcloud.md#cbr) | — |
| `CBR/UnregisterAgent/v1` | 移除客户端 | `agent_id` | — |
| `CBR/UpdateAgent/v1` | 修改客户端 | `agent_id` | — |

## COC

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `COC/ListResourceViews/v1` | 读取CMDB跨账号资源视图 | — | — |
| `COC/ListResources/v1` | 读取用户所有资源 | — | — |
| `COC/ListResourcesOfResourceView/v1` | 读取CMDB跨账号资源视图聚合的资源 | `view_id` | — |
| `COC/ShowLastSyncStatus/v1` | 读取多云资源最新同步状态 | — | — |
| `COC/SyncResourceAgent/v1` | 同步 Agent：同步华为云资源Agent信息 | — | — |

## CTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CTS/CheckObsBuckets/v3` | 转储条件检查：检查已经配置OBS桶是否可以成功转储 | — | — |
| `CTS/ListNotifications/v3` | 读取关键操作通知 | `notification_type` | — |
| `CTS/ListOperations/v3` | 读取云服务的全量操作列表 | — | — |
| `CTS/ListQuotas/v3` | 读取租户追踪器配额信息 | — | — |
| `CTS/ListTraceResources/v3` | 读取事件的资源类型列表 | — | — |
| `CTS/ListTrackers/v3` | 读取追踪器 | — | — |
| `CTS/ListUserResources/v3` | 读取30天事件的操作用户列表 | — | — |

## Config

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `Config/ListAllResources/v1` | 读取列举所有资源 | — | — |
| `Config/ListRegions/v1` | 读取用户可见的区域 | — | — |
| `Config/ListResources/v1` | 读取列举指定类型的资源 | `provider`、`type` | — |
| `Config/ListTrackedResources/v1` | 读取列举资源记录器收集的全部资源 | — | — |
| `Config/ShowConfigurationAggregatorSourcesStatus/v1` | 读取指定资源聚合器聚合帐号的状态信息 | `aggregator_id` | — |
| `Config/ShowResourceById/v1` | 读取单个资源 | `provider`、`resource_id`、`type` | — |
| `Config/ShowResourceDetail/v1` | 读取帐号下的单个资源 | `resource_id` | — |
| `Config/ShowResourceHistory/v1` | 读取资源历史 | `resource_id` | — |
| `Config/ShowResourceRelations/v1` | 读取列举资源关系 | `resource_id` | — |
| `Config/ShowResourceRelationsDetail/v1` | 读取列举资源关系详情 | `resource_id` | — |
| `Config/ShowTrackedResourceDetail/v1` | 读取资源记录器收集的单个资源 | `resource_id` | — |
| `Config/ShowTrackerConfig/v1` | 读取记录器 | — | — |

## ECS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ECS/ListCloudServers/v2` | 读取云服务器列表接口 | — | — |
| `ECS/ListFlavorSellPolicies/v2` | 读取规格销售策略 | — | — |
| `ECS/ListFlavors/v2` | 读取规格详情和规格扩展信息列表 | — | — |
| `ECS/ListLaunchTemplateVersions/v2` | 读取模板版本列表 | — | — |
| `ECS/ListRecycleBinServers/v2` | 读取回收站中虚拟机列表 | — | — |
| `ECS/ListServerAzInfo/v2` | 读取可用区列表 | — | — |
| `ECS/ListServerBlockDevices/v2` | 读取弹性云服务器挂载磁盘列表详情信息 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | 用 volumeId、bus、pciAddress 关联设备；云端 device 不直接当作主机设备路径，见 [H-device](../../helpers.md#h-device) |
| `ECS/ListServerGroups/v2` | 读取云服务器组列表 | — | — |
| `ECS/ListServerInterfaces/v2` | 读取云服务器网卡信息 | `server_id: ECS.ServerId` | — |
| `ECS/ListServerTags/v2` | 读取项目标签 | — | — |
| `ECS/ListServerVolumeAttachments/v2` | 读取弹性云服务器挂载磁盘列表信息 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ListServersDetails/v2` | 读取云服务器详情列表 | — | — |
| `ECS/ListTemplates/v2` | 读取模板列表 | — | — |
| `ECS/NovaListAvailabilityZones/v2` | 读取可用区列表 | — | — |
| `ECS/NovaListFlavors/v2` | 读取云服务器规格列表 | — | — |
| `ECS/NovaListFlavorsDetails/v2` | 读取云服务器规格详情列表 | — | — |
| `ECS/NovaListKeypairs/v2` | 读取SSH密钥列表 | — | — |
| `ECS/NovaListServerGroups/v2` | 读取云服务器组列表 | — | — |
| `ECS/NovaListServerInterfaces/v2` | 读取云服务器网卡信息 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaListServerSecurityGroups/v2` | 读取指定云服务器安全组列表 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaListServerVolumes/v2` | 读取弹性云服务器挂载磁盘信息 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaListServers/v2` | 读取云服务器列表 | — | — |
| `ECS/NovaListServersDetails/v2` | 读取云服务器详情列表 | — | — |
| `ECS/NovaListVersions/v2` | 读取API版本信息列表 | — | — |
| `ECS/NovaShowFlavor/v2` | 读取云服务器规格详情 | `flavor_id` | — |
| `ECS/NovaShowFlavorExtraSpecs/v2` | 读取云服务器规格extra_specs的详情 | `flavor_id` | — |
| `ECS/NovaShowKeypair/v2` | 读取SSH密钥详情 | `keypair_name` | — |
| `ECS/NovaShowServer/v2` | 读取云服务器详情 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaShowServerGroup/v2` | 读取云服务器组详情 | `server_group_id` | — |
| `ECS/NovaShowServerInterface/v2` | 读取指定云服务器网卡信息 | `port_id`、`server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaShowServerMetadata/v2` | 读取云服务器元数据列表 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaShowServerMetadataItem/v2` | 读取云服务器指定Key的元数据 | `key`、`server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaShowServerVolume/v2` | 读取弹性云服务器挂载的单个磁盘信息 | `server_id: ECS.ServerId`、`volume_id`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/NovaShowVersion/v2` | 读取指定API版本信息 | `api_version` | — |
| `ECS/ShowAppendableVolumeQuota/v2` | 读取包周期虚拟机可以追加卷数量 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ShowMetadataOptions/v2` | 读取云服务器元数据配置 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ShowRecycleBin/v2` | 读取回收站配置 | — | — |
| `ECS/ShowServer/v2` | 读取云服务器详情 | `server_id: ECS.ServerId`；缺失 → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ShowServerAttachableNicNum/v2` | 读取虚拟机可挂载网卡 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ShowServerBlockDevice/v2` | 读取弹性云服务器单个磁盘信息 | `server_id: ECS.ServerId`、`volume_id`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |
| `ECS/ShowServerGroup/v2` | 读取云服务器组详情 | `server_group_id` | — |
| `ECS/ShowServerLimits/v2` | 读取租户配额 | — | — |
| `ECS/ShowServerTags/v2` | 读取云服务器标签 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](hcloud.md#ecs) | — |

## EPS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EPS/ListMigrationRecord/v1` | 读取资源迁移记录 | — | — |
| `EPS/ShowEnterpriseProjectQuota/v1` | 读取企业项目配额 | — | — |

## EVS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EVS/CinderListAvailabilityZones/v2` | 读取所有的可用分区信息 | — | — |
| `EVS/CinderListQuotas/v2` | 读取租户的详细配额 | 当前 IAM 项目 ID | `target_project_id=project_id`；KooCLI 7.2.12 用 `usage=True` |
| `EVS/CinderListVolumeTransfers/v2` | 读取云硬盘过户记录列表概要 | — | — |
| `EVS/CinderListVolumeTypes/v2` | 读取云硬盘类型列表 | — | — |
| `EVS/CinderShowVolumeTransfer/v2` | 读取单个云硬盘过户记录详情 | `transfer_id` | — |
| `EVS/CreateSnapshot/v2` | 创建云硬盘快照 | `snapshot.volume_id` | — |
| `EVS/ListSnapshots/v2` | 读取云硬盘快照详情列表 | — | — |
| `EVS/ListVersions/v2` | 读取接口版本信息列表 | — | — |
| `EVS/ListVolumeTags/v2` | 读取云硬盘资源的所有标签 | — | — |
| `EVS/ListVolumes/v2` | 读取所有云硬盘详情 | — | — |
| `EVS/ListVolumesByTags/v2` | 读取通过标签查询云硬盘资源实例详情 | — | — |
| `EVS/ListVolumesInRecycle/v2` | 读取回收站中所有云硬盘详情 | — | — |
| `EVS/RetypeVolume/v2` | 磁盘类型变更 | `volume_id: EVS.VolumeId`；缺 `volume_id` → [EVS/ListVolumes/v2](hcloud.md#evs) | — |
| `EVS/ShowRecyclePolicy/v2` | 读取回收站策略 | — | — |
| `EVS/ShowSnapshot/v2` | 读取单个云硬盘快照详情 | `snapshot_id: EVS.SnapshotId`；缺 `snapshot_id` → [EVS/ListSnapshots/v2](hcloud.md#evs) | — |
| `EVS/ShowVersion/v2` | 读取API接口的版本信息 | `version` | — |
| `EVS/ShowVolume/v2` | 读取单个云硬盘详情 | `volume_id: EVS.VolumeId`；缺失 → [H-volume](../../helpers.md#h-volume) | — |
| `EVS/ShowVolumeInRecycle/v2` | 读取回收站中单个云硬盘详情 | `volume_id: EVS.VolumeId`；缺 `volume_id` → [EVS/ListVolumes/v2](hcloud.md#evs) | — |
| `EVS/ShowVolumeTags/v2` | 读取云硬盘标签 | `volume_id: EVS.VolumeId`；缺 `volume_id` → [EVS/ListVolumes/v2](hcloud.md#evs) | — |

## IMS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `IMS/CreateImage/v2` | 制作镜像 | — | — |
| `IMS/CreateWholeImage/v2` | 制作整机镜像 | — | — |
| `IMS/ExportImage/v2` | 导出镜像 | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/GlanceListImageMemberSchemas/v2` | 读取镜像成员列表视图(OpenStack原生) | — | — |
| `IMS/GlanceListImageMembers/v2` | 读取镜像成员列表(OpenStack原生) | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/GlanceListImageSchemas/v2` | 读取镜像列表视图(OpenStack原生) | — | — |
| `IMS/GlanceListImages/v2` | 读取镜像列表(OpenStack原生) | — | — |
| `IMS/GlanceShowImage/v2` | 读取镜像详情(OpenStack原生) | `image_id: IMS.ImageId` ← [ECS/ShowServer/v2](hcloud.md#ecs) 的 `server.image.id` | — |
| `IMS/GlanceShowImageMember/v2` | 读取镜像成员详情(OpenStack原生) | `image_id: IMS.ImageId`、`member_id`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/GlanceShowImageMemberSchemas/v2` | 读取镜像成员视图(OpenStack原生) | — | — |
| `IMS/GlanceShowImageSchemas/v2` | 读取镜像视图(OpenStack原生) | — | — |
| `IMS/GlanceUpdateImage/v2` | 修改镜像配置：更新镜像信息(OpenStack原生) | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/ImportImageQuick/v2` | 导入镜像：镜像文件快速导入 | — | — |
| `IMS/ListImageByTags/v2` | 读取按标签查询镜像 | — | — |
| `IMS/ListImageMembers/v2` | 读取镜像成员列表 | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/ListImageTags/v2` | 读取镜像标签 | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/ListImages/v2` | 读取镜像列表 | — | — |
| `IMS/ListImagesTags/v2` | 读取租户所有镜像标签 | — | — |
| `IMS/ListOsVersions/v2` | 读取镜像支持的OS列表 | — | — |
| `IMS/ListTags/v2` | 读取按条件查询租户镜像标签列表 | — | — |
| `IMS/ListVersions/v2` | 读取版本列表(OpenStack原生) | — | — |
| `IMS/RegisterImage/v2` | 注册镜像 | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/ShowImageMember/v2` | 读取镜像成员详情 | `image_id: IMS.ImageId`、`member_id`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |
| `IMS/ShowImageQuota/v2` | 读取镜像配额 | — | — |
| `IMS/ShowVersion/v2` | 读取版本列表(OpenStack原生) | `version` | — |
| `IMS/UpdateImage/v2` | 更新镜像信息 | `image_id: IMS.ImageId`；缺 `image_id` → [IMS/ListImages/v2](hcloud.md#ims) | — |

## LTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LTS/ListAccessConfig/v2` | 读取日志接入 | — | — |
| `LTS/ListCharts/v2` | 读取日志流图表 | `log_group_id`、`log_stream_id`；缺 `log_group_id` → [LTS/ListLogGroups/v2](../common/hcloud.md#lts) | — |
| `LTS/ListHost/v2` | 读取主机信息 | — | — |
| `LTS/ListHostGroup/v2` | 读取主机组 | — | — |
| `LTS/ListTransfers/v2` | 读取日志转储 | — | — |
| `LTS/ShowAdminConfig/v2` | 读取日志汇聚开关 | — | — |
| `LTS/ShowAomMappingRule/v2` | 读取单个接入规则 | `rule_id` | — |
| `LTS/ShowAomMappingRules/v2` | 读取所有接入规则 | — | — |
| `LTS/ShowLogConvergeConfig/v2` | 读取组织成员汇聚配置 | `member_account_id` | — |
| `LTS/ShowMemberGroupAndStream/v2` | 读取组织成员日志组日志流 | `member_account_id` | — |

## RMS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `RMS/ListAllResources/v1` | 读取列举所有资源 | — | — |
| `RMS/ListRegions/v1` | 读取用户可见的区域 | — | — |
| `RMS/ListResources/v1` | 读取列举指定类型的资源 | `provider`、`type` | — |
| `RMS/ShowConfigurationAggregatorSourcesStatus/v1` | 读取指定资源聚合器聚合帐号的状态信息 | `aggregator_id` | — |
| `RMS/ShowResourceById/v1` | 读取单个资源 | `provider`、`resource_id`、`type` | — |
| `RMS/ShowResourceDetail/v1` | 读取帐号下的单个资源 | `resource_id` | — |
| `RMS/ShowResourceHistory/v1` | 读取资源历史 | `resource_id` | — |
| `RMS/ShowResourceRelations/v1` | 读取列举资源关系 | `resource_id` | — |
| `RMS/ShowResourceRelationsDetail/v1` | 读取列举资源关系详情 | `resource_id` | — |
| `RMS/ShowTrackerConfig/v1` | 读取记录器 | — | — |

## SMN

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `SMN/ListLogtank/v2` | 读取云日志 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](hcloud.md#smn) | — |
| `SMN/ListSubscriptions/v2` | 读取订阅者列表 | — | — |
| `SMN/ListSubscriptionsByTopic/v2` | 读取指定Topic的订阅者列表 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](hcloud.md#smn) | — |
| `SMN/ListTopicAttributes/v2` | 读取主题策略 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](hcloud.md#smn) | — |
| `SMN/ListTopicDetails/v2` | 读取主题详情 | `topic_urn`；缺 `topic_urn` → [SMN/ListTopics/v2](hcloud.md#smn) | — |
| `SMN/ListTopics/v2` | 读取主题列表 | — | — |
| `SMN/ListTopicsWithAssociatedResources/v2` | 读取主题列表及主题关联资源信息 | — | — |
