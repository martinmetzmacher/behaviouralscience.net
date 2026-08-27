import { defineCollection, z } from 'astro:content';

const dateSchema = z.union([z.string(), z.date()]).transform((val) => {
  if (val instanceof Date) return val.toISOString();
  return String(val);
});

const blog = defineCollection({
  schema: z.object({
    id: z.number().optional(),
    title: z.string().default('Untitled'),
    slug: z.string().optional(),
    date: dateSchema,
    modified: dateSchema.optional(),
    author: z.string().default('Martin Metzmacher'),
    url: z.string().optional(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    excerpt: z.string().default(''),
  }),
});

const pages = defineCollection({
  schema: z.object({
    id: z.number().optional(),
    title: z.string().default('Untitled'),
    slug: z.string().optional(),
    date: dateSchema.optional(),
    url: z.string().optional(),
  }),
});

export const collections = { blog, pages };
