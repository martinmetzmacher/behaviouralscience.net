---
date: 2026-08-28
project: behaviouralscience.net (Website Machine / Thought Leadership)
source_interview: interviews/2026-08-28-site-rebuild-interview.md
execution_tier: high — judgment-bearing & aesthetic architecture
status: ready
---

# BRIEF — Rebuild behaviouralscience.net as an Ultra-Sleek Editorial Publication

> The contract. Written at RELEASE, before execution starts.
> **Test:** could a competent stranger execute this without asking me anything?

## Goal

Transform the extracted WordPress dump of `behaviouralscience.net` into an ultra-fast, modern, iA Writer / Substack-aesthetic Astro publication that preserves 100% of historical URLs verbatim to protect SEO PageRank authority, while providing a stunning reading experience for Martin's thought-leadership and future essays.

## Why

The domain has strong historical authority and backlink profile. By migrating off WordPress.com onto a modern Astro static architecture, we eliminate bloat and maintenance costs while turning the site into an editorial authority asset. Maintaining verbatim URL continuity ensures Google sees zero breakages.

## Decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | **Astro + Tailwind CSS** | Ultra-fast SSG, 100 Lighthouse score, Markdown Content Collections, matching the stack used in `paartherapie.in`. |
| D2 | **Verbatim Legacy URL Parity** (`/[year]/[month]/[day]/[slug]/`) | Guarantees 100% URL continuity for all 61 archived articles, protecting legacy Google PageRank and backlinks. |
| D3 | **iA Writer / Substack Aesthetic** | Typography-first design: Newsreader serif for body, Inter for UI metadata, JetBrains Mono accents, generous margins, subtle reading time, and zero visual clutter. |
| D4 | **Dark / Light Mode Toggle** | Seamless client-side theme switcher with zero flash (using CSS variables and `localStorage`). |
| D5 | **Editorial Metadata & Author Footnote** | Clean author bio linking Martin's academic roots with current books, diagnostics, and projects. |
| D6 | **Integrated Historical Comments** | Cleanly rendered reader discussions at the bottom of archived articles. |
| D7 | **Cloudflare Pages / Static Ready** | Ready for 1-click zero-cost deployment to Cloudflare Pages. |
| D8 | **Hybrid Authority Model (Farnam Street / HBR)** | Combines high-volume SEO traffic engine (frameworks/comparisons) with personal branding (Martin's scientific anchor) and multi-stream conversion (B2B advisory, couples diagnostics at `paartherapie.in`, books, and curated high-ticket education programs). No low-end affiliate spam. |

## Deliverables

1. `package.json`, `astro.config.mjs`, `tailwind.config.mjs` — Modern Astro project setup.
2. `src/content/blog/` — All 61 posts organized as typed Content Collections.
3. `src/content/pages/` — All 7 static pages (About, Martin Metzmacher bio, etc.).
4. `src/pages/[year]/[month]/[day]/[slug].astro` — Verbatim date-based post route handler matching original WordPress URLs.
5. `src/pages/[...slug].astro` — Static page route handler for `/about-behavioural-science-blog/`, `/martin-metzmacher/`, etc.
6. `src/pages/index.astro` — Sleek editorial homepage featuring lead essays, curated topic indexes, search/filter, and author narrative.
7. `src/pages/category/[category].astro` & `src/pages/tag/[tag].astro` — Topic exploration pages.
8. `src/layouts/BaseLayout.astro` & `src/layouts/PostLayout.astro` — Typography-first responsive layouts with dark/light mode.
9. `src/components/Header.astro`, `Footer.astro`, `AuthorCard.astro`, `ThemeToggle.astro`, `CommentList.astro`.
10. `public/` — Static assets, downloaded media images, favicon, and robots.txt.

## Constraints

- Must build cleanly with `npm run build` producing static HTML in `dist/`.
- Must preserve exact historical post permalinks `/[year]/[month]/[day]/[slug]/`.
- Zero bloated trackers or heavy client JS.

## Out of Scope

- Setting up an active paid newsletter sending server (can be added later via Substack/Buttondown embed).
- User authentication/login (site is 100% static & publicly readable).

## Done Means

- [ ] Astro build passes with zero errors (`npm run build`).
- [ ] All 61 historical posts render at their exact historical `/YYYY/MM/DD/slug/` paths.
- [ ] Static pages render at their original slugs (e.g. `/martin-metzmacher/`).
- [ ] Aesthetic matches iA Writer / Substack editorial purity (clean serif typography, dark/light mode).
- [ ] Media assets and images render properly locally.
