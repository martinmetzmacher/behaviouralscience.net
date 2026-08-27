/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        serif: ['Newsreader', 'Georgia', 'Cambria', 'serif'],
        sans: ['Plus Jakarta Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '68ch',
            color: 'inherit',
            a: {
              color: 'inherit',
              textDecoration: 'underline',
              textUnderlineOffset: '3px',
              textDecorationThickness: '1px',
              '&:hover': {
                opacity: 0.8,
              },
            },
            h1: {
              fontFamily: 'Newsreader, Georgia, serif',
              fontWeight: '500',
              letterSpacing: '-0.02em',
            },
            h2: {
              fontFamily: 'Newsreader, Georgia, serif',
              fontWeight: '500',
              letterSpacing: '-0.015em',
            },
            h3: {
              fontFamily: 'Newsreader, Georgia, serif',
              fontWeight: '500',
            },
            blockquote: {
              fontStyle: 'italic',
              borderLeftColor: 'currentColor',
              opacity: 0.9,
            },
            code: {
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '0.875em',
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
