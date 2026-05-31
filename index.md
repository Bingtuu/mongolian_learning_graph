---
title: 蒙古语学习知识库
type: index
---

# 蒙古语学习知识库

> 基于 LLM Wiki 理念构建的蒙古语（新蒙文/西里尔）学习知识库。

## 项目结构

```
├── raw/          ← 原始学习材料（只读）
├── wiki/         ← 知识库核心（LLM 维护）
│   └── index.md  ← 知识库总索引
├── schema/       ← 模式定义与工作流
│   └── AGENTS.md
└── prd/          ← 产品需求文档
```

## 进入知识库

👉 [**wiki/index.md**](wiki/index.md) — 知识库总索引与快速导航

## 工作流

- **收录 (Ingest)**：将 `raw/` 中的新材料整理为 `wiki/` 中的结构化知识
- **查询 (Query)**：基于已有知识回答问题
- **检查 (Lint)**：扫描断裂链接、孤立页面、内容矛盾

## 最近更新

- 2026-05-31 — 初始化知识库结构，创建 25+ 页面
- 2026-05-31 — 收录 *Modern Mongolian: A Course-Book* (John Gaunt, 2004)
