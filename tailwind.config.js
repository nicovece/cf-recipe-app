/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // HTML templates
    "./src/**/*.html",
    "./src/templates/**/*.html",
    "./src/recipes/templates/**/*.html",
    
    // Python files (Django views, models, etc.)
    "./src/recipe_project/**/*.py",
    "./src/recipes/**/*.py",
    
    // Template tag files specifically
    "./src/recipes/templatetags/**/*.py",
    
    // JavaScript files (if any)
    "./src/static/**/*.js",
    
    // Include all files that might contain Tailwind classes
    "./src/**/*.{html,py,js,ts,jsx,tsx}",
  ],
  safelist: [
    // Hover states
    'hover:text-orange-600',
    'hover:border-orange-600',
    'hover:text-accent-600',
    'hover:border-accent-600',
    'hover:text-white',
    'hover:bg-accent-400',
    'hover:border-accent-400',
    'hover:rounded-md',
    'hover:text-accent-800',
    'hover:scale-105',
    'hover:shadow-xl',
    'hover:underline',
    
    // Navigation classes (from template tags)
    'bg-alternate_a-800/70',
    'backdrop-blur-sm',
    'bg-alternate_a-100',
    'text-accent-300',
    'text-accent-600',
    'border-accent-300',
    'border-l',
    'border-alternate_a-700',
    'border-alternate_a-300',
    'text-accent-800',
    
    // Footer classes (from template tags)
    'fixed',
    'right-0',
    'z-50',
    'bottom-0',
    'left-0',
    'text-accent-300',
    'border-t',
    'border-gray-200',
    'text-accent-800',
    
    // Custom utility classes
    '!border-2',
    '!border-accent-600',
    'border-2',
    'border-4',
    'border',
    
    // Form and component classes
    'form-field',
    'form-label',
    'errorlist',
    'errorlist.nonfield',
    'errorlist.field-errors',
    'success-message',
    'info-message',
  ],
  theme: {
    extend: {
      colors: {
        ground_a: {
          50: '#fdfbf7',
          100: '#F7F0DE',
          200: '#efe0c0',
          300: '#e6d0a2',
          400: '#D7B25B',
          500: '#d1a94a',
          600: '#c99a3a',
          700: '#b8862e',
          800: '#966e28',
          900: '#7a5a26',
        },
        ground_b: '#c0a659',
        alternate_b: '#a9c57c',
        alternate_a: {
          100: '#E2F3EE',
          200: '#BAE2D6',
          300: '#8CCFBB',
          400: '#6fc3aa',
          500: '#55b799',
          700: '#6A7572',
          800: '#162722',
        },
        accent: {
          100: '#FDE5D3',
          300: '#F8B27A',
          400: '#F47F21',
          600: '#E36F10',
          800: '#61330D',
          900: '#311907',
        },
      },
      fontFamily: {
        serif: ['Merriweather', 'serif'],
      },
      aspectRatio: {
        '4/3': '4 / 3',
      },
    },
  },
  plugins: [],
}

