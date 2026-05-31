"""
全面 Review 知识库，按 CLAUDE.md 标准检查所有页面。
使用自定义 frontmatter 解析器（避免 YAML 的 wikilink 解析问题）。
"""
import os, re, sys

wiki_dir = 'wiki'
files = []
for root, dirs, filenames in os.walk(wiki_dir):
    for f in filenames:
        if f.endswith('.md'):
            files.append(os.path.join(root, f))

# 收集现有文件（用于断链检查）
existing = set()
existing_lower = {}
for f in files:
    rel = f.replace('\\', '/')
    basename = os.path.basename(rel)
    name_no_ext = basename[:-3]
    existing.add(name_no_ext)
    existing.add(basename)
    existing_lower[name_no_ext.lower()] = name_no_ext
    existing_lower[basename.lower()] = basename

def extract_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[3:end].strip()
    return None

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

def parse_wikilink_list(val):
    if not val:
        return []
    links = []
    for m in re.finditer(r'\[\[([^\]]+)\]\]', val):
        links.append(m.group(1))
    return links

issues = {
    'broken_links': [],
    'missing_frontmatter': [],
    'missing_required_field': [],
    'missing_source': [],
    'missing_status': [],
    'mixed_tokens': [],
    'example_no_source': [],
    'low_content': [],
    'empty_page': [],
    'related_self': [],
}

NEEDS_SOURCE_STATUS = {'concept', 'entity', 'rule', 'comparison', 'example', 'synthesis', 'exercise'}

latin_in_cyrillic = set('aAeEoOpPcCxXyY')

def count_cyrillic_words(text):
    return len(re.findall(r'[\u0400-\u04FF]+', text))

def check_wikilink_target(target):
    target = target.strip().split('#')[0].split('|')[0]
    if target in existing:
        return True
    if target.lower() in existing_lower:
        return True
    for ex in existing:
        if ex.endswith('/' + target) or ex == target:
            return True
    return False

def body_after_fm(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end+3:]
    return text

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    rel = filepath.replace('\\', '/')
    basename = os.path.basename(rel)[:-3]
    
    if len(text.strip()) < 100:
        issues['empty_page'].append(rel)
        continue
    
    fm_text = extract_frontmatter(text)
    if fm_text is None:
        issues['missing_frontmatter'].append(rel)
        continue
    
    fm = parse_frontmatter_simple(fm_text)
    page_type = fm.get('type', '').strip()
    
    # 必需字段
    required_fields = ['title', 'type', 'category', 'level']
    for field in required_fields:
        if field not in fm or not fm.get(field):
            issues['missing_required_field'].append((rel, page_type or 'unknown', field))
    
    if page_type in NEEDS_SOURCE_STATUS:
        src = fm.get('source', '').strip()
        if not src or src == '[]':
            issues['missing_source'].append((rel, page_type))
        st = fm.get('status', '').strip()
        if not st:
            issues['missing_status'].append((rel, page_type))
    
    body = body_after_fm(text)
    
    # 断裂链接
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', body)
    for link in links:
        target = link.strip().split('#')[0]
        if not check_wikilink_target(target):
            issues['broken_links'].append((rel, target))
    
    # related 自引用
    related_raw = fm.get('related', '')
    related_links = parse_wikilink_list(related_raw)
    for r in related_links:
        r_clean = r.split('|')[0].split('#')[0]
        if r_clean == basename:
            issues['related_self'].append((rel, r_clean))
    
    # 混字污染
    fm_end_pos = text.find('---', 3) + 3 if text.startswith('---') else 0
    text_after_fm = text[fm_end_pos:]
    for line_no, line in enumerate(text_after_fm.splitlines(), 1):
        for word in re.findall(r"[\u0400-\u04FFa-zA-Z]+", line):
            has_cyrillic = any(0x0400 <= ord(ch) <= 0x04FF for ch in word)
            if has_cyrillic:
                bad_chars = [ch for ch in word if ch in latin_in_cyrillic]
                if bad_chars:
                    issues['mixed_tokens'].append((rel, line_no, word, ''.join(bad_chars)))
    
    # 例句来源检查（仅 example 和 rule 页面）
    # concept/entity 页面中的内嵌示例不强制要求独立来源标注
    if page_type in ('example', 'rule'):
        quotes = re.findall(r'(?:^|\n)> .+(?:\n> .+)*', text_after_fm)
        for qb in quotes:
            qb_lines = qb.strip().splitlines()
            if not qb_lines:
                continue
            # 排除提示/说明块（> **...）
            if qb_lines[0].startswith('> **'):
                continue
            # 排除表格行（> |）
            if re.match(r'>\s*\|', qb_lines[0]):
                continue
            # 排除纯说明文字（> 说明： / > 来源： / > 注意：）
            first_content = qb_lines[0].lstrip('> ').strip()
            if first_content.startswith('说明：') or first_content.startswith('来源：') or first_content.startswith('注意：'):
                continue
            has_cyrillic = any(re.search(r'[\u0400-\u04FF]', l) for l in qb_lines)
            if not has_cyrillic:
                continue
            any_source = any('—' in l and ('来源' in l or '语法点' in l or '[[' in l) for l in qb_lines)
            if not any_source:
                first_line = qb_lines[0].strip()
                safe_line = first_line[:60].encode('ascii', 'replace').decode('ascii')
                issues['example_no_source'].append((rel, safe_line))
    
    # 最低内容检查
    if page_type == 'rule':
        has_table = '|' in body and '---' in body
        has_example = '>' in body and re.search(r'[\u0400-\u04FF]', body)
        has_common_errors = '常见错误' in body or '常见误区' in body
        if not (has_table and has_example and has_common_errors):
            missing_parts = []
            if not has_table: missing_parts.append('table')
            if not has_example: missing_parts.append('example')
            if not has_common_errors: missing_parts.append('common_errors')
            issues['low_content'].append((rel, page_type, ','.join(missing_parts)))
    
    elif page_type == 'example':
        has_core = '核心' in body or '句型' in body or '替换练习' in body or '使用场景' in body
        heading_count = len(re.findall(r'\n## ', body))
        has_scene = '场景' in body or '###' in body or heading_count >= 3
        has_summary = '总结' in body or '要点' in body or '语法' in body or '常见错误' in body
        if not (has_core and has_scene and has_summary):
            missing_parts = []
            if not has_core: missing_parts.append('core')
            if not has_scene: missing_parts.append('scene')
            if not has_summary: missing_parts.append('summary')
            issues['low_content'].append((rel, page_type, ','.join(missing_parts)))
    
    elif page_type == 'concept':
        cyrillic_count = count_cyrillic_words(body)
        has_heading2 = bool(re.search(r'\n## ', body))
        if cyrillic_count < 3 or not has_heading2:
            issues['low_content'].append((rel, page_type, f"cyr={cyrillic_count},h2={has_heading2}"))
    
    elif page_type == 'entity':
        has_table = '|' in body
        cyrillic_count = count_cyrillic_words(body)
        if not has_table and cyrillic_count < 5:
            issues['low_content'].append((rel, page_type, "no_table_few_examples"))
    
    elif page_type == 'comparison':
        has_table = '|' in body and '---' in body
        has_example = '>' in body and re.search(r'[\u0400-\u04FF]', body)
        has_errors = '常见错误' in body or '注意' in body or '辨析' in body
        if not (has_table and has_example and has_errors):
            missing_parts = []
            if not has_table: missing_parts.append('table')
            if not has_example: missing_parts.append('example')
            if not has_errors: missing_parts.append('errors')
            issues['low_content'].append((rel, page_type, ','.join(missing_parts)))

# 构建报告文本
report_lines = []
report_lines.append("=" * 70)
report_lines.append("KNOWLEDGE BASE REVIEW REPORT")
report_lines.append("=" * 70)

total_issues = sum(len(v) for v in issues.values())
report_lines.append(f"\nTotal issues found: {total_issues}\n")

summary = {}
for name, items in issues.items():
    summary[name] = len(items)
    if not items:
        continue
    report_lines.append(f"\n--- {name.replace('_', ' ').upper()} ({len(items)}) ---")
    seen = set()
    for item in items:
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        if isinstance(item, tuple):
            report_lines.append(f"  {' | '.join(str(x) for x in item)}")
        else:
            report_lines.append(f"  {item}")

report_lines.append(f"\n{'=' * 70}")
report_text = '\n'.join(report_lines)

# 写入文件
with open('review_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

# 打印 ASCII 摘要
print("=" * 60)
print("KNOWLEDGE BASE REVIEW COMPLETE")
print("=" * 60)
print(f"Total issues: {total_issues}")
for name, count in sorted(summary.items()):
    print(f"  {name:30s}: {count:3d}")
print("=" * 60)
print("Full report: review_report.txt")
