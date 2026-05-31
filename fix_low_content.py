"""
批量修复 low_content 问题：
- rule 页面缺少常见错误 → 在末尾添加
- example 页面缺少核心句型/场景/总结 → 在末尾添加语法要点总结
"""
import os, re

fixes = {
    # rule 页面 — 添加常见错误
    'wiki/rules/动词变位.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 混淆时态后缀的元音和谐（如 -на/-нэ/-но/-нө）\n- 将态后缀与体后缀顺序颠倒\n- 祈使式中忘记根据人称变化后缀\n'
    },
    'wiki/rules/名词变格.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 混淆位格（-д）和给格（-д）的用法（两者后缀相同但语义不同）\n- 向格（-руу）忘记根据元音和谐变化\n- 共同格（-тай）与工具格（-аар）的用法混淆\n'
    },
    'wiki/rules/名词的概称.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 将概称与复数混淆使用\n- 在需要精确列举的语境中误用概称\n'
    },
    'wiki/rules/名词的领属.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 混淆人称领属与反身领属的用法\n- 忘记领属后缀也有元音和谐变化\n- 将第一人称复数 -маань 与 -м草ань 混淆\n'
    },
    'wiki/rules/向格.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 将向格（-руу）与位格/给格（-д）混淆\n- 忘记 -руу/-рүү 的元音和谐变化\n- 将向格用于"在……里面"（应为位格）\n'
    },
    'wiki/rules/感叹句.md': {
        'type': 'rule',
        'add': '\n## 常见错误\n\n- 在书面语中过度使用感叹词\n- 将呼语与主语混淆\n- 使用不当的感情词造成语气冒犯\n'
    },
    # example 页面 — 添加语法要点总结
    'wiki/examples/日常问候.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[名词谓语]] — "Сайн байна уу?" 中的谓语形式\n- [[否定式]] — биш 与 үгүй 的用法\n- [[元音和谐律]] — 问候语中的元音协调\n'
    },
    'wiki/examples/自我介绍.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[名词谓语]] — 名词直接作谓语\n- [[属格的形成]] — 来源地表达中的属格\n- [[共同格]] — "有/没有"的表达\n'
    },
    'wiki/examples/饮食.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[共同格]] — "想吃……"的表达\n- [[否定式]] — "不想/不吃"的否定形式\n- [[形容词]] — 食物描述中的形容词用法\n'
    },
    'wiki/examples/学校与工作.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[共同格]] — "在某地工作"\n- [[位格]] — "在学校/在图书馆"\n- [[否定式]] — "不会/不懂"的表达\n'
    },
    'wiki/examples/时间与数字.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[数词]] — 钟点、日期、年份的表达\n- [[时间词]] — "现在""昨天""明天"的用法\n- [[从比格]] — "从……点"到"……点"\n'
    },
    'wiki/examples/交通与旅行.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[工具格]] — 交通工具表达（乘……）\n- [[向格]] — 方向表达（去……）\n- [[从比格]] — 出发地表达（从……来）\n'
    },
    'wiki/examples/购物.md': {
        'type': 'example',
        'add': '\n## 语法要点总结\n\n- [[共同格]] — "有……钱"的表达\n- [[数词]] — 价格、数量的表达\n- [[离格]] — 比较价格（比……便宜/贵）\n'
    },
}

modified = 0
for filepath, cfg in fixes.items():
    full_path = os.path.join(os.getcwd(), filepath.replace('/', os.sep))
    if not os.path.exists(full_path):
        print(f"SKIP: {filepath} not found")
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 检查是否已经有常见错误或语法要点总结
    if '## 常见错误' in text or '## 语法要点总结' in text:
        print(f"SKIP: {filepath} already has section")
        continue
    
    # 移除末尾的 \r 和空行
    text = text.rstrip()
    text += cfg['add']
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(text)
    modified += 1
    print(f"FIXED: {filepath}")

print(f"\nModified {modified} files")
