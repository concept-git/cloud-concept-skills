# KCS Foundry

从工单、社区和经验库中提炼问题解决方案，形成可追溯、可复用的 KCS 知识卡。

## 当前状态

已建立项目目录，并下载 OpenKB 上游源码；KCS 提炼流程尚未实现。

## 目录

```text
kcs-foundry/
├── README.md
└── vendor/
    ├── openkb/              # 上游源码快照，保留许可证及来源信息
    └── openkb.source.json   # 来源、分支、提交与获取时间
```

## OpenKB 来源

- 上游：https://github.com/VectifyAI/OpenKB
- 源码目录：`vendor/openkb/`
- 获取口径：上游默认分支 `main` 的最新提交，浅克隆（depth=1）。
- 固定提交：`ff54396e575ee6feb0113b631a34caa082b441cc`
- 提交时间：2026-07-22T11:44:01+08:00
- 许可证：Apache-2.0，原文保留在 `vendor/openkb/LICENSE`。

本次仅下载源码并记录来源，尚未安装依赖或启动服务。上游代码与后续 KCS Foundry 实现分目录维护。
