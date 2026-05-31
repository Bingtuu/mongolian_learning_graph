"""
Apply fix: remove footnote digits merged into Mongolian suffixes.
Pattern: hyphen + Cyrillic letters + digit(s) -> keep only hyphen + Cyrillic letters
"""
import os, re

wiki_dir = 'wiki'
files = []
for root, dirs, filenames in os.walk(wiki_dir):
    for f in filenames:
        if f.endswith('.md'):
            files.append(os.path.join(root, f))

pattern = re.compile(r'(-[\u0400-\u04FF]+)(\d+)')

fixed_files = []
total_replacements = 0

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original = text
    # Replace: keep only the suffix (group 1), drop the digit (group 2)
    text, count = pattern.subn(r'\1', text)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        fixed_files.append((filepath.replace('\\', '/'), count))
        total_replacements += count

print("=" * 60)
print("FOOTNOTE POLLUTION FIX APPLIED")
print("=" * 60)
print(f"Files modified: {len(fixed_files)}")
print(f"Total replacements: {total_replacements}")
print()
for fname, cnt in fixed_files:
    print(f"  {cnt:>2} replacements in {fname}")
print("=" * 60)
