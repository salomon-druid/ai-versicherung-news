#!/usr/bin/env python3
import sys

for filepath in sys.argv[1:]:
    with open(filepath, 'r') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) >= 3:
        frontmatter = parts[1]
        # Replace curly/typographic quotes with regular quotes
        frontmatter = frontmatter.replace('\u201e', '"')  # „
        frontmatter = frontmatter.replace('\u201c', '"')  # "
        frontmatter = frontmatter.replace('\u201d', '"')  # "
        # Fix double closing quotes: "" -> "
        import re
        frontmatter = re.sub(r'""+', '"', frontmatter)
        parts[1] = frontmatter
        with open(filepath, 'w') as f:
            f.write('---'.join(parts))
        print(f'Fixed: {filepath}')
