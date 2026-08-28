# Interview: behaviouralscience.net Modern Rebuild & Repositioning

**Date:** 2026-08-28  
**Topic:** Rebuilding `behaviouralscience.net` from WordPress dump into an iA Writer / Medium / Substack style publication  
**Participants:** Martin Metzmacher, Antigravity  

---

## Verbatim Q&A & User Directives

### Q1: What is the primary purpose and future role of behaviouralscience.net?
**Decision:** Flagship Thought-Leadership, Credibility & SEO Reach: The domain has strong historical authority (formerly PageRank 4). It will serve as the scientific authority anchor connecting Martin's academic/behavioural science foundation with current and future projects, books, and praxis.

### Q2: Which specific aesthetic and reading experience do you want to lead with?
**Decision:** Ultra-Minimalist iA Writer / Editorial Purity: Clean typography (Newsreader serif for articles, Inter for UI/meta, crisp mono accents), generous whitespace, distraction-free reading, monochrome minimalism, dark/light mode toggle.

### Q3: What tech stack and deployment architecture do you prefer?
**Decision:** Astro + Tailwind CSS + Cloudflare Pages: Ultra-fast static site generation (100 Lighthouse score), zero-JS reading performance by default, Markdown content collections (matching the `paartherapie.in` pipeline).

### Q4: How should historical URL routing and permalinks be structured?
**Decision (Crucial Clarification):** **Preserve 100% exact historical URL parity verbatim (`/[year]/[month]/[day]/[slug]/`)** for all 61 archived articles and original static pages (`/about-behavioural-science-blog/`, `/martin-metzmacher/`, etc.) so that Google's index and historical backlinks are completely preserved with zero ranking risk. Future articles can use clean modern routes.

### Q5: How should the domain be monetized and positioned (Branding vs. Lead Gen vs. SEO vs. Affiliate)?
**Decision:** **Hybrid Authority Platform (Farnam Street / HBR Model):**
- **Top of Funnel:** SEO traffic engine ranking on frameworks (COM-B, EAST, Nudge) and high-CPC comparisons ($17+ CPC).
- **Core Positioning:** Founder scientific bedrock for Martin Metzmacher (elevating from generic consultant to Behavioral Scientist & Systems Architect).
- **Bottom of Funnel:** Multi-stream conversion routing to:
  1. B2B Advisory & Applied Behavioral Design leads.
  2. Couples & Relationship Diagnostics (bridging cognitive bias/self-regulation into `paartherapie.in`).
  3. Books, diagnostic tools & intellectual property.
  4. Curated high-ticket education guides (MSc / Executive program partnerships) and reading lists — zero spammy affiliate banners or low-end ads.

---

## Harvested Insights & Architectural Principles

1. **SEO Parity is Paramount:** Never break an existing 200 OK link. Astro dynamic routes must support the legacy date-nested pattern `[year]/[month]/[day]/[slug].astro` directly.
2. **Editorial Purity over Widget Clutter:** The publication is designed for deep reading. Avoid distracting banners, aggressive popups, heavy social sidebars, or bloated script bundles. Prioritize pristine typographic rhythm (proportional margins, optical font sizes, KaTeX math rendering, and dark/light mode toggle).
3. **Authority Bridge:** The homepage and author pages should present Martin's academic foundation in behavioural science as the credible bedrock of his current high-leverage work, books, and diagnostic practice.
4. **Cloudflare Edge Deployment:** Deployable cleanly to Cloudflare Pages or static hosting with instant edge caching.
5. **Prestige Monetization Invariant:** Maintain institutional brand equity; only monetize via high-value consulting inquiries, relationship diagnostics, book sales, and curated high-ticket academic/executive program partnerships.
