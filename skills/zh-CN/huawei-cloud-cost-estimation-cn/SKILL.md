---
name: huawei-cloud-cost-estimation-cn
description: >-
  估算华为云下单前费用，通过 hcloud 开通白名单内资源，并引导用户通过控制台处理退订。
  适用于华为云询价、预算、资源创建、退订指引或 hcloud 可用性检查。
compatibility: 需要 hcloud KooCLI 7.2+、对应的 IAM 权限和网络连接；依赖由用户自行安装配置
metadata:
  language: zh-CN
  translation_of: huawei-cloud-cost-estimation
  author: concept-git
  version: "3.2.7"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/zh-CN/huawei-cloud-cost-estimation-cn
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云询价与资源开通

社区维护，非华为云官方技能。用当前 hcloud 响应给出价格和状态，参数以当前命令帮助为准。

## 先判断用户要做什么

- hcloud 是否可用：读 `references/cli-installation.md` 的可用性检查，只报告实际验证过的能力。
- 询价、预算、比价：进入“报价”。
- 购买、创建资源：进入“开通”。
- 退订或停止使用：读 `references/lifecycle/concepts.md` 的退订说明，引导用户在控制台操作；不生成或执行退订命令。
- 历史账单、余额、对账：转费用中心或账单只读技能。其他云和白名单外操作，说明范围并给出相应控制台入口。

## 报价

先读 `references/pricing/commands.md`。按以下四步处理：

1. **问清需求。** 确认服务、区域、规格、数量、计费方式，以及周期或用量。需要容量的产品还要确认容量。把缺项和有实质区别的候选一次问清；用户已授权你选择时，按其预算和用途选择并说明依据。仅询价时，可说明后使用 Linux、空 AZ、分期方式 NA；不替用户默认计费方式或使用时长。
2. **找到对应规格。** 先查服务对应的资源类型，再按区域和计费方式查规格。保留候选的服务、资源类型、区域、计费模式和规格编码；同名规格不能跨模式或跨区域复用。按需产品再查计费因子和单位；容量规则、分页方法见询价说明。
3. **查询并核对。** 包周期与按需使用各自的询价接口。请求必须与已选规格、周期／用量、数量及容量一致。产品的容量或单位含义尚未明确时，停止该项询价并标为待核实。分开记录返回事实、报错和原因假设；有金额不等于报价已核实，也不代表能开通。
4. **把价格说清楚。** 按项列出服务、规格、区域、计费方式、数量×周期或用量和金额，核对合计、币种及未包含项。只展示响应中的折扣，注明“非最终账单”；只有配置、计费单位和响应均已核实的项目才能计入小计；待核实项即使返回金额也单列，部分小计不称完整预算；正式报价按询价说明中的交付规则处理。

## 开通

先读 `references/lifecycle/concepts.md` 和 `references/lifecycle/commands.md`。依次完成：

1. **核对操作。** 确认创建操作在白名单中，运行该操作的 `--help`。帮助报错或没有参数定义时停止。
2. **核验配置。** 用只读接口核实目标区域、可用区、规格的售卖状态和计费支持，以及账号限制、镜像、网络等依赖。查到规格或价格只完成了部分核验；不能直接说“有货”。
3. **核对费用。** 对准备创建的完整配置询价，包含关联付费资源。无法可靠询价时，说明“价格未知且可能收费”，取得额外同意；这不能代替可开通性检查。
4. **检查请求。** 给完整命令加全局 `--dryrun`，检查实际构造的请求。干跑失败先修正；干跑成功只说明请求能在本地构造。
5. **确认并执行。** 展示配置、数量、计费方式、周期、费用及执行顺序，取得用户对该配置的明确确认。另行正式调用，只移除 `--dryrun`。多条命令按顺序执行，失败后停止写入，报告各项状态。

配置改变时，重新核验、询价、干跑和确认。创建失败后先只读排查，不循环换规格试买，不自动回滚。返回任务或订单编号时先说明“已受理”，再只读核对最终状态。

## 沟通与按需查阅

用中文常用说法，先说结论，再说明依据和下一步；优先短段落和分项，用户指定格式时按其要求。只读步骤在需求明确时连续执行，长流程简短汇报进展；仅在缺少影响选择的信息或需要费用、写入确认时停下询问。

所有 BSS 调用使用 `--cli-region=cn-north-1`，部署区域仍填用户选择的区域。不接收聊天中的 AK、SK、Token，不在输出或日志中展示凭证。

- hcloud 不可用或需配置：读 `references/cli-installation.md`，让用户自行处理。
- 403 等权限问题：读 `references/iam-policies.md`。
- 需要核对字段关系：读 `references/pricing/rfq-models/rfq-core.yml` 及当前计费方式对应的模型；仅查询公共维度时只读核心文件。
