#!/bin/bash
# Fetch images from Unsplash for AI insurance news articles
# Usage: ./scripts/fetch-unsplash-images.sh

set -e

source "$(dirname "$0")/../.env"

ACCESS_KEY="$UNSPLASH_ACCESS_KEY"
IMAGES_DIR="$(dirname "$0")/../public/images"
mkdir -p "$IMAGES_DIR"

# Category to search query mapping
declare -A QUERIES=(
  ["ki-anwendungen"]="artificial-intelligence,technology"
  ["regulierung"]="law,regulation,documents"
  ["makler"]="office,business,meeting"
  ["maerkte"]="stock-market,finance,analytics"
  ["innovation"]="startup,innovation,lightbulb"
  ["risikomanagement"]="security,protection,shield"
  ["default"]="insurance,digital,technology"
)

echo "=== Fetching Unsplash Images ==="

for category in "${!QUERIES[@]}"; do
  query="${QUERIES[$category]}"
  echo "Fetching: $category ($query)"
  
  response=$(curl -s "https://api.unsplash.com/photos/random?query=${query}&orientation=landscape&w=1200&h=630&client_id=${ACCESS_KEY}")
  
  image_url=$(echo "$response" | jq -r '.urls.custom // .urls.regular // empty')
  photographer=$(echo "$response" | jq -r '.user.name // "Unsplash"')
  photographer_url=$(echo "$response" | jq -r '.user.links.html // "https://unsplash.com"')
  photo_id=$(echo "$response" | jq -r '.id // empty')
  
  if [ -n "$image_url" ] && [ "$image_url" != "null" ]; then
    filename="${category}.jpg"
    curl -sL "$image_url" -o "$IMAGES_DIR/$filename"
    echo "  ✓ Saved: $filename (by $photographer)"
    
    # Save attribution
    echo "{\"id\":\"$photo_id\",\"photographer\":\"$photographer\",\"url\":\"$photographer_url\"}" > "$IMAGES_DIR/${category}.json"
  else
    echo "  ✗ Failed to fetch image"
  fi
  
  sleep 1  # Rate limit
done

echo ""
echo "Done! Images saved to $IMAGES_DIR"
