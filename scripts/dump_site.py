#!/usr/bin/env python3
"""
Complete Site Dump & Exporter for behaviouralscience.net
Extracts:
1. All Posts (JSON + Markdown with YAML frontmatter + comments)
2. All Pages (JSON + Markdown)
3. Taxonomies (Categories, Tags)
4. Comments (linked to posts)
5. Media Assets (images, PDFs, graphics)
6. Raw HTML Snapshots (from sitemap.xml)
7. Manifest & Index CSV
"""

import os
import re
import csv
import json
import time
import urllib.request
import urllib.parse
from html import unescape
from xml.etree import ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP_DIR = os.path.join(BASE_DIR, "dump")
RAW_JSON_DIR = os.path.join(DUMP_DIR, "raw_json")
MEDIA_DIR = os.path.join(DUMP_DIR, "media")
HTML_DIR = os.path.join(DUMP_DIR, "html")
POSTS_MD_DIR = os.path.join(DUMP_DIR, "posts_markdown")
PAGES_MD_DIR = os.path.join(DUMP_DIR, "pages_markdown")

WP_API_BASE = "https://public-api.wordpress.com/rest/v1.1/sites/behaviouralscience.wordpress.com"
SITE_URL = "https://behaviouralscience.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for d in [RAW_JSON_DIR, MEDIA_DIR, HTML_DIR, POSTS_MD_DIR, PAGES_MD_DIR]:
    os.makedirs(d, exist_ok=True)

def fetch_url(url, as_json=True, retries=3):
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if as_json:
                    return json.loads(data.decode("utf-8"))
                return data
        except Exception as e:
            if attempt == retries - 1:
                print(f"[ERROR] Failed to fetch {url}: {e}")
                return None
            time.sleep(1)

def html_to_clean_markdown(html_text):
    if not html_text:
        return ""
    
    text = html_text
    # Standardize breaks and paragraphs
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL|re.IGNORECASE)
    
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n'.join(['> ' + line.strip() for line in m.group(1).strip().split('\n')]) + '\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>', r'![\2](\1)', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', r'![](\1)', text, flags=re.DOTALL|re.IGNORECASE)
    
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', r'\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<hr\s*/?>', r'\n---\n', text, flags=re.IGNORECASE)
    
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?(?:ul|ol)[^>]*>', r'\n', text, flags=re.IGNORECASE)
    
    text = re.sub(r'<[^>]+>', '', text)
    text = unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    print("=== Starting behaviouralscience.net Site Dump ===")
    
    # 1. Site Info
    print("\n[1/6] Fetching site metadata...")
    site_info = fetch_url(WP_API_BASE)
    if site_info:
        with open(os.path.join(RAW_JSON_DIR, "site_info.json"), "w", encoding="utf-8") as f:
            json.dump(site_info, f, indent=2, ensure_ascii=False)
        print(f" -> Site Name: {site_info.get('name')}")
        print(f" -> Description: {site_info.get('description')}")
        print(f" -> Subscribers: {site_info.get('subscribers_count')}")

    # 2. Taxonomies (Categories & Tags)
    print("\n[2/6] Fetching categories and tags...")
    cats_data = fetch_url(f"{WP_API_BASE}/categories?number=100")
    categories = cats_data.get("categories", []) if cats_data else []
    with open(os.path.join(RAW_JSON_DIR, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    print(f" -> Saved {len(categories)} categories")

    tags = []
    page = 1
    while True:
        tags_data = fetch_url(f"{WP_API_BASE}/tags?number=100&page={page}")
        if not tags_data or "tags" not in tags_data:
            break
        current_tags = tags_data["tags"]
        if not current_tags:
            break
        tags.extend(current_tags)
        if len(tags) >= tags_data.get("found", len(tags)):
            break
        page += 1
    with open(os.path.join(RAW_JSON_DIR, "tags.json"), "w", encoding="utf-8") as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)
    print(f" -> Saved {len(tags)} tags")

    # 3. Comments
    print("\n[3/6] Fetching all comments...")
    comments = []
    page = 1
    while True:
        comments_data = fetch_url(f"{WP_API_BASE}/comments?number=100&page={page}")
        if not comments_data or "comments" not in comments_data:
            break
        current_comments = comments_data["comments"]
        if not current_comments:
            break
        comments.extend(current_comments)
        if len(comments) >= comments_data.get("found", len(comments)):
            break
        page += 1
    with open(os.path.join(RAW_JSON_DIR, "comments.json"), "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)
    print(f" -> Saved {len(comments)} comments")

    # Group comments by post ID
    comments_by_post = {}
    for c in comments:
        post_id = c.get("post", {}).get("ID")
        if post_id:
            comments_by_post.setdefault(post_id, []).append(c)

    # 4. Posts
    print("\n[4/6] Fetching all posts...")
    posts = []
    page = 1
    while True:
        posts_data = fetch_url(f"{WP_API_BASE}/posts?number=100&page={page}")
        if not posts_data or "posts" not in posts_data:
            break
        current_posts = posts_data["posts"]
        if not current_posts:
            break
        posts.extend(current_posts)
        if len(posts) >= posts_data.get("found", len(posts)):
            break
        page += 1

    with open(os.path.join(RAW_JSON_DIR, "posts.json"), "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f" -> Saved {len(posts)} posts to raw JSON")

    media_urls = set()
    manifest_rows = []

    # Generate Markdown for Posts
    for p in posts:
        pid = p.get("ID")
        title = unescape(p.get("title", "Untitled"))
        date = p.get("date", "")
        modified = p.get("modified", "")
        slug = p.get("slug", f"post-{pid}")
        url = p.get("URL", "")
        author = p.get("author", {}).get("name", "")
        categories_list = list(p.get("categories", {}).keys())
        tags_list = list(p.get("tags", {}).keys())
        excerpt = html_to_clean_markdown(p.get("excerpt", ""))
        content_html = p.get("content", "")
        content_md = html_to_clean_markdown(content_html)
        post_comments = comments_by_post.get(pid, [])
        
        # Collect media links
        for m in re.findall(r'https?://[^\s"\'<>]+', content_html):
            clean_m = m.split("?")[0].replace("&#038;", "&")
            if any(clean_m.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.svg', '.webp']):
                media_urls.add(clean_m)
        
        for att in p.get("attachments", {}).values():
            if "URL" in att:
                clean_att = att["URL"].split("?")[0]
                media_urls.add(clean_att)

        featured = p.get("featured_image")
        if featured:
            media_urls.add(featured.split("?")[0])

        filename_date = date[:10] if len(date) >= 10 else "2000-01-01"
        md_filename = f"{filename_date}-{slug}.md"
        md_path = os.path.join(POSTS_MD_DIR, md_filename)

        manifest_rows.append({
            "type": "post",
            "id": pid,
            "date": date,
            "title": title,
            "slug": slug,
            "categories": ", ".join(categories_list),
            "tags": ", ".join(tags_list),
            "comments_count": len(post_comments),
            "word_count": len(content_md.split()),
            "url": url,
            "markdown_file": f"posts_markdown/{md_filename}"
        })

        frontmatter = [
            "---",
            f"id: {pid}",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            f"date: {date}",
            f"modified: {modified}",
            f"author: {json.dumps(author, ensure_ascii=False)}",
            f"url: {url}",
            f"categories: {json.dumps(categories_list, ensure_ascii=False)}",
            f"tags: {json.dumps(tags_list, ensure_ascii=False)}",
            f"excerpt: {json.dumps(excerpt, ensure_ascii=False)}",
            f"comment_count: {len(post_comments)}",
            "---",
            "",
            content_md,
            ""
        ]

        if post_comments:
            frontmatter.append("## Comments\n")
            for c in post_comments:
                c_author = c.get("author", {}).get("name", "Anonymous")
                c_date = c.get("date", "")
                c_content = html_to_clean_markdown(c.get("content", ""))
                frontmatter.append(f"### By {c_author} on {c_date}\n\n{c_content}\n")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(frontmatter))

    print(f" -> Generated {len(posts)} Markdown files in posts_markdown/")

    # 5. Pages
    print("\n[5/6] Fetching all pages...")
    pages_data = fetch_url(f"{WP_API_BASE}/posts?type=page&number=100")
    pages = pages_data.get("posts", []) if pages_data else []
    with open(os.path.join(RAW_JSON_DIR, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print(f" -> Saved {len(pages)} pages to raw JSON")

    for p in pages:
        pid = p.get("ID")
        title = unescape(p.get("title", "Untitled"))
        date = p.get("date", "")
        slug = p.get("slug", f"page-{pid}")
        url = p.get("URL", "")
        content_html = p.get("content", "")
        content_md = html_to_clean_markdown(content_html)
        
        for m in re.findall(r'https?://[^\s"\'<>]+', content_html):
            clean_m = m.split("?")[0].replace("&#038;", "&")
            if any(clean_m.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.svg', '.webp']):
                media_urls.add(clean_m)

        for att in p.get("attachments", {}).values():
            if "URL" in att:
                clean_att = att["URL"].split("?")[0]
                media_urls.add(clean_att)

        md_filename = f"{slug}.md"
        md_path = os.path.join(PAGES_MD_DIR, md_filename)
        
        manifest_rows.append({
            "type": "page",
            "id": pid,
            "date": date,
            "title": title,
            "slug": slug,
            "categories": "",
            "tags": "",
            "comments_count": 0,
            "word_count": len(content_md.split()),
            "url": url,
            "markdown_file": f"pages_markdown/{md_filename}"
        })

        frontmatter = [
            "---",
            f"id: {pid}",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            f"date: {date}",
            f"url: {url}",
            "---",
            "",
            content_md,
            ""
        ]
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(frontmatter))

    print(f" -> Generated {len(pages)} Markdown files in pages_markdown/")

    # Write Manifest CSV
    manifest_csv = os.path.join(DUMP_DIR, "content_manifest.csv")
    with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["type", "id", "date", "title", "slug", "categories", "tags", "comments_count", "word_count", "url", "markdown_file"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f" -> Generated content manifest CSV ({len(manifest_rows)} items)")

    # 6. Media Files & HTML Snapshots from Sitemap
    print(f"\n[6/6] Fetching Media Assets ({len(media_urls)} detected) & HTML Snapshots...")
    
    # Download media files
    for media_url in sorted(media_urls):
        try:
            parsed_path = urllib.parse.urlparse(media_url).path
            filename = os.path.basename(urllib.parse.unquote(parsed_path))
            if not filename or len(filename) > 100:
                continue
            dest = os.path.join(MEDIA_DIR, filename)
            if not os.path.exists(dest):
                print(f" -> Downloading media: {filename} ({media_url})")
                req = urllib.request.Request(media_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
                    out.write(r.read())
        except Exception as e:
            print(f" [WARN] Failed to download media {media_url}: {e}")

    # Fetch sitemap.xml and download raw HTML pages
    sitemap_raw = fetch_url(f"{SITE_URL}/sitemap.xml", as_json=False)
    if sitemap_raw:
        with open(os.path.join(RAW_JSON_DIR, "sitemap.xml"), "wb") as f:
            f.write(sitemap_raw)
        
        root = ET.fromstring(sitemap_raw)
        urls = []
        for elem in root.iter():
            if elem.tag.endswith("loc") and elem.text:
                urls.append(elem.text.strip())
        
        print(f" -> Found {len(urls)} URLs in sitemap.xml. Saving HTML snapshots...")
        for u in urls:
            try:
                parsed = urllib.parse.urlparse(u)
                path_part = parsed.path.strip("/").replace("/", "__")
                if not path_part:
                    path_part = "index"
                html_file = os.path.join(HTML_DIR, f"{path_part}.html")
                if not os.path.exists(html_file):
                    html_data = fetch_url(u, as_json=False)
                    if html_data:
                        with open(html_file, "wb") as f:
                            f.write(html_data)
            except Exception as e:
                print(f" [WARN] Failed HTML snapshot for {u}: {e}")

    print("\n=== COMPLETE SITE DUMP FINISHED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
