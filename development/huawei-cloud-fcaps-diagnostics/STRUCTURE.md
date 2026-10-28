# 工程结构

一个技能入口。FCAPS 为主骨架，工具／目标系统为分册维度。

| 位置 | 唯一职责 |
| --- | --- |
| SKILL.md | 目标、通用规则、按需路由与输出要求 |
| references/commands/index.md | FCAPS 类别与环境导航 |
| references/commands/<类别>/<工具>.md | 命令模式、观测、输入与约束的四列契约 |
| references/tools/<工具>.md | 工具适用条件、帮助发现与执行要求 |
| references/helpers.md | 缺失输入的类型、生产者、选择条件与输出绑定 |
| references/triage.md | 现象不明时选择事实类别 |
| references/recipes/index.md | 场景到 KCS 文章的索引 |
| references/recipes/kcs/ | Issue、Environment、Resolution、Cause 四字段文章 |
| references/documents/index.md | 文档读取与来源核对规则 |
| references/documents/huaweicloud.md | FCAPS 主题到官方来源及契约的指引 |
| references/documents/catalog.jsonl | 仅含元数据，按关键词搜索命中项 |

F/C/A/P/S 对应 fault/configuration/accounting/performance/security；common 放共享查询。没有命令的类别／环境组合不建空文件。hcloud 网络配置与主机安全分别成册。

一条命令只定义一次，其他入口只链接。hcloud ID 保留服务／操作／版本；系统命令使用环境／模式 ID。工具入口不复制契约；已知 ID 或文章可直接读取，依赖与文档按当前步骤加载。

KCS 遵循 [Article Structure](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/040/010/020)（2026-10-28 核对）：Issue 用请求者语言，Environment 写适用条件，Resolution 用编号步骤链接契约，Cause 只写已确认原因，未知或不适用时说明。统一保留四字段与 `status: draft`；验证边界集中在场景索引。

本地 QA 位于仓库的 `qa/development/huawei-cloud-fcaps-diagnostics/`，历史验证归档在其 `verification/` 下，不随技能分发。维护时先核验帮助及适用查询，再从最终契约复核；结果绑定相应修订，历史通过不沿用为当前修订通过。无适用环境时保留受阻。

文档正文、图片、真实目标、凭据和原始日志留在技能外。文档索引由 QA 的 `documents.py` 生成与检查；补充来源和来源散列分别由 `documents-links.json`、`documents-source.json` 管理。Markdown／HTML 共用文档身份；读取规则仅在文档入口定义。
