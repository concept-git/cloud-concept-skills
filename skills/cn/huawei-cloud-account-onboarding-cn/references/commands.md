# 命令合同附录

本文件只保留命令合同：用途、模板、响应字段、取值映射与限制。实体与状态语义看 `concepts.md`，行为与红线看 `SKILL.md`。

## 命令格式标准

**服务名恒为 `BSS`**，**区域恒为 `cn-north-1`**（BSS 为全局端点，勿用 profile 默认 region 替代）。

```bash
hcloud BSS <Operation> --cli-region=cn-north-1 --cli-output=json
```

两条命令都**无业务参数**，凭当前 profile 身份识别账号；不要传 `customer_id`、`domain_id` 或分页参数。

### 凭证前提

KooCLI 需要**已配置 profile**（用户自行 `hcloud configure set`）。只导出 `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` 环境变量**不生效**，会报 `[USE_ERROR]配置文件中不存在配置项`。无 profile 时停下，请用户配置，不代为写入凭证。

## 全局约束

- **命令白名单** —— 仅 `ShowRealNameAuthStatus` 与 `ShowRealNameAuthQrCode` 两条。
  其余实名相关 operation 均**不在本技能范围**：`CreatePersonalRealnameAuth`、
  `CreateEnterpriseRealnameAuthentication`、`ChangeEnterpriseRealnameAuthentication`
  是写操作，`ShowRealnameAuthenticationReviewResult` 仅限伙伴凭证调用。
- **仅主账号** —— IAM 子用户调用会失败；失败时说明须用主账号凭证，不代换凭证。
- **流控 5 次/秒** —— 两条命令各自限速（维度：源 IP、API、ParentUid）。轮询间隔不得低于 2 秒；命中 `429` / `APIGW.0308` 时退避重试，不加密度。
- **取码必须先查状态** —— 取码命令自身不校验实名状态，已实名账号同样返回可用二维码地址（实测）。门禁由本技能承担。
- **不落盘** —— `qr_code_url` 含一次性 `ticket`，只渲染给当次用户；不写文件、不写日志、不进任何持久产物。

## account_onboarding

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ShowRealNameAuthStatus` | 查账号实名状态与类型 | - | 首查恒为此条；也用于取码后的轮询 |
| `ShowRealNameAuthQrCode` | 取人脸认证二维码地址 | - | 仅在状态为「未实名」且用户在手机旁时调用 |

### 响应字段

`ShowRealNameAuthStatus`

| 字段 | 类型 | 取值 | 含义 |
| --- | --- | --- | --- |
| `verified_status` | Integer | `-1` | 未实名认证 → 需引导取码 |
| | | `0` | 实名认证审核中 → 等待，不重复取码 |
| | | `1` | 实名认证不通过 → 控制台看原因，不代改材料 |
| | | `2` | 已实名认证 → 短路，不取码 |
| `verified_type` | Integer | `0` | 个人实名认证 |
| | | `1` | 企业实名认证 |
| | | `null` | `verified_status=-1` 时不返回 |

`ShowRealNameAuthQrCode`

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `qr_code_url` | String | 人脸认证入口地址（`auth.huaweicloud.com` 域，含一次性 `ticket`）。**仅限单次使用，扫描后即失效；未在 10 分钟内扫描自动作废。** |

### 命令模板

#### `ShowRealNameAuthStatus`

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 --cli-output=json
```

只取状态位时用 `--cli-query` 收窄输出（返回裸整数）：

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 --cli-output=json --cli-query=verified_status
```

#### `ShowRealNameAuthQrCode`

```bash
hcloud BSS ShowRealNameAuthQrCode --cli-region=cn-north-1 --cli-output=json --cli-query=qr_code_url
```

输出是带引号的地址一行，去引号后直接喂给渲染脚本：

```bash
npx tsx scripts/render-qr.ts "$(hcloud BSS ShowRealNameAuthQrCode \
  --cli-region=cn-north-1 --cli-output=json --cli-query=qr_code_url | tr -d '"')"
```

#### 轮询至实名落地

用 KooCLI 内置 waiter，不要自写 sleep 循环：

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 --cli-output=json \
  --cli-waiter="{\"expr\":\"verified_status\",\"to\":\"2\",\"timeout\":600,\"interval\":5}"
```

`timeout` 上限 600 秒（KooCLI 硬限），`interval` 取值 2–10 秒。二维码 10 分钟作废，故 600s 超时与凭据寿命对齐：waiter 超时即二维码大概率已作废，此时**先问用户**是否重新取码，不自动重发。

轮询结束后另跑一次状态查询确认终态（waiter 超时不区分「仍未实名」与「转入审核中」）。

## 错误与失败路由

| 现象 | 处理 |
| --- | --- |
| `[USE_ERROR]配置文件中不存在配置项` | 请用户 `hcloud configure set` 配置 profile；不代写凭证 |
| `429` / `APIGW.0308` | 命中流控，退避后重试，间隔不低于 2 秒 |
| 子用户调用失败 | 说明仅主账号可调用；不代换凭证 |
| `verified_status=1`（不通过） | 给控制台实名认证页路径，让用户自查审核意见；本技能不查审核细节、不代改材料 |
| 企业认证 / 证件认证 / 银行卡认证 / 认证变更 | 均不在本技能通道，指路控制台「账号中心 → 实名认证」，不代办 |
| 非华为云实名 / 通用 KYC | 说明超出范围，不取证 |
