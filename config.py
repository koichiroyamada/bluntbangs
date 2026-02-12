import os
from datetime import datetime

SITE_NAME = "bluntbangs"
SITE_URL = os.environ.get("SITE_URL", "https://www.bluntbangs.com")  # 環境変数から取得、なければデフォルト値
SITE_DESCRIPTION = "このサイトはあれこれ試しているところです。"
COPYRIGHT = f"© {datetime.now().year} bluntbangs"
GOOGLE_ANALYTICS_ID = "G-405M9FNRRJ"

# パス設定
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "docs"
STATIC_DIR = "static"
