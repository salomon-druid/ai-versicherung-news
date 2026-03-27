import { defineCollection, z } from 'astro:content';

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    category: z.enum([
      'ki-digitalisierung',
      'versicherer',
      'versicherungsprodukte',
      'versicherungsumfeld',
      'makler',
      'risiken-schaeden',
    ]),
    tags: z.array(z.string()).optional(),
    author: z.string().default('ai-versicherung-news'),
    image: z.string().optional(),
    company: z.string().optional(),
    companyDomain: z.string().optional(),
    sources: z.array(
      z.object({
        title: z.string(),
        url: z.string().url(),
        date: z.string().optional(),
        outlet: z.string().optional(),
      })
    ),
    featured: z.boolean().default(false),
  }),
});

export const collections = { news };
