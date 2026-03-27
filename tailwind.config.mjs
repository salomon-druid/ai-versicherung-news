/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#edffc7',
          100: '#d4ffb0',
          200: '#b8f593',
          300: '#9aed75',
          400: '#6ee54a',
          500: '#39D12C',
          600: '#2eb824',
          700: '#259f1d',
          800: '#1d8617',
          900: '#176d12',
          950: '#0f4a0c',
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
