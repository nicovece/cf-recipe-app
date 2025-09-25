#!/bin/bash

# Simple Tailwind + Django Auto-Sync Script
# Watches for Tailwind rebuilds and automatically runs collectstatic

set -e

echo "🚀 Starting Tailwind CSS + Django auto-sync..."

# Get script directory and ensure we're in project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated. Looking for recipeapp/bin/activate..."
    if [[ -f "recipeapp/bin/activate" ]]; then
        source recipeapp/bin/activate
        echo "✅ Activated virtual environment"
    else
        echo "❌ Virtual environment not found. Please activate it manually first."
        exit 1
    fi
fi

# Initial build and sync
echo "📦 Initial build..."
pnpm run build
echo "🔄 Initial Django sync..."
cd src && python manage.py collectstatic --noinput
cd ..

# Start Tailwind watch in background
echo "👀 Starting Tailwind watch mode..."
pnpm run dev > /tmp/tailwind.log 2>&1 &
TAILWIND_PID=$!

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping watch mode..."
    kill $TAILWIND_PID 2>/dev/null || true
    rm -f /tmp/tailwind.log 2>/dev/null || true
    echo "✅ Stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "✅ Tailwind watch started (PID: $TAILWIND_PID)"
echo "🔄 Watching for CSS changes..."
echo "🛑 Press Ctrl+C to stop"

# Watch for changes to the output.css file
LAST_MODIFIED=0

while true; do
    if [[ -f "./src/static/css/output.css" ]]; then
        CURRENT_MODIFIED=$(stat -f %m "./src/static/css/output.css" 2>/dev/null || stat -c %Y "./src/static/css/output.css" 2>/dev/null || echo "0")

        if [[ "$CURRENT_MODIFIED" != "$LAST_MODIFIED" ]] && [[ "$CURRENT_MODIFIED" != "0" ]]; then
            echo "📝 CSS updated! Running collectstatic..."
            cd src && python manage.py collectstatic --noinput > /dev/null 2>&1
            cd ..
            echo "✅ Django static files updated"
            LAST_MODIFIED=$CURRENT_MODIFIED
        fi
    fi

    sleep 2
done