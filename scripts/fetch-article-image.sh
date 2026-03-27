#!/bin/bash
# Fetch unique images from Unsplash for insurance news articles
# Usage: ./scripts/fetch-article-image.sh <slug> <category>

set -e

source "$(dirname "$0")/../.env"

ACCESS_KEY="$UNSPLASH_ACCESS_KEY"
SLUG="$1"
CATEGORY="$2"
IMAGES_DIR="$(dirname "$0")/../public/images/articles"
mkdir -p "$IMAGES_DIR"

# Category to search query mapping
declare -A QUERIES=(
  ["ki-digitalisierung"]="artificial-intelligence,neural-network,technology"
  ["versicherer"]="insurance-company,corporate,skyscraper,business-tower"
  ["versicherungsprodukte"]="contract,document,agreement,insurance-policy"
  ["versicherungsumfeld"]="parliament,law,regulation,eu-flag"
  ["makler"]="business-meeting,handshake,office,consulting"
  ["risiken-schaeden"]="storm,flood,cyberattack,disaster,fire"
)

query="${QUERIES[$CATEGORY]:-insurance,digital,technology}"

echo "Fetching image for: $SLUG ($query)"

response=$(curl -s "https://api.unsplash.com/photos/random?query=${query}&orientation=landscape&w=1200&h=630&client_id=${ACCESS_KEY}")

image_url=$(echo "$response" | jq -r '.urls.custom // .urls.regular // empty')
photographer=$(echo "$response" | jq -r '.user.name // "Unsplash"')
photographer_url=$(echo "$response" | jq -r '.user.links.html // "https://unsplash.com"')
photo_id=$(echo "$response" | jq -r '.id // empty')

if [ -n "$image_url" ] && [ "$image_url" != "null" ]; then
  curl -sL "$image_url" -o "$IMAGES_DIR/${SLUG}.jpg"
  echo "{\"id\":\"$photo_id\",\"photographer\":\"$photographer\",\"url\":\"$photographer_url\",\"category\":\"$CATEGORY\",\"fetched\":\"$(date -Iseconds)\"}" > "$IMAGES_DIR/${SLUG}.json"
  echo "✓ Saved: ${SLUG}.jpg (by $photographer)"
else
  echo "✗ Failed, using category fallback"
  cp "$(dirname "$0")/../public/images/${CATEGORY}.jpg" "$IMAGES_DIR/${SLUG}.jpg" 2>/dev/null || cp "$(dirname "$0")/../public/images/default.jpg" "$IMAGES_DIR/${SLUG}.jpg"
fi
