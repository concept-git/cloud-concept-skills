# KooCLI 可用性与配置

hcloud由用户本机安装配置。检查前读 `gotchas.md` G01–G02；凭证处理按G12。

## 可用性检查

1. `hcloud version` 仅确认本机CLI版本。
2. 需要连接检查时，读 `IAM KeystoneListAuthProjects --help` 后用 `--cli-region=cn-north-1 --cli-output=json` 查询。成功仅证实本次IAM连接、鉴权及读取获准；BSS询价、创建权限另验。询价项目按G02选，不由端点区域推断。
3. 仅当IAM调用明确报缺配置时查 `hcloud configure list`，否则跳过。

报告版本、IAM结果及未验证范围；不列项目清单或domain/project ID，不推断凭证类型。

## 用户本机配置

按[官方安装指南](https://support.huaweicloud.com/qs-hcli/hcli_02_003.md)选系统／架构安装包，优先复用profile。缺配置由用户运行 `hcloud configure set`，凭证本机输入。

命令不存在查PATH；下载失败核对官方链接；连接错误按网络／代理证据排查。
