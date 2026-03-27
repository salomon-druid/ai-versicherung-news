import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://ai-versicherung-news.vercel.app',
  integrations: [
    sitemap({
      changefreq: 'daily',
      priority: 0.7,
      lastmod: new Date(),
      serialize(item) {
        if (item.url.includes('/news/')) {
          item.changefreq = 'daily';
          item.priority = 0.9;
        }
        return item;
      },
    }),
    tailwind(),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
  output: 'static',
});
