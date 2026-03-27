/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff8ff',
          100: '#dbeffe',
          200: '#bee3fe',
          300: '#91d3fd',
          400: '#5db9fa',
          500: '#38a2f6',
          600: '#2183eb',
          700: '#196bd8',
          800: '#1b57af',
          900: '#1c4b8a',
          950: '#0f2b46',
        },
        accent: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        navy: '#0f2b46',
        cyan: '#38bdf8',
        gold: '#f59e0b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
