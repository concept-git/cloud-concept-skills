# 开通核验

按 `../../SKILL.md` 主流程执行；陷阱和失败处理集中在 `../gotchas.md` G07–G12。准备创建时在 `commands.md` 找到所选操作及依赖，再读明确版本的当前帮助。

## ECS 售卖与依赖

用 `ECS/ListFlavors` 查询目标规格／AZ，保留 `id`、CPU、内存及相关 `os_extra_specs`。

| 检查项 | 规则 |
| --- | --- |
| 售卖状态 | `cond:operation:az` 为目标 AZ 状态，`cond:operation:status` 为区域状态；优先级见 G08。`normal/promotion`：商用；`abandon`：下线；`sellout`：售罄；`obt/obt_sellout`：公测。 |
| 计费 | `cond:operation:charge` 中 `period` 为包周期，`demand` 为按需；官方约定字段缺省时两者均支持。 |
| 补充售卖证据 | `ListFlavorSellPolicies` 保留规格、AZ、`sell_mode`、`sell_status` 和账号限制。 |
| 依赖 | 核实项目／区域、配额、镜像架构／状态／最小磁盘、磁盘支持、子网归属／状态／可用 IP、安全组访问权限／规则、登录方式。 |

依据：[ECS 扩展字段](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212656.md)。明确不兼容、售罄或权限受限时停止，未解决的条件如实说明。

## 选择登录方式

获授权时使用适合的已有密钥对，核实用户能使用其私钥但不读取私钥。包周期 ECS 密钥登录按当前帮助补齐 `server.metadata.op_svc_userid` 等关联字段。密码登录先按 G12 处理，再准备请求。

## 退订与停用

引导用户在控制台操作，不生成或执行退订／删除命令。

- 包周期：费用中心 → 订单管理 → 云服务退订（或“退订与退换货”）。
- 按需：对应资源的服务控制台 → 备份／迁移后删除。

提交前按控制台预览与[官方规则](https://support.huaweicloud.com/usermanual-billing/unsubscription_topic_2000010.md)，核对账号、资源、关联资源、退款、手续费及退款去向。
