#!/bin/bash

# Django management script - runs manage.py commands from the src directory
# Usage: ./manage.sh [command] [options]

if [ $# -eq 0 ]; then
    echo "Usage: ./manage.sh [command] [options]"
    echo "Examples:"
    echo "  ./manage.sh runserver"
    echo "  ./manage.sh makemigrations"
    echo "  ./manage.sh migrate"
    echo "  ./manage.sh createsuperuser"
    echo "  ./manage.sh shell"
    exit 1
fi

# Change to src directory and run the command
cd src && python manage.py "$@"
