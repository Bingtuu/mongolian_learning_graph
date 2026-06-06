---
title: 蒙古语学习知识库
type: index
---

# 蒙古语学习知识库

> 基于 LLM Wiki 理念构建的蒙古语（新蒙文/西里尔）学习知识库。

## 仓库结构

```
├── wiki/              ← Obsidian 知识库核心（所有知识页面）
│   ├── index.md       ← 知识库总索引与快速导航
│   ├── log.md         ← 操作日志
│   ├── concepts/      ← 语言学概念
│   ├── entities/      ← 语言元素（字母、词类）
│   ├── rules/         ← 语法规则
│   ├── examples/      ← 主题例句集
│   ├── exercises/     ← 练习题
│   ├── comparisons/   ← 易混淆知识对比
│   ├── syntheses/     ← 合成速查与路线图
│   └── sources/       ← 源材料摘要
├── raw/               ← 原始学习材料（只读，PDF 等）
│   ├── MANIFEST.md    ← 源材料清单（LLM 可发现所有 raw 资源）
│   └── books/         ← 教材扫描件（已排除在版本控制外）
└── .project/          ← 项目维护文件（Obsidian 默认隐藏）
    ├── docs/          ← 规范文档（CLAUDE.md、AGENTS.md、README.md）
    ├── scripts/       ← 维护脚本（review、lint、fix）
    └── reports/       ← 生成的检查报告（已排除在版本控制外）
```

> **Obsidian 用法**：用 Obsidian 打开本仓库根目录。知识库核心内容位于 `wiki/`，`.project/` 以点开头，Obsidian 默认不显示，保持知识库视野干净。

## 进入知识库

👉 [**wiki/index.md**](wiki/index.md) — 知识库总索引与快速导航

## 工作流

- **收录 (Ingest)**：将 `raw/` 中的新材料整理为 `wiki/` 中的结构化知识
- **查询 (Query)**：基于已有知识回答问题
- **检查 (Lint)**：扫描断裂链接、孤立页面、内容矛盾

## 规范文档

- `.project/docs/CLAUDE.md` — AI 编码规范与工作流
- `.project/docs/AGENTS.md` — Agent 执行指令速查
- `.project/docs/README.md` — 项目介绍与来源说明

## 最近更新

- 2026-06-01 — Peace Corps Unit 3–4 提取完成，练习层补齐至阶段6，批量修复 87 个 needs-check 页面
- 2026-05-31 — 全库 Review 修复（270 问题 → 0），建立知识库运营规范
- 2026-05-31 — 初始化知识库结构，创建 25+ 页面
- 2026-05-31 — 收录 *Modern Mongolian: A Course-Book* (John Gaunt, 2004)
