"""
批量为缺少来源标注的例句添加来源。
策略：
- 读取每个文件的 frontmatter，获取 source 和 title
- 找到所有引用块（连续以 > 开头的行）
- 排除：表格、提示块、单字示例、已有来源的
- 在有效例句引用块末尾添加来源行
"""
import os, re

wiki_dir = 'wiki'
files = []
for root, dirs, filenames in os.walk(wiki_dir):
    for f in filenames:
        if f.endswith('.md'):
            files.append(os.path.join(root, f))

def extract_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[3:end].strip(), text[end+3:]
    return None, text

def parse_frontmatter_simple(fm_text):
    result = {}
    current_key = None
    current_val = None
    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m:
            if current_key is not None:
                result[current_key] = current_val.strip() if current_val else ''
            current_key = m.group(1)
            current_val = m.group(2)
        else:
            if current_key is not None:
                current_val = (current_val or '') + '\n' + line
    if current_key is not None:
        result[current_key] = current_val.strip() if current_val else ''
    return result

def extract_first_source(source_val):
    """从 source 字段提取第一个来源"""
    if not source_val:
        return None
    # 匹配 [[页面名|别名]] 或 [[页面名]]
    m = re.search(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', source_val)
    if m:
        return m.group(1)
    # 如果不是 wikilink，返回 None
    return None

fixed_count = 0
files_modified = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    rel = filepath.replace('\\', '/')
    basename = os.path.basename(rel)[:-3]
    
    fm_text, body = extract_frontmatter(text)
    if fm_text is None:
        continue
    
    fm = parse_frontmatter_simple(fm_text)
    page_type = fm.get('type', '').strip()
    source_val = fm.get('source', '')
    first_source = extract_first_source(source_val)
    
    # 只有 concept/entity/rule/example/comparison 页面需要处理
    if page_type not in ('concept', 'entity', 'rule', 'example', 'comparison', 'synthesis'):
        continue
    
    # 如果没有可用来源，跳过
    if not first_source:
        continue
    
    lines = body.splitlines()
    new_lines = []
    i = 0
    file_fixed = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是引用块的开始
        if line.startswith('> '):
            # 收集整个引用块
            quote_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith('> '):
                quote_lines.append(lines[j])
                j += 1
            
            quote_text = '\n'.join(quote_lines)
            
            # 检查是否是有效例句
            # 1. 包含西里尔字母
            has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', quote_text))
            if not has_cyrillic:
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 2. 排除表格行
            if re.search(r'>\s*\|', quote_text):
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 3. 排除提示/警告块（以 > ** 开头）
            if quote_lines[0].startswith('> **'):
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 4. 排除列表项（> - 或 > *）
            if re.match(r'>\s*[-*]\s', quote_lines[0]):
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 5. 排除代码块或标记（> `）
            if quote_lines[0].startswith('> `'):
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 6. 检查是否已有来源标注
            has_source = any('—' in ql and ('来源' in ql or '语法点' in ql or '参见' in ql) for ql in quote_lines)
            if has_source:
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 7. 检查是否已有 wikilink（可能是内嵌链接，不是来源）
            # 但如果最后一行包含 [[，可能是已经处理过的
            last_line = quote_lines[-1].strip()
            if '[[' in last_line and '—' in last_line:
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 8. 排除纯中文引用块（非蒙古语例句）
            cyrillic_words = re.findall(r'[\u0400-\u04FF]+', quote_text)
            if len(cyrillic_words) < 2:
                new_lines.extend(quote_lines)
                i = j
                continue
            
            # 这是一个有效例句，添加来源
            new_lines.extend(quote_lines)
            # 添加来源行
            source_line = f"> — 来源: [[{first_source}]] | 语法点: [[{basename}]]"
            new_lines.append(source_line)
            file_fixed += 1
            i = j
            continue
        else:
            new_lines.append(line)
            i += 1
    
    if file_fixed > 0:
        new_body = '\n'.join(new_lines)
        new_text = '---\n' + fm_text + '\n---' + new_body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        files_modified.append((rel, file_fixed))
        fixed_count += file_fixed

print("=" * 60)
print("EXAMPLE SOURCE FIX COMPLETE")
print("=" * 60)
print(f"Files modified: {len(files_modified)}")
print(f"Total examples fixed: {fixed_count}")
for fname, cnt in files_modified:
    print(f"  {cnt:>3} in {fname}")
print("=" * 60)
