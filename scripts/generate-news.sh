#!/bin/bash
# Daily AI Insurance News Generator
# Searches for current news, generates articles, commits and pushes

set -e

PROJECT_DIR="/home/simsalabim/.openclaw/workspace/ai-versicherung-news"
TODAY=$(date +%Y-%m-%d)
NEWS_DIR="$PROJECT_DIR/src/content/news"

echo "=== AI Insurance News Generator ==="
echo "Date: $TODAY"
echo ""

cd "$PROJECT_DIR"

# Pull latest changes
git pull --rebase origin main 2>/dev/null || true

echo "News generation ready. Articles will be created by Salomon."
echo "Run: openclaw cron run ai-news-generator"
