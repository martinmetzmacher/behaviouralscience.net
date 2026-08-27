#!/usr/bin/env python3
"""
Populate Astro Content Collections from dump data.
"""

import os
import shutil
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP_DIR = os.path.join(BASE_DIR, "dump")
SRC_CONTENT_BLOG = os.path.join(BASE_DIR, "src", "content", "blog")
SRC_CONTENT_PAGES = os.path.join(BASE_DIR, "src", "content", "pages")
PUBLIC_MEDIA = os.path.join(BASE_DIR, "public", "media")
PUBLIC_UPLOADS = os.path.join(BASE_DIR, "public", "wp-content", "uploads")

os.makedirs(SRC_CONTENT_BLOG, exist_ok=True)
os.makedirs(SRC_CONTENT_PAGES, exist_ok=True)
os.makedirs(PUBLIC_MEDIA, exist_ok=True)
os.makedirs(PUBLIC_UPLOADS, exist_ok=True)

# Copy media files to public
dump_media = os.path.join(DUMP_DIR, "media")
for f in os.listdir(dump_media):
    src = os.path.join(dump_media, f)
    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(PUBLIC_MEDIA, f))

# Copy posts
dump_posts = os.path.join(DUMP_DIR, "posts_markdown")
for f in os.listdir(dump_posts):
    if f.endswith(".md"):
        src = os.path.join(dump_posts, f)
        dest = os.path.join(SRC_CONTENT_BLOG, f)
        shutil.copy2(src, dest)

# Copy pages
dump_pages = os.path.join(DUMP_DIR, "pages_markdown")
for f in os.listdir(dump_pages):
    if f.endswith(".md"):
        src = os.path.join(dump_pages, f)
        dest = os.path.join(SRC_CONTENT_PAGES, f)
        shutil.copy2(src, dest)

print(f"Synced {len(os.listdir(SRC_CONTENT_BLOG))} posts and {len(os.listdir(SRC_CONTENT_PAGES))} pages into src/content/")
