# Recipe Management App

A simple Django web application for managing and storing recipes. This app allows you to create, store, and organize recipes with automatic difficulty calculation based on cooking time and ingredients.

## 🎨 Tailwind CSS Integration

This project uses Tailwind CSS for styling with a custom build workflow. See [TAILWIND_WORKFLOW.md](./TAILWIND_WORKFLOW.md) for detailed instructions on working with styles.

**Quick Start for Styling:**

```bash
# Development mode (auto-sync with Django)
pnpm run dev-django

# Production build
pnpm run build-django
```

## Features

- **Recipe Management**: Create and store recipes with names, ingredients, and cooking times
- **Automatic Difficulty Calculation**: The app automatically calculates recipe difficulty based on cooking time and number of ingredients
- **Ingredient Lists**: Store ingredients as comma-separated values with automatic list conversion
- **Cooking Time Validation**: Ensures cooking times are reasonable (1 minute to 24 hours)
- **Reference Links**: Add optional reference URLs to recipes
- **Like System**: Built-in like counting system (future feature)
- **Comments**: Support for recipe comments (future feature)

## Difficulty Levels

The app automatically calculates difficulty based on:

- **Easy**: < 10 minutes cooking time, < 4 ingredients
- **Medium**: < 10 minutes cooking time, ≥ 4 ingredients
- **Intermediate**: ≥ 10 minutes cooking time, < 4 ingredients
- **Hard**: ≥ 10 minutes cooking time, ≥ 4 ingredients

## Requirements

- Python 3.x
- Django 5.2.5+

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd cf-recipe-app
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```bash
   ./manage.sh migrate
   ```

4. Create a superuser (optional):

   ```bash
   ./manage.sh createsuperuser
   ```

5. Run the development server:

   ```bash
   ./manage.sh runserver
   ```

6. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

The app includes a convenient management script (`manage.sh`) that handles Django commands from the correct directory:

- `./manage.sh runserver` - Start the development server
- `./manage.sh makemigrations` - Create database migrations
- `./manage.sh migrate` - Apply database migrations
- `./manage.sh createsuperuser` - Create an admin user
- `./manage.sh shell` - Open Django shell

## Project Structure

```
cf-recipe-app/
├── manage.sh              # Django management script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── src/                  # Django project source
    ├── manage.py         # Django management script
    ├── recipe_project/   # Main Django project
    └── recipes/          # Recipe app
        ├── models.py     # Recipe model definition
        ├── views.py      # View logic
        └── admin.py      # Admin interface
```

## Contributing

This is a simple recipe management app. Feel free to contribute by adding new features or improving existing functionality.

## License

[Add your license information here]
