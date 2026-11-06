# 共享查询 · linux

首次使用本环境或工具不匹配时读 [linux](../../tools/linux.md)。缺输入才读 [Helper](../../helpers.md)。

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LINUX/os-release`<br>`cat /etc/os-release` | 读取发行版标识和版本 | 目标主机 | 读取数据；不 source 此文件 |
| `LINUX/kernel`<br>`uname -r` | 读取当前内核版本 | 目标主机 | 版本不等于补丁或漏洞结论 |
| `LINUX/identity`<br>`id` | 读取执行用户及组 | 当前会话 | 权限结论还需目标对象的访问检查 |
