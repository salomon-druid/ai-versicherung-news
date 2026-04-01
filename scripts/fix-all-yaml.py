#!/usr/bin/env python3
"""Fix typographic quotes in YAML frontmatter of Astro content files."""

import os
import re
import glob

def fix_typographic_quotes(content):
    """Replace typographic quotes with regular quotes in YAML frontmatter."""
    # Split content into frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Replace typographic quotes in frontmatter only
            frontmatter = frontmatter.replace('„', '"').replace('"', '"')
            
            return f'---{frontmatter}---{body}'
    
    return content

def main():
    content_dir = '/home/simsalabim/.openclaw/workspace/ai-versicherung-news/src/content'
    
    # Find all markdown files
    md_files = glob.glob(f'{content_dir}/**/*.md', recursive=True)
    
    fixed_count = 0
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            fixed_content = fix_typographic_quotes(original_content)
            
            if fixed_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f'Fixed: {file_path}')
                fixed_count += 1
        except Exception as e:
            print(f'Error processing {file_path}: {e}')
    
    print(f'\nTotal files fixed: {fixed_count}')

if __name__ == '__main__':
    main()