"""
Detect and fix footnote digit pollution in Mongolian suffixes.
Issue: footnote markers (like 4) got merged into suffix text during PDF extraction.
Example: -сан4 should be -сан
"""
import os, re, sys

wiki_dir = 'wiki'
files = []
for root, dirs, filenames in os.walk(wiki_dir):
    for f in filenames:
        if f.endswith('.md'):
            files.append(os.path.join(root, f))

# Pattern: hyphen + Cyrillic letters + digits
pattern = re.compile(r'(-[\u0400-\u04FF]+)(\d+)')

dry_run_results = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = list(pattern.finditer(text))
    if not matches:
        continue
    
    lines = text.splitlines()
    line_offsets = []
    pos = 0
    for i, line in enumerate(lines):
        line_offsets.append((pos, pos + len(line), i + 1, line))
        pos += len(line) + 1
    
    for m in matches:
        start = m.start()
        suffix = m.group(1)
        digit = m.group(2)
        
        line_no = 1
        line_text = ""
        for lo, hi, ln, lt in line_offsets:
            if lo <= start < hi:
                line_no = ln
                line_text = lt
                break
        
        dry_run_results.append({
            'file': filepath.replace('\\', '/'),
            'line': line_no,
            'line_text': line_text.strip(),
            'match': m.group(0),
            'suffix': suffix,
            'digit': digit,
        })

# Build full report in UTF-8 file (avoids console encoding issues)
report_lines = []
report_lines.append("=" * 70)
report_lines.append(f"Footnote Digit Pollution Scan Report -- {len(dry_run_results)} issues found")
report_lines.append("=" * 70)

current_file = None
count_by_file = {}
for r in dry_run_results:
    f = r['file']
    count_by_file[f] = count_by_file.get(f, 0) + 1
    if f != current_file:
        current_file = f
        report_lines.append(f"\n[FILE] {f}")
    report_lines.append(f"  Line {r['line']:>3}: {r['match']:<12} -> {r['suffix']}")
    report_lines.append(f"      Context: {r['line_text'][:80]}")

report_lines.append(f"\n{'=' * 70}")
report_lines.append(f"Affected files: {len(count_by_file)}")
report_lines.append(f"Total issues: {len(dry_run_results)}")
report_lines.append("=" * 70)

report_text = '\n'.join(report_lines)

# Write to file
with open('footnote_pollution_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)
    f.write('\n')

# Print ASCII summary to console
print("=" * 60)
print("FOOTNOTE POLLUTION SCAN COMPLETE")
print("=" * 60)
print(f"Total issues found: {len(dry_run_results)}")
print(f"Affected files: {len(count_by_file)}")
for fname, cnt in sorted(count_by_file.items()):
    print(f"  {cnt:>2} issues in {fname}")
print("=" * 60)
print("Full report saved to: footnote_pollution_report.txt")
print("=" * 60)
