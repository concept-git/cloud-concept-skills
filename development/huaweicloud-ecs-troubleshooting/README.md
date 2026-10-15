# huaweicloud-ecs-troubleshooting

**Status: In development — structure draft only, not ready to install or use.**

**状态：开发中，仅完成目录结构设计，尚不能安装或用于实际排障。**

This draft is isolated under `development/`, outside the released English and
Simplified Chinese skills in `skills/en/` and `skills/cn/`. It is not registered in
the installable skill catalog or published to ClawHub.

计划支持华为云 ECS Linux 实例及其关联网络、存储、监控、审计与备份服务的故障定位。

- 已完成：参考结构分析、八类故障现象划分、文件职责与跨服务边界设计。
- 当前内容：15 个空骨架文件（`SKILL.md` 与 `references/` 下的 14 个文件）。
- 尚未完成：技能 frontmatter、诊断指令、云 API/CLI 契约、采集逻辑与行为验证。

结构、核心概念及简要流程见 [STRUCTURE.md](STRUCTURE.md)。本文件和结构说明是开发文档，未来不随技能运行载荷安装。

进入正式技能目录前，应完成实现、核实华为云接口与权限、建立中英文版本、补充 QA，
并通过仓库验证后再登记正式目录。此开发稿不单独声明发布版本。
