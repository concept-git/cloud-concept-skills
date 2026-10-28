# IAM 范围与权限

错误处理见 `gotchas.md` G01。结合当前帮助、403响应和API Explorer确定操作、账号／客户范围及被拒绝的权限，由用户管理员授权，不自行提权。

| 工作流 | 权限范围 |
| --- | --- |
| 询价 | 只读 BSS 询价／字典，包含 `ListUsageTypes`；通常为 `bss:order:view` 加对应只读权限 |
| 项目发现 | IAM `KeystoneListAuthProjects` / `KeystoneListProjects`；项目选择按 `gotchas.md` G02 |
| 开通 | 白名单服务的创建权限；依赖查询仅需只读权限 |
| 伙伴代客报价 | 客户授权 Token；项目选择按 `gotchas.md` G02 |

服务权限定义随账号／站点／版本变化，以当前定义为准。读取失败补对应读取权限，不扩大为写权限；客户授权失败停止该范围。历史账单和余额按 `../SKILL.md` 分流。
