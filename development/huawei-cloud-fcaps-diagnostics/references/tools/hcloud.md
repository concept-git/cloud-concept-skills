# hcloud

使用已配置的华为云 KooCLI。首次构造调用查 `hcloud Service Operation/version --help`；同版本已查帮助可复用。调用保留完整操作版本；它与 HTTP 路径版本可能不同。

- 作用域采用已确认的 profile、region、IAM project、目标资源与时间窗。用 `--cli-profile`、`--cli-region` 选择配置；API 的 `project_id` 另按帮助填写。IAM project 与企业项目分别处理。
- `configure test` 只检查配置格式；真实认证看 API 响应。退出码为 0 时仍检查错误对象。stdout 可能在 JSON 前带升级提示；仅剥离已识别提示，未知前缀仍报错，不自动升级 CLI。
- 数组参数使用 `.1`、`.2`；分页、枚举与时间单位按所选操作帮助。毫秒时间戳与 ISO 8601 时间不互换。
- GET 也可能发起检测，POST 也可能只查询。同步、检测、安装、发送和生成登录地址按实际影响处理；已有任务直接查询结果。
- 资源衔接按 Helper 的类型、选择条件和输出字段；多结果先定位目标。异步请求被接受不等于任务完成。

## 工具入口

下表命令接在 `rtk proxy hcloud` 后。需要核验历史时查[验证记录](../verification/cloud.md#cli-元工具)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `version` | 读取 CLI 版本 | — | — |
| `configure test` | 检查本地配置格式 | 已有配置 | 不证明认证有效 |
| `configure list` | 读取配置项列表 | — | — |
| `configure show` | 读取指定配置项 | 已有 profile | — |
| `configure set` | 修改本地配置 | 目标 profile | 按授权范围配置认证与作用域 |
| `log show` | 读取 CLI 日志配置 | — | — |
| `log set` | 修改本地日志配置 | — | 按 help 选择级别 |
| `meta download` | 下载并修改元数据缓存 | — | 更新后重新核对所用操作的 help |
| `meta clear` | 删除本地元数据缓存 | — | 后续需重新获取帮助 |
| `update` | 修改本机 CLI 安装版本 | — | 更新后重新核对所用操作的 help |

## 诊断选项

以下选项附加到所选命令，详细格式查 help。

| 选项 | 用途与约束 |
| --- | --- |
| `--debug` | 输出调用信息；原命令仍执行。 |
| `--dryrun` | 预览请求；跳过目标业务 API，仍可能读取元数据或项目资料。 |
| `--skeleton` | 生成 JSON 入参骨架。 |
| `--cli-profile`、`--cli-region`、`--cli-project-id` | 选择配置、区域与默认项目。API 的 `project_id` 另按操作 help 填写。 |
| `--cli-domain-id`、`--cli-x-project-id` | 指定账号或鉴权项目；按 API 要求使用。 |
| `--cli-endpoint` | 排查端点选择；使用官方服务端点。 |
| `--cli-connect-timeout`、`--cli-read-timeout`、`--cli-retry-count` | 设置连接、读取超时与重试；重试不会修复权限拒绝。 |
| `--cli-query`、`--cli-output` | 筛选返回字段与显示格式；不改变服务端查询范围。 |
| `--cli-waiter` | 轮询原 API；使用前确认原操作只读。 |

共享查询见[共享分册](../commands/common/hcloud.md)。

## 维护入口

操作形式：`hcloud Service Operation/version`；这是华为云 KooCLI，不是 Hetzner 的同名工具。通用约束见[主入口规则](../../SKILL.md#安全规则)。

[A 计量计费／hcloud](../commands/accounting/hcloud.md) · [共享查询／hcloud](../commands/common/hcloud.md) · [C 配置／hcloud-network](../commands/configuration/hcloud-network.md) · [C 配置／hcloud](../commands/configuration/hcloud.md) · [扩展／hcloud](../commands/extensions/hcloud.md) · [F 故障／hcloud](../commands/fault/hcloud.md) · [P 性能／hcloud](../commands/performance/hcloud.md) · [S 安全／hcloud-host](../commands/security/hcloud-host.md) · [S 安全／hcloud](../commands/security/hcloud.md)
