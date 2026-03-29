#!/usr/bin/env python3
"""
Rebuild the articles database from markdown files.
Run after adding new articles to keep the DB in sync.
"""
import json, os, re
from datetime import datetime

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')
NEWS_DIR = os.path.join(PROJECT_DIR, 'src', 'content', 'news')
DB_PATH = os.path.join(PROJECT_DIR, 'data', 'articles-db.json')

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

articles = []
for f in sorted(os.listdir(NEWS_DIR)):
    if not f.endswith('.md'):
        continue
    with open(os.path.join(NEWS_DIR, f), 'r', encoding='utf-8') as fh:
        content = fh.read()
    parts = content.split('---')
    if len(parts) < 3:
        continue
    fm = parts[1]
    
    title = re.search(r'title:\s*["\x27](.*?)["\x27]', fm)
    desc = re.search(r'description:\s*["\x27](.*?)["\x27]', fm)
    pub = re.search(r'pubDate:\s*(\S+)', fm)
    cat = re.search(r'category:\s*["\x27]?(\S+?)["\x27]?\s*$', fm, re.MULTILINE)
    tags_match = re.search(r'tags:\s*\[(.*?)\]', fm)
    company = re.search(r'company:\s*["\x27](.*?)["\x27]', fm)
    domain = re.search(r'companyDomain:\s*["\x27](.*?)["\x27]', fm)
    sources = re.findall(r'url:\s*["\x27](.*?)["\x27]', fm)
    
    slug = f.replace('.md', '')
    tags = [t.strip().strip('"').strip("'") for t in tags_match.group(1).split(',')] if tags_match else []
    
    articles.append({
        'slug': slug,
        'title': title.group(1) if title else '',
        'description': desc.group(1) if desc else '',
        'pubDate': pub.group(1) if pub else '',
        'category': cat.group(1) if cat else '',
        'tags': [t for t in tags if t],
        'company': company.group(1) if company else '',
        'companyDomain': domain.group(1) if domain else '',
        'sourceCount': len(sources),
        'file': f
    })

db = {
    'generated': datetime.now().isoformat(),
    'count': len(articles),
    'categories': {},
    'articles': articles
}

# Count by category
for a in articles:
    cat = a['category']
    db['categories'][cat] = db['categories'].get(cat, 0) + 1

with open(DB_PATH, 'w', encoding='utf-8') as fh:
    json.dump(db, fh, indent=2, ensure_ascii=False)

print(f"Database rebuilt: {len(articles)} articles")
for cat, count in sorted(db['categories'].items()):
    print(f"  {cat}: {count}")
