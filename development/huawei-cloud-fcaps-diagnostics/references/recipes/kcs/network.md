---
status: draft
---

# 云服务器访问目标服务超时、拒绝连接或丢包，如何定位？

## Issue

“从云服务器访问某个地址不通，或者只有部分请求超时。”需要定位受影响的访问方向、路径和故障边界。

## Environment

- 华为云 ECS、VPC；仅在路径实际涉及时检查 EIP、ELB、VPN 等资源。
- 主机为 Linux 或 Windows；容器业务另绑定 Kubernetes context、namespace 和对象身份。

## Resolution

1. 确认源、目的、协议、端口、方向、时间窗，以及失败是否仅发生在名称解析、建连或业务请求阶段。
2. 用 [ECS/ListServerInterfaces/v2](../../commands/configuration/hcloud.md#ecs) 定位云网卡，按 [H-port](../../helpers.md#h-port)、[H-subnet](../../helpers.md#h-subnet) 和需要时的 [H-eip](../../helpers.md#h-eip) 解析关联资源；再从[网络配置分册](../../commands/configuration/hcloud-network.md)选择安全组、子网、路由及实际路径上的查询。
3. 主机可访问时读取 [Linux 地址与路由](../../commands/configuration/linux.md)或 [Windows 网卡与路由](../../commands/configuration/windows.md)，结合对应[Linux 防火墙](../../commands/security/linux.md)或 [Windows 防火墙](../../commands/security/windows.md)规则。云端放行不能代替主机侧核对。
4. 在已授权范围内选择有限探测：[LINUX/dns-query](../../commands/fault/linux.md)、[LINUX/icmp-probe](../../commands/fault/linux.md) 或 [WINDOWS/tcp-probe](../../commands/fault/windows.md)。逐跳结果按[链路测试指引](../../documents/huaweicloud.md#f-故障)解释；抓包须另外核对采集范围与开销。
5. 容器服务按需查 [KUBERNETES/endpoints](../../commands/configuration/kubernetes.md) 和 [KUBERNETES/networkpolicy](../../commands/security/kubernetes.md)。将已确认的边界及缺口写入报告；修复后从原来源验证原协议、端口和业务请求。

## Cause

尚未确定。中间跳无响应、ICMP 不通、端口连通或端点存在均不能单独证明业务路径的根因或健康状态。
