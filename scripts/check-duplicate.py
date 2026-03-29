#!/usr/bin/env python3
"""
Check if an article already exists based on title similarity.
Usage: python3 scripts/check-duplicate.py "Article Title"
Exit code 0 = duplicate found, 1 = no duplicate
"""
import json
import sys
import os

def normalize(text):
    """Normalize text for comparison."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9äöüß\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def similarity(a, b):
    """Simple word overlap similarity."""
    words_a = set(normalize(a).split())
    words_b = set(normalize(b).split())
    if not words_a or not words_b:
        return 0
    intersection = words_a & words_b
    return len(intersection) / min(len(words_a), len(words_b))

if len(sys.argv) < 2:
    print("Usage: python3 check-duplicate.py 'Article Title'")
    sys.exit(1)

new_title = sys.argv[1]
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles-db.json')

if not os.path.exists(db_path):
    print("No database found - assuming no duplicate")
    sys.exit(1)

with open(db_path) as f:
    db = json.load(f)

threshold = 0.7
for article in db['articles']:
    score = similarity(new_title, article['title'])
    if score >= threshold:
        print(f"DUPLICATE FOUND (similarity: {score:.0%})")
        print(f"  Existing: {article['title']}")
        print(f"  New:      {new_title}")
        print(f"  Slug:     {article['slug']}")
        print(f"  Date:     {article['pubDate']}")
        sys.exit(0)

print(f"OK: No duplicate found for '{new_title}'")
sys.exit(1)
