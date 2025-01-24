// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// https://astro.build/config
export default defineConfig({
    integrations: [
      tailwind({
        applyBaseStyles: false,
      }),
      react(),
      mdx(),
    ],
    vite: {
      server: {
          watch: {
              usePolling: true,
          }
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, './src'),
        },
      },
  },
});