/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        'primary': {
          DEFAULT: '#3761F2',
          50: '#E8EEFE',
          100: '#D1DDFD',
          200: '#A4BAFB',
          300: '#7698F9',
          400: '#4975F7',
          500: '#3761F2',
          600: '#0C3CE8',
          700: '#0930B6',
          800: '#072383',
          900: '#041651',
        },
        'secondary': {
          DEFAULT: '#0D1425',
          50: '#1F355A',
          100: '#182B4A',
          200: '#15243F',
          300: '#111C31',
          400: '#0D1425',
          500: '#0A101D',
          600: '#080C16',
          700: '#06090E',
          800: '#030407',
          900: '#000000',
        },
      },
    },
  },
  plugins: [],
} 