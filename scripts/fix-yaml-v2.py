#!/usr/bin/env python3
"""Fix YAML frontmatter by removing problematic characters."""
import re
import sys

def fix_yaml_value(val):
    """Fix a YAML value string by escaping inner quotes."""
    val = val.strip()
    # If it's a quoted string, check for inner quotes
    if val.startswith('"') and val.endswith('"'):
        inner = val[1:-1]
        # Replace any remaining double quotes inside with single quotes
        inner = inner.replace('"', "'")
        val = f'"{inner}"'
    return val

def fix_yaml_line(line):
    """Fix a single YAML line with potential quote issues."""
    # Match key: "value" or key: value
    m = re.match(r'^(\s*[\w-]+:\s*)(.*)', line)
    if m:
        prefix = m.group(1)
        value = m.group(2).strip()
        # Check if value has problematic inner quotes
        if value.count('"') > 2:
            # Too many quotes - fix by using single quotes for the whole value
            cleaned = value.replace('"', "'")
            # Wrap in double quotes
            if not cleaned.startswith('"'):
                cleaned = f'"{cleaned}"'
            return prefix + cleaned + '\n'
    return line

def fix_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    fm_lines = parts[1].split('\n')
    fixed_lines = []
    for line in fm_lines:
        # Replace typographic quotes
        line = line.replace('\u201e', "'")  # „
        line = line.replace('\u201c', "'")  # "
        line = line.replace('\u201d', "'")  # "
        
        # Fix lines with too many double quotes
        if line.count('"') > 2 and ':' in line:
            # Split on first colon
            key, _, val = line.partition(':')
            val = val.strip()
            if val.startswith('"'):
                # Count quotes
                quote_count = val.count('"')
                if quote_count > 2:
                    # Replace all inner quotes with single quotes
                    # Keep first and last quote
                    inner = val[1:-1] if val.endswith('"') else val[1:]
                    inner = inner.replace('"', "'")
                    val = f'"{inner}"'
                    line = f'{key}: {val}'
        
        fixed_lines.append(line)
    
    parts[1] = '\n'.join(fixed_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---'.join(parts))
    return True

for filepath in sys.argv[1:]:
    if fix_frontmatter(filepath):
        print(f'Fixed: {filepath}')
