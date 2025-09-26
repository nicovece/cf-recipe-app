/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Django templates
    "./src/templates/**/*.html",
    "./src/recipes/templates/**/*.html",

    // Python files that might contain Tailwind classes
    "./src/recipe_project/**/*.py",
    "./src/recipes/**/*.py",

    // JavaScript files (if any)
    "./src/static/**/*.js",

    // Include all files that might contain Tailwind classes
    "./src/**/*.{html,py,js,ts,jsx,tsx}",
  ],
  safelist: [
    // Classes that might be generated dynamically and not detected
    // by Tailwind's content scanning
    {
      pattern: /text-(gray|accent|alternate_a)-(100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /columns-(1|2|3|4|5|6|7|8|9|10|11|12|auto)/,
    },
    {
      pattern: /grid-cols-(1|2|3|4|5|6|7|8|9|10|11|12)/,
    },
    // Specific responsive grid classes
    // 'lg:grid-cols-1',
    // 'lg:grid-cols-2',
    // 'lg:grid-cols-3',
    // 'lg:grid-cols-4',
    // 'md:grid-cols-1',
    // 'md:grid-cols-2',
    // 'md:grid-cols-3',
    // 'sm:grid-cols-1',
    // 'sm:grid-cols-2',
    // Django form classes that might be added dynamically
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
        // Custom color palette from your existing design
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
  plugins: [
    require('@tailwindcss/typography'),
  ],
  corePlugins: {
    // Enable all core plugins for maximum flexibility
    scale: true,
    transform: true,
  },
}