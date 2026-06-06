# 蒙古语学习知识库 (Mongolian Learning Graph)

> 一个基于 **LLM Wiki** 理念构建的 Obsidian 知识库，面向中文母语者的蒙古语（新蒙文/西里尔）学习项目。
> 本知识库由 **人 + LLM 协作维护**：LLM 负责所有的总结、交叉引用和页面维护工作，你负责策划源材料和提出对的问题。

---

## 设计理念：LLM Wiki

本项目遵循 Andrej Karpathy 提出的 **LLM Wiki** 模式——一种利用大语言模型增量式构建和维护持久化知识库的架构。

### 与 RAG 的核心差异

传统 RAG 每次查询时从原始文档中检索相关片段再生成答案，没有知识积累。问一个需要综合五份文档的微妙问题，LLM 每次都要重新找和拼凑。

LLM Wiki 的思路不同：知识被**预先编译**为结构化的互联页面，而不是在查询时临时拼凑。跨引用已经建立，矛盾已经标记，综合已经反映所有已读内容。每添加一份新源材料，知识库就变得更丰富——它**持续复合增长**，而不是每次重新推导。

### 三层架构

```
raw/          ← 原始源材料（不可变层）
  │              LLM 读取但不修改
  ▼
wiki/         ← 知识层（LLM 全权维护）
  │              70+ Markdown 页面，[[双向链接]]互联
  ▼
schema/       ← 模式定义（.project/docs/CLAUDE.md）
                 定义工作流、规范、操作纪律
```

### 人机协作分工

| 谁 | 做什么 |
|------|--------|
| **你（人类）** | 筛选源材料、提问、指导分析方向、审阅 LLM 产出、决定学习路径 |
| **LLM（AI 助手）** | 总结教材、交叉引用、页面维护、格式检查、日志记录——所有"文书工作" |

详细工作流规范 → [.project/docs/CLAUDE.md](.project/docs/CLAUDE.md)

---

## 知识库架构

### 目录结构

```
mongol_learning/
├── raw/                    # 原始学习材料（只读，不入版本控制）
│   ├── MANIFEST.md         # 源材料清单（LLM 可通过它发现所有 raw 资源）
│   └── books/              # PDF 教材、扫描版语法书
├── .project/
│   ├── docs/
│   │   ├── CLAUDE.md       # 唯一 schema 规范（AI 工作流定义）
│   │   └── AGENTS.md       # 极简唤起标记
│   ├── scripts/            # 维护脚本（lint、review、fix）
│   └── reports/            # 检查报告（已排除在版本控制外）
├── wiki/                   # 核心知识网络（全部 Markdown）
│   ├── index.md            # 总索引与学习路径
│   ├── log.md              # 操作日志（每次操作必记录）
│   ├── concepts/           # 抽象语言学概念（元音和谐律、黏着语、SOV 语序等）
│   ├── entities/           # 具体语言元素
│   │   ├── alphabet/       # 字母与发音
│   │   └── parts-of-speech/# 词类（名词、动词、数词、副词等）
│   ├── rules/              # 语法规则（变格、时态、否定、领属等）
│   ├── examples/           # 主题例句集（问候、家庭、购物、旅行等）
│   ├── exercises/          # 阶段练习（阶段1–6 + 专项练习）
│   ├── comparisons/        # 易混淆知识点对比
│   ├── syntheses/          # 合成速查（路线图、速查表、句型模板）
│   └── sources/            # 源材料摘要与收录进度
└── README.md               # 本文件
```

### 页面规范

每张知识卡片都包含结构化 YAML frontmatter，使 Dataview 等工具可以跨页面查询：

```yaml
---
title: 中文标题
type: concept|entity|rule|comparison|source|example|synthesis|exercise|index|log
category: 分类
level: fundamental|beginner|intermediate|advanced
related: [[相关页面1]], [[相关页面2]]
prerequisites: [[前置知识]]
source: [[源材料页面]]        # 知识页必需
status: draft|needs-check|reviewed  # 知识页必需
---
```

页面之间通过 `[[双向链接]]` 连接，Obsidian 图谱视图可直观展示知识网络。

---

## 收录情况

### 源材料

| 教材 | 类型 | 来源 | 状态 |
|------|------|------|------|
| *Colloquial Mongolian* (Sanders & Bat-Ireedui, 1999) | 口语教材 | Routledge | 已提取·待补全 |
| **清格尔泰《蒙古语语法（西里尔）》** | 传统语法 | [mongol-surah.github.io](https://mongol-surah.github.io/cyrillic/cyrillic-grammar/)（巴·达赖转写） | 已提取格体系、动词形态、句法、构词法 |
| **Gaunt《现代蒙古语（西里尔）》** | 在线教材 | [mongol-surah.github.io](https://mongol-surah.github.io/cyrillic/gaunt-mongolian/) | 已提取疑问句、否定式、隐藏 g 名词、强调句 |
| **Peace Corps Pre-Service Training Book — Mongolian** | 培训教材 | Peace Corps (199p) | **进行中** — U1–U4 已提取 |
| Vacek & Lubsandorji《Mongolian Grammar Reference》 | 语法参考书 | 扫描版 PDF (425p) | 待 OCR |

完整清单 → [raw/MANIFEST.md](raw/MANIFEST.md)

### 已覆盖知识领域

| 领域 | 包含内容 |
|------|----------|
| **音系** | 字母表、元音分类（前后/中性）、辅音分类、元音和谐律 |
| **名词语法** | 8 个格、复数形式、领属（人称/反身）、属格规则、N-stem 名词、隐藏 g 名词 |
| **动词语法** | 现在时/将来时、过去时、习惯式、祈使式、否定式、进行体 |
| **句法与语气** | SOV 语序、名词谓语、疑问句、强调句、主语标记 нь、助词 ч |
| **主题会话** | 日常问候、自我介绍、家庭与人物、饮食、学校与工作、时间与数字、交通与旅行、购物 |
| **练习层** | 阶段1–6（覆盖上述所有主题）+ 元音和谐后缀选择专项练习 |
| **合成速查** | 初学者语法路线图、动词形态速查、格用法对比、否定与疑问速查、句型模板 |

### 质量指标

| 指标 | 状态 |
|------|------|
| 断裂链接 | **0** |
| 核心页面缺 `source` / `status` | **0** |
| 西里尔/拉丁混字 token | **0** |

---

## 使用方式

### 方式一：Obsidian（推荐）

1. 克隆本仓库到本地
2. 在 [Obsidian](https://obsidian.md/) 中选择「打开本地仓库」
3. 开启「设置 → 文件与链接」中的相对路径选项（确保 `[[双向链接]]` 正常工作）

#### Obsidian 插件配置

本知识库充分利用 Obsidian 生态。以下插件按重要性分级推荐：

**核心插件（必须安装）**

| 插件 | 在本知识库中的作用 | 安装 |
|------|--------------------|------|
| **Dataview** | 基于 YAML frontmatter 运行动态查询。**70+ 页面全部带有结构化 frontmatter**，缺失 Dataview 将无法跨页面过滤和统计 | 社区插件 → 搜索 `Dataview` → 安装启用 |

安装后，可在任意 wiki 页面中添加以下查询块：

```dataview
TABLE type, level, status FROM "wiki" SORT level ASC
```

```dataview
TABLE type, level FROM "wiki" WHERE status = "reviewed" SORT level ASC
```

```dataview
TABLE rows.level as "页面列表" FROM "wiki" GROUP BY level
```

**推荐插件（显著提升工作流）**

| 插件 | 在本知识库中的作用 | 安装 |
|------|--------------------|------|
| **Obsidian Git** | LLM 每次编辑后自动提交和推送变更，版本控制自动化，无需手动操作 | 社区插件 → 安装 → 设置自动提交间隔（建议 10 分钟） |
| **Marp** | 将 Markdown 导出为幻灯片。`wiki/syntheses/` 中的速查页面可一键转为演示文稿 | 社区插件 → 搜索 `Marp` → 安装 |

**可选插件（按需安装）**

| 插件 | 作用 |
|------|------|
| **Obsidian Web Clipper** | 浏览器扩展，将网页文章转为 Markdown 存入 `raw/`——对应 Ingest 流程 |
| **Spaced Repetition** | 间隔重复闪卡，从 wiki 知识点生成 Anki 风格复习卡片，适合语言学习 |
| **Tag Wrangler** | 辅助管理自定义标签（本库主要使用 `category` 而非标签） |

**图谱视图（内置功能）**

`Ctrl/Cmd + G` 打开图谱视图——枢纽节点（被大量引用的页面）、孤岛页面（缺少入链）、分类聚类一目了然。可开启 Filters → 仅显示 `wiki/` 以排除其他目录。

**安装建议**

1. **第一步**：安装 Dataview（必须，否则知识库不可查询）
2. **第二步**：安装 Obsidian Git（推荐，实现版本控制自动化）
3. **第三步**：按需安装 Marp + Obsidian Web Clipper + Spaced Repetition
4. **最后**：`Ctrl/Cmd + G` 打开图谱，浏览知识网络

### 方式二：任意 Markdown 阅读器

所有内容均为标准 Markdown。`[[WikiLink]]` 在纯文本中表现为方括号链接，可在 Obsidian 外配合其他支持 wikilink 的编辑器阅读。

---

## 维护工作流

本知识库的日常维护围绕三个核心操作展开：

| 操作 | 触发时机 | LLM 执行内容 |
|------|----------|-------------|
| **Ingest（收录）** | 将新教材放入 `raw/books/` 后 | 读取源材料 → 提取知识点 → 新建或合并页面 → 更新 index + log |
| **Query（查询→回写）** | 提出学习或分析性问题时 | 搜索 wiki 页面 → 综合答案 → **如有新洞察则写回 wiki 为新页面** |
| **Lint（健康检查）** | 操作后即时 + 定期深度检查 | 扫描断裂链接、混字、缺失元数据、跨页矛盾 → 修复 → 记录 log |

其中 **Query → 回写** 是让知识库持续复合增长的关键：回答不仅仅停留在对话历史中——有价值的对比分析、速查表、学习路线图会被永久性地写入 `wiki/comparisons/` 或 `wiki/syntheses/`。

详细规范 → [.project/docs/CLAUDE.md](.project/docs/CLAUDE.md)

---

## 下一步计划

### 近期（内容扩展）

- **Peace Corps Unit 5 (Clothes)** — 衣物词汇、偏好表达、频率副词
- **Peace Corps Unit 6 (Shopping)** — 购物对话、颜色、讨价还价、尺寸表达
- **阶段7练习** — 覆盖 Unit 5–6 内容的综合练习页

### 中期（深化与校对）

- Peace Corps Unit 7–9 — 健康、天气、安全主题
- Vacek 语法书 OCR — 若获得可提取文本版本，用作核心语法页的二次校对来源
- 早期页面的逐句来源标注补全

### 远期（发布与工具）

- 使用 Quartz 等工具将知识库发布为可公开浏览的静态网站
- 添加标签云、语法点索引、难度过滤等搜索导航增强

---

## 致谢与声明

- 本项目为**学习研究用途**，所有原始教材版权归各自作者及出版方所有。
- 知识库中的结构化内容（页面组织、例句拆解、练习设计）由维护者与 LLM 协作生成。
- 感谢 **清格尔泰** 先生、**John Gaunt**、**Peace Corps**、**Vacek & Lubsandorji** 的学术贡献。
- 感谢 **巴·达赖（海占）** 老师的转写工作，感谢 [mongol-surah.github.io](https://mongol-surah.github.io/) 志愿者团队（yabuhu@proton.me）将多部经典教材数字化并免费发布。

---

> **状态**：活跃维护中 · 当前阶段：Peace Corps Unit 1–4 已完成，下一步 Unit 5 (Clothes) + Unit 6 (Shopping)

> **入口索引**：进入知识库请从 [wiki/index.md](wiki/index.md) 开始
