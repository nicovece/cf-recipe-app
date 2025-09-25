#!/bin/bash

# Development Tailwind CSS + Django Static Files Watch Script
# This script runs Tailwind in watch mode and automatically syncs with Django

set -e  # Exit on any error

echo "🚀 Starting Tailwind CSS development mode with Django sync..."

# Function to sync with Django
sync_django() {
    echo "🔄 Syncing with Django staticfiles..."
    source recipeapp/bin/activate
    python src/manage.py collectstatic --noinput
    echo "✅ Django staticfiles synced"
}

# Initial sync
echo "📦 Initial build and sync..."
pnpm run build
sync_django

echo "👀 Starting Tailwind watch mode..."
echo "💡 The CSS will be automatically synced with Django when changes are detected."
echo "🛑 Press Ctrl+C to stop"

# Start Tailwind in watch mode
tailwindcss -i ./src/static/css/input.css -o ./src/static/css/output.css --watch &
TAILWIND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Tailwind watch mode..."
    kill $TAILWIND_PID 2>/dev/null || true
    echo "✅ Development mode stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Simple polling approach for cross-platform compatibility
echo "🔄 Starting file watcher (polling every 3 seconds)..."
LAST_MODIFIED=0

while true; do
    if [ -f ./src/static/css/output.css ]; then
        CURRENT_MODIFIED=$(stat -f %m ./src/static/css/output.css 2>/dev/null || stat -c %Y ./src/static/css/output.css 2>/dev/null || echo "0")
        
        if [ "$CURRENT_MODIFIED" != "$LAST_MODIFIED" ] && [ "$CURRENT_MODIFIED" != "0" ]; then
            echo "📝 CSS file changed, syncing with Django..."
            sync_django
            LAST_MODIFIED=$CURRENT_MODIFIED
        fi
    fi
    
    sleep 3
done
