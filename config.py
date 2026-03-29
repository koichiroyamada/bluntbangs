import os
import yaml
from datetime import datetime
from pathlib import Path

# YAML設定ファイルを読み込み
config_file = Path(__file__).parent / "config.yml"
with open(config_file, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

# 設定値を属性として展開
SITE_NAME = _config.get('SITE_NAME', 'bluntbangs')
COPYRIGHT = f"© {datetime.now().year} {SITE_NAME}"
GOOGLE_ANALYTICS_ID = _config.get('GOOGLE_ANALYTICS_ID', '')
MENU_ITEMS = _config.get('MENU_ITEMS', [])
CONTENT_DIR = _config.get('CONTENT_DIR', 'content')
TEMPLATE_DIR = _config.get('TEMPLATE_DIR', 'templates')
OUTPUT_DIR = _config.get('OUTPUT_DIR', 'docs')
STATIC_DIR = _config.get('STATIC_DIR', 'static')