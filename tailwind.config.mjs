/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ef',
          100: '#dcf0da',
          200: '#bce3b8',
          300: '#93cf8d',
          400: '#6ab862',
          500: '#3e7339',
          600: '#356431',
          700: '#2d5429',
          800: '#254422',
          900: '#1e381c',
          950: '#0f1f0e',
        },
        dark: '#1F2933',
        bg: '#F5F4F1',
        gold: '#D4AF37',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
