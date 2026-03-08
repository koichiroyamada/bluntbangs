import os
from datetime import datetime

SITE_NAME = "bluntbangs"
COPYRIGHT = f"© {datetime.now().year} bluntbangs"
GOOGLE_ANALYTICS_ID = "G-405M9FNRRJ"

# メニュー設定
MENU_ITEMS = [
    {"name": "Home", "url": "index.html"},
    {"name": "Archives", "url": "archive.html"},
]

# ディレクトリ設定
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "docs"  # GitHub Pages用にdocsとしています
STATIC_DIR = "static"