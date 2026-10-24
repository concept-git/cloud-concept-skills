# 执行通道

先确认目标身份、OS 和授权，再选择已可用的通道。通道就绪不代表所执行命令无副作用。

| 通道 | 前置事实 | 执行与核对 |
| --- | --- | --- |
| 本机或 SSH | 目标主机、账号、端口、主机密钥已确认 | 在目标内核验 OS 和工具；逐参数转义；保留退出状态和完整错误；凭据不写脚本 |
| 华为云 COC | 目标实例及 UniAgent 状态已确认 | 先查 [COC 资源](commands/configuration/hcloud.md#coc)；核对现有脚本内容和参数后才执行；按任务 ID 查询结束状态与输出 |
| Windows 远程会话 | 目标 Windows、会话类型及模块已确认 | 在远端执行 PowerShell 对象查询；远程链路成功不证明 cmdlet 成功 |
| Kubernetes API | 目标 context、身份和作用域已确认 | 用显式 context 查询；修改 kubeconfig、创建资源、安装组件属于额外操作 |

COC 执行及任务查询见[故障分册](commands/fault/hcloud.md#coc)。阿里云云助手参数和公共脚本 ID不能直接替换成 COC 参数；无已就绪通道时记录缺口，不安装 Agent 补齐验证。
