#!/bin/bash
# Quick sync script: rebuild CSS and update Django
pnpm run build && python manage.py collectstatic --noinput
echo "✅ CSS synced!"