# Nomalyze

A smart Django web application for managing and analyzing recipes. Nomalyze allows you to create, store, and organize recipes with automatic difficulty calculation and advanced data analytics based on cooking time and ingredients.

**🌐 Live Application:** [https://cf-recipe-app.onrender.com](https://cf-recipe-app.onrender.com)

## About the Name

**Nomalyze** combines "nom" (the sound of eating) with "analyze" - perfectly capturing our app's dual purpose of helping you discover delicious recipes while providing intelligent data insights about your cooking patterns and preferences.

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

- **Smart Recipe Management**: Create and store recipes with names, ingredients, and cooking times
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
   cd nomalyze
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
nomalyze/
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

## Maintainer & Contact

**Maintained by:** Nico Vece

**Contact:**
- Email: m@nicovece.com
- GitHub: [@nicovece](https://github.com/nicovece)
- LinkedIn: [nicovece](https://www.linkedin.com/in/nicovece/)
- Portfolio: [nicovece.github.io/cf-portfolio-astro](https://nicovece.github.io/cf-portfolio-astro/)

## Getting Help

If you encounter any issues or have questions:

1. **Check the Documentation**: Review this README and code comments
2. **Open an Issue**: Create an issue on the [GitHub repository](https://github.com/nicovece/cf-recipe-app/issues)
3. **Contact the Maintainer**: Reach out via email at m@nicovece.com

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

Please ensure your code follows Django best practices and includes appropriate tests.

## License

MIT License - Feel free to use this project for learning and portfolio purposes.
