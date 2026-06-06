# raw/ 原始源材料清单

> **本目录的使命**: 存储所有原始学习材料（不可变层）。
> **本目录的使命**: 存储所有原始学习材料（不可变层）。
 > **只读规则**: LLM 可读取本目录中的任何文件，但**绝不修改**。
 > **版本控制**: 大型二进制文件被 `.gitignore` 排除，但本清单文件纳入版本控制，确保 LLM 能发现所有可用源材料。
 
 ---
 
 ## 源材料总览
 
 | # | 文件名 | 格式 | 语言 | 级别 | 类型 | 对应源摘要页 | 提取状态 |
 |---|--------|------|------|------|------|-------------|----------|
 | 1 | `Colloquial Mongolian.pdf` | PDF | 英文 | Primary | 口语教材 | [[Colloquial Mongolian]] | 已提取·待补全 |
 | 2 | `Peace-Corps-Pre-Service-Training-Book-Mongilian.pdf` | PDF | 英文 | Primary | 综合教材 | [[Peace Corps Pre-Service Training Book — Mongolian]] | 进行中 (U1-U4 完成) |
 | 3 | `vacek_lubsandorji.pdf` | PDF | 英文 | Primary | 语法参考 | [[Vacek & Lubsandorji — Mongolian Grammar Reference]] | 待 OCR |
 
 ---
 
 ## 文件详情
 
 ### 1. Colloquial Mongolian.pdf
 
 | 属性 | 值 |
 |------|-----|
 | **文件路径** | `raw/books/Colloquial Mongolian.pdf` |
 | **文件格式** | PDF (扫描版) |
 | **作者** | Alan J.K. Sanders, Jantsangiyn Bat-Ireedui |
 | **出版** | Routledge, 1999 |
 | **语言** | 英文（蒙古语例句） |
 | **级别** | Primary |
 | **类型** | 口语教材 |
 | **对应源摘要页** | [[Colloquial Mongolian]] |
 | **OCR 状态** | 已完成 |
 | **提取状态** | 已提取，待补全 |
 | **内容概要** | 面向初学者的综合口语课程，含对话、语法说明、词汇和文化注释 |
 | **章节数** | 16 章 + 附录 |
 
 ### 2. Peace-Corps-Pre-Service-Training-Book-Mongilian.pdf
 
 | 属性 | 值 |
 |------|-----|
 | **文件路径** | `raw/books/Peace-Corps-Pre-Service-Training-Book-Mongilian.pdf` |
 | **文件格式** | PDF (文本可提取) |
 | **作者** | Peace Corps |
 | **出版** | 约 2000s |
 | **语言** | 英文（蒙古语例句） |
 | **级别** | Primary |
 | **类型** | 综合教材 |
 | **对应源摘要页** | [[Peace Corps Pre-Service Training Book — Mongolian]] |
 | **提取状态** | 进行中：U1-U4 已提取，U5-U9 待提取 |
 | **内容概要** | 和平队岗前培训教材，按单元组织，涵盖日常会话场景与基础语法 |
 | **章节数** | 9 单元 |
 
 ### 3. vacek_lubsandorji.pdf
 
 | 属性 | 值 |
 |------|-----|
 | **文件路径** | `raw/books/vacek_lubsandorji.pdf` |
 | **文件格式** | PDF (扫描版) |
 | **作者** | Vacek & Lubsandorji |
 | **出版** | 约 2000s |
 | **语言** | 英文（蒙古语例句） |
 | **级别** | Primary |
 | **类型** | 语法参考 |
 | **对应源摘要页** | [[Vacek & Lubsandorji — Mongolian Grammar Reference]] |
 | **OCR 状态** | 待 OCR |
 | **提取状态** | 尚未提取 |
 | **内容概要** | 系统的蒙古语语法参考，涵盖词法、句法 |
 
 ---
 
 ## 收录流程
 
 当添加新的原始源材料时：
 
 1. 将文件放入 `raw/books/`
 2. 更新本清单，添加新条目
 3. 在 `wiki/sources/` 中创建对应的源摘要页
 4. 按 CLAUDE.md §5 的源材料处理流程进行收录
 
 ---
 
 ## 文件维护规范
 
 - **只读**: 一旦入库，原始文件**绝不修改**
 - **命名**: 保留原始文件名，不缩写
 - **跨源摘要页同步**: 源材料的提取状态以 `wiki/sources/` 为准，本清单仅做快速概览
