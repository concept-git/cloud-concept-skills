# 工程结构

一个技能入口。FCAPS 是主骨架，工具／目标系统是分册维度。

| 位置 | 唯一职责 |
| --- | --- |
| SKILL.md | 目标、安全规则、反幻觉规则、易错点和按需路由 |
| references/commands/<类别>/<工具>.md | 具体命令模式的四列契约 |
| references/tools/<工具>.md | 工具适用条件、帮助发现、分册导航 |
| references/documents/index.md | 文档读取条件、来源核对与回退 |
| references/documents/huaweicloud.md | FCAPS 主题到官方文档及契约的指引 |
| references/documents/catalog.jsonl | 合并归档与精选来源的元数据；按关键词读取命中项 |
| references/execution.md | 执行通道与华为云适配边界 |
| references/helpers.md | 输入类型、生产者、选择条件、输出绑定 |
| references/verification/<环境>.md | 独立、带日期和范围的验证摘要 |
| references/triage.md、report.md | 分诊与结果字段 |
| references/recipes/ | 原九项规划，每项仅一至两句 |

F/C/A/P/S 分别为 fault/configuration/accounting/performance/security。common 保留共享发现；extensions 保留已有扩展。hcloud 的网络配置和主机安全继续分册。没有命令的类别／系统组合不建空文件。

维护 hcloud 时先读 references/tools/hcloud.md，契约位于 commands/*/hcloud*.md。一条命令只定义一次；其他入口只链接。完整操作 ID 保持版本，系统命令用环境／模式 ID，不给选项虚构 API 版本。

入口→FCAPS 类别及环境→所需行；只有输入缺失、通道未确认或需要实测范围时才读 Helper、通道或验证摘要。已知 ID 可直接定位，无强制加载链。工具入口不复制契约。

以当前技能说明、命令契约与文档索引为准。测试代码位于 qa/development/huawei-cloud-fcaps-diagnostics/；原始下载、日志和临时报告放到仓库外的临时目录。运行文档不包含真实目标、凭据或原始日志。

先执行帮助及适用查询，再按事实编写；无适用环境的条目保留受阻。写入后从最终契约读取命令复核，结果绑定契约摘要。一次成功不能代表其他系统、集群或全部参数。

文档正文和图片留在技能外。索引不是当前环境的观测，快照日期不是在线可用性保证。生成与检查使用 QA 的 documents.py；补充来源登记在 QA 的 documents-links.json，来源散列保存在 documents-source.json。归档和补充核验各自保留日期；正文变化只触发受影响条目的审阅，不自动修改命令。Markdown／HTML 共用一个文档身份，读取规则只在 documents/index.md 定义。
