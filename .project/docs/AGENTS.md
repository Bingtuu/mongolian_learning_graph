# 蒙古语知识库 Agent 指令

> **本文件已被 CLAUDE.md 整合。**
> **详细规范、模板、流程请参见项目根目录的 `CLAUDE.md`。**
> **本文件仅保留极简速查，供快速唤起上下文使用。**

你是蒙古语学习知识库的维护助手。工作是将学习材料整理为结构化的知识网络。

## 目录速查

```
raw/          — 原始材料（只读，绝不修改）
wiki/         — 知识库（全权负责）
  index.md    — 总索引（创建/更新页面后必须更新）
  log.md      — 操作日志（每次操作必须记录）
  concepts/   — 抽象概念
  entities/   — 具体语言元素
  rules/      — 语法规则 + 运营规则
  sources/    — 源材料摘要
  examples/   — 例句集
  comparisons/— 对比页
  syntheses/  — 合成速查
  exercises/  — 练习题
schema/       — 本文件
```

## 速查要点

### Frontmatter（所有页面必须）

```yaml
---
title: 中文标题
type: concept|entity|rule|comparison|source|example|synthesis|exercise|index|log
category: 分类
level: fundamental|beginner|intermediate|advanced
related: [[页面A]], [[页面B]]
prerequisites: [[页面X]]
source: [[源材料]]        # 知识页必需
status: draft|needs-check|needs-ocr|reviewed  # 知识页必需
---
```

### 例句格式（强制）

```markdown
> Би эмч биш, багш.
> (我不是医生，是老师。)
> — [[日常问候]] | 语法点: [[否定式]]
```

### 工作流口诀

| 场景 | 操作 |
|------|------|
| 收录源材料 | 检查 sources/ → 检查 OCR → 已有页面? 合并 : 新建 → 更新 index + log |
| 更新页面 | 读取 → 判断补充/修正/重写 → 更新 source/status → 记录 log |
| 检查知识库 | lint 脚本 → 断链/孤立/缺元数据/格式/矛盾/混字/过期 |
| 发现冲突 | 标记差异 → 不擅自裁决 → status → needs-check |

### 九大原则（优先级排序）

1. 单一事实来源（SSOT）— 禁止重复页面
2. 从不修改 `raw/`
3. 所有页面 Markdown 格式
4. 积极使用 [[双向链接]]
5. 保持 frontmatter 完整
6. 记录操作日志
7. 中文为主，蒙古语为辅
8. 标记来源冲突
9. 先检查后提交

---

**完整规范 → `CLAUDE.md`**
