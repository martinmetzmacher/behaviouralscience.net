# behaviouralscience.net — Complete Site Dump & Migration Archive

**Source Site:** [https://behaviouralscience.net](https://behaviouralscience.net) (`behaviouralscience.wordpress.com`)  
**Extracted On:** August 28, 2026  
**Archive Location:** `/Users/martinmetzmacher/axonnode/behaviouralscience.net/dump/`

---

## 📊 Summary of Extracted Content

| Content Type | Count | Destination Folder | Format |
|---|---|---|---|
| **Blog Posts** | **61** | `dump/posts_markdown/` | Markdown + YAML Frontmatter (inc. Comments) |
| **Pages** | **7** | `dump/pages_markdown/` | Markdown + YAML Frontmatter |
| **URL Inventory** | **547** | `dump/url_inventory.csv` | Full URL paths, short URLs, GUIDs & redirect targets |
| **Comments** | **78** | `dump/raw_json/comments.json` & embedded in MD | Full comment thread data |
| **Categories** | **13** | `dump/raw_json/categories.json` | JSON |
| **Tags** | **466** | `dump/raw_json/tags.json` | JSON |
| **Media Assets** | **15+** | `dump/media/` | PNG, JPG, GIF, PDF assets |
| **Raw JSON Exports**| **8 datasets** | `dump/raw_json/` | Raw REST API data |
| **HTML Snapshots** | **79** | `dump/html/` | Raw full HTML page captures |
| **Content Manifest**| **68 rows** | `dump/content_manifest.csv` | Full index & metrics |

---

## 📁 Directory Structure

```text
behaviouralscience.net/
├── README.md                  # This documentation
├── scripts/
│   └── dump_site.py          # Python dump & export automation script
└── dump/
    ├── content_manifest.csv  # CSV index of all posts/pages (date, slug, word count, comments)
    ├── raw_json/             # Complete structured database
    │   ├── site_info.json    # WordPress blog metadata & settings
    │   ├── posts.json        # All 61 posts in full API format
    │   ├── pages.json        # All 7 pages in full API format
    │   ├── categories.json   # 13 taxonomy categories
    │   ├── tags.json         # 466 taxonomy tags
    │   ├── comments.json     # 78 reader comments with author info
    │   └── sitemap.xml       # Original sitemap snapshot
    ├── posts_markdown/       # Clean Markdown posts with frontmatter & comments
    ├── pages_markdown/       # Clean Markdown pages with frontmatter
    ├── media/                # Downloaded media, images, charts, and PDFs
    └── html/                 # Offline raw HTML snapshots of all sitemap pages
```

---

## 🚀 Migration & Transfer Options

This dump is formatted to allow instant migration to any modern stack:

1. **Astro / Next.js / Nuxt / Hugo / 11ty:**
   - The files in `dump/posts_markdown/` and `dump/pages_markdown/` have standard frontmatter (`title`, `date`, `slug`, `categories`, `tags`, `excerpt`) and can be placed directly into an Astro content collection (`src/content/blog/`).
2. **WordPress (Self-Hosted or New Instance):**
   - The `dump/raw_json/posts.json` and `dump/raw_json/comments.json` can be imported via WP-CLI or standard JSON import.
3. **Database / Headless CMS (Supabase / Ghost / Sanity / Strapi):**
   - Direct ingestion using `posts.json` and `comments.json`.
