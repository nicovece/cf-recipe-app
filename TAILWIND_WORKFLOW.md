# Tailwind CSS + Django Workflow Guide

This guide explains how to work with Tailwind CSS in this Django project.

## 🚀 Quick Start

### Development Mode (Recommended)

```bash
# Start development with auto-sync to Django
pnpm run dev-django
```

This will:

- Build Tailwind CSS in watch mode
- Automatically sync changes to Django's staticfiles
- Monitor for file changes every 3 seconds

### Production Build

```bash
# Build for production and sync with Django
pnpm run build-django
```

## 📋 Available Commands

| Command                 | Description                               |
| ----------------------- | ----------------------------------------- |
| `pnpm run dev`          | Tailwind watch mode only (no Django sync) |
| `pnpm run dev-django`   | **Development mode with auto-sync**       |
| `pnpm run build`        | One-time Tailwind build (no Django sync)  |
| `pnpm run build-prod`   | Minified Tailwind build (no Django sync)  |
| `pnpm run build-django` | **Production build with Django sync**     |
| `pnpm run clean`        | Remove generated CSS files                |
| `pnpm run check`        | Check Tailwind config without building    |

## 🔧 Configuration

### Tailwind Config (`tailwind.config.js`)

- **Content Scanning**: Automatically scans HTML templates, Python files, and template tags
- **Safelist**: Includes all dynamic classes from template tags
- **Custom Colors**: Extended with project-specific color palette

### File Structure

```
src/
├── static/css/
│   ├── input.css          # Tailwind source
│   └── output.css         # Generated CSS
└── staticfiles/css/       # Django static files
    ├── input.css          # Synced from static/
    └── output.css         # Synced from static/
```

## 🎨 Custom Classes

### Template Tag Classes

The following classes are automatically included via safelist:

- Navigation: `bg-alternate_a-800/70`, `backdrop-blur-sm`, `text-accent-300`
- Footer: `fixed`, `z-50`, `bottom-0`, `text-accent-800`
- Forms: `form-field`, `form-label`, `errorlist`

### Custom Colors

- `ground_a`: Warm earth tones (50-900)
- `alternate_a`: Cool greens (100-800)
- `accent`: Orange accent colors (100-900)

## 🐛 Troubleshooting

### Styles Not Appearing

1. **Check if files are synced**:

   ```bash
   ls -la src/static/css/output.css src/staticfiles/css/output.css
   ```

2. **Manual sync**:

   ```bash
   source recipeapp/bin/activate
   python src/manage.py collectstatic --noinput
   ```

3. **Rebuild everything**:
   ```bash
   pnpm run clean
   pnpm run build-django
   ```

### Development Mode Issues

- If auto-sync stops working, restart with `pnpm run dev-django`
- Check that the virtual environment is activated
- Ensure Django development server is running

### Missing Classes

- Check if the class is in the safelist in `tailwind.config.js`
- Verify the class is used in templates
- Run `pnpm run check` to validate config

## 🔄 Workflow Examples

### Daily Development

```bash
# Terminal 1: Start Django server
source recipeapp/bin/activate
python src/manage.py runserver

# Terminal 2: Start Tailwind development
pnpm run dev-django
```

### Before Deployment

```bash
# Build production CSS and sync
pnpm run build-django

# Deploy your Django app
```

### Adding New Classes

1. Use classes in your templates
2. If they're dynamic (from template tags), add to safelist in `tailwind.config.js`
3. Run `pnpm run build-django` to rebuild

## 📁 File Locations

- **Tailwind Config**: `tailwind.config.js`
- **CSS Source**: `src/static/css/input.css`
- **Generated CSS**: `src/static/css/output.css`
- **Django Static**: `src/staticfiles/css/output.css`
- **Build Scripts**: `build.sh`, `dev.sh`

## 🎯 Best Practices

1. **Use `pnpm run dev-django` for development** - it handles everything automatically
2. **Add dynamic classes to safelist** - prevents purging of template-generated classes
3. **Run `pnpm run build-django` before deployment** - ensures production-ready CSS
4. **Check file sync** if styles aren't appearing - Django serves from `staticfiles/`
5. **Use custom colors consistently** - they're defined in the Tailwind config

## 🚨 Common Issues

### "Styles not loading"

- Django serves from `staticfiles/`, not `static/`
- Run `pnpm run build-django` to sync files

### "Classes missing after build"

- Add dynamic classes to safelist in `tailwind.config.js`
- Rebuild with `pnpm run build-django`

### "Watch mode not syncing"

- Check if virtual environment is activated
- Restart with `pnpm run dev-django`
- Verify Django server is running
