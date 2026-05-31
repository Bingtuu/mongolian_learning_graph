import os, re

wiki_dir = 'wiki'
files = []
for root, dirs, filenames in os.walk(wiki_dir):
    for f in filenames:
        if f.endswith('.md'):
            files.append(os.path.join(root, f))

existing = set()
for f in files:
    rel = f.replace('\\', '/')
    existing.add(rel)
    existing.add(rel[:-3])
    existing.add(os.path.basename(rel)[:-3])
    existing.add(os.path.basename(rel))

broken = []
missing_meta = []
mixed_tokens = []

latin_in_cyrillic = set('aAeEoOpPcCxXyY')

def extract_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[3:end].strip()
    return ''

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    rel = f.replace('\\', '/')
    
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text)
    for link in links:
        target = link.strip().split('#')[0]
        candidates = [
            target + '.md',
            'wiki/' + target + '.md',
            target,
            'wiki/' + target,
        ]
        found = any(c in existing for c in candidates)
        if not found:
            broken.append((rel, target))
    
    fm = extract_frontmatter(text)
    if fm:
        m_type = re.search(r'^type:\s*(\S+)', fm, re.M)
        if m_type:
            t = m_type.group(1)
            if t in ('concept', 'entity', 'rule', 'comparison', 'synthesis', 'example', 'exercise'):
                has_source = 'source:' in fm
                has_status = 'status:' in fm
                if not has_source or not has_status:
                    missing_meta.append((rel, t, has_source, has_status))
    
    for line_no, line in enumerate(text.splitlines(), 1):
        for word in re.findall(r"[\u0400-\u04FFa-zA-Z]+", line):
            has_cyrillic = any(0x0400 <= ord(ch) <= 0x04FF for ch in word)
            if has_cyrillic:
                bad_chars = [ch for ch in word if ch in latin_in_cyrillic]
                if bad_chars:
                    mixed_tokens.append((rel, line_no, word, ''.join(bad_chars)))

out_lines = []
out_lines.append('=== Health Check Report ===')
out_lines.append('')
out_lines.append('--- Broken Links ---')
if broken:
    seen = set()
    for rel, target in broken:
        key = (rel, target)
        if key not in seen:
            seen.add(key)
            out_lines.append(f'  {rel} -> [[{target}]]')
else:
    out_lines.append('  No broken links')
out_lines.append('')

out_lines.append('--- Missing source/status ---')
if missing_meta:
    for rel, t, has_s, has_st in missing_meta:
        missing = []
        if not has_s: missing.append('source')
        if not has_st: missing.append('status')
        out_lines.append(f'  {rel} (type={t}) missing: {", ".join(missing)}')
else:
    out_lines.append('  None missing')
out_lines.append('')

out_lines.append('--- Mixed Cyrillic/Latin tokens ---')
if mixed_tokens:
    seen = set()
    for rel, line_no, word, bad in mixed_tokens:
        key = (rel, line_no, word)
        if key not in seen:
            seen.add(key)
            out_lines.append(f'  {rel}:{line_no} word="{word}" latin chars: {bad}')
else:
    out_lines.append('  No mixed tokens')

result = '\n'.join(out_lines)
print(result)
with open('lint_result2.txt', 'w', encoding='utf-8') as f:
    f.write(result)
