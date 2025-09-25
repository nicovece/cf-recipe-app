#!/bin/bash

# Tailwind CSS + Django Static Files Build Script
# This script builds Tailwind CSS and syncs it with Django's staticfiles

set -e  # Exit on any error

echo "🎨 Building Tailwind CSS..."

# Build Tailwind CSS (production version)
echo "📦 Running Tailwind build..."
pnpm run build-prod

# Activate virtual environment and run collectstatic
echo "🔄 Syncing with Django staticfiles..."
source recipeapp/bin/activate
python src/manage.py collectstatic --noinput

echo "✅ Build complete! Tailwind CSS has been built and synced with Django."
echo "📁 Files updated:"
echo "   - src/static/css/output.css"
echo "   - src/staticfiles/css/output.css"
