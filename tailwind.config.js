/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.html",
    "./src/templates/**/*.html",
    "./src/recipes/templates/**/*.html",
    "./src/recipe_project/**/*.py",
    "./src/recipes/**/*.py",
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
          // 300: '#FBCCA6',
          300: '#88928F',
          400: '#6fc3aa',
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
    },
  },
  plugins: [],
}

