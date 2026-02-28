import os
import shutil
import markdown
import re
import config
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime
from email.utils import format_datetime

def setup_output_dir(output_path: Path):
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

def parse_date(date_str, file_stat):
    """
    日付文字列を解析し、datetimeオブジェクトを返す。
    文字列が無効な場合は、ファイルの最終更新日時を使用する。
    """
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return datetime.fromtimestamp(file_stat.st_mtime)
    else:
        return datetime.fromtimestamp(file_stat.st_mtime)

def generate():
    content_dir = Path(config.CONTENT_DIR)
    template_dir = Path(config.TEMPLATE_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    static_dir = Path(config.STATIC_DIR)

    setup_output_dir(output_dir)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    index_template = env.get_template('index.html')
    post_template = env.get_template('post.html') # 記事用テンプレート
    page_template = env.get_template('page.html') # 固定ページ用テンプレート
    not_found_template = env.get_template('404.html')
    feed_template = env.get_template('feed.xml')
    sitemap_template = env.get_template('sitemap.xml')

    posts = []
    # コンテンツディレクトリがない場合のハンドリング
    if not content_dir.exists():
        print(f"Warning: Content directory '{content_dir}' not found.")
        return

    # 1. まず全記事を読み込んでリストを作成
    for md_file in sorted(content_dir.glob('*.md')):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                text = f.read()
                # Meta拡張を使ってタイトルや日付を取得
                md = markdown.Markdown(extensions=['meta', 'fenced_code'])
                html_content = md.convert(text)
                meta = md.Meta if hasattr(md, 'Meta') else {}

                # 日付、タイトル、タイプを取得
                date_str = meta.get('date', [None])[0]
                post_date = parse_date(date_str, md_file.stat())
                title = meta.get('title', [md_file.stem])[0]
                page_type = meta.get('type', ['post'])[0]
                image = meta.get('image', [None])[0]

                # slugとURLを生成
                slug = md_file.stem
                output_filename = f"{slug}.html"
                full_url = f"{config.SITE_URL}/{output_filename}"

                # 抜粋用にHTMLタグを除去
                plain_text = re.sub(r'<[^>]+>', '', html_content)

                post_data = {
                    'content': html_content,
                    'title': title,
                    'date': post_date,
                    'formatted_date': post_date.strftime('%Y.%m.%d'),
                    'rss_date': format_datetime(post_date), # RSS用の日付形式
                    'url': output_filename,
                    'full_url': full_url,
                    'image': image,
                    'excerpt': plain_text[:100], # タグを除去したテキストから抜粋
                    'meta': meta
                }

                if page_type == 'page':
                    # 固定ページを生成
                    template = page_template  # Use page_template for pages
                    page_html = template.render(
                    site_name=config.SITE_NAME,
                    site_url=config.SITE_URL,
                    site_description=config.SITE_DESCRIPTION,
                    page_title=f"{title} | {config.SITE_NAME}",
                    description=title,
                    copyright=config.COPYRIGHT,
                    post=post_data,
                    google_analytics_id=config.GOOGLE_ANALYTICS_ID,
                    lastmod=post_date.strftime('%Y-%m-%d'),
                    full_url=full_url,
                    og_type="website"
                )
                    with open(output_dir / output_filename, 'w', encoding='utf-8') as f:
                        f.write(page_html)
                else:
                    posts.append(post_data)
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    # 2. 日付順にソート（新しい順）
    posts.sort(key=lambda x: x['date'], reverse=True)

    # 3. 前後の記事へのリンク情報を付与して個別ページ生成
    for i, post in enumerate(posts):
        # より新しい記事（リスト上の前の要素）
        if i > 0:
            post['newer_post'] = posts[i-1]
        # より古い記事（リスト上の次の要素）
        if i < len(posts) - 1:
            post['older_post'] = posts[i+1]

        post_html = post_template.render(
            site_name=config.SITE_NAME,
            site_url=config.SITE_URL,
            site_description=config.SITE_DESCRIPTION,
            page_title=f"{post['title']} | {config.SITE_NAME}",
            description=post['title'],
            copyright=config.COPYRIGHT,
            post=post,
            google_analytics_id=config.GOOGLE_ANALYTICS_ID,
            full_url=post['full_url'],
            og_type="article"
        )
        with open(output_dir / post['url'], 'w', encoding='utf-8') as f:
            f.write(post_html)

    # インデックスページ生成
    html = index_template.render(
        site_name=config.SITE_NAME,
        site_url=config.SITE_URL,
        site_description=config.SITE_DESCRIPTION,
        page_title=config.SITE_NAME,
        description=config.SITE_DESCRIPTION,
        copyright=config.COPYRIGHT,
        posts=posts,
        google_analytics_id=config.GOOGLE_ANALYTICS_ID,
        full_url=config.SITE_URL,
        og_type="website"
    )

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 404ページ生成
    html_404 = not_found_template.render(
        site_name=config.SITE_NAME,
        site_url=config.SITE_URL,
        site_description=config.SITE_DESCRIPTION,
        page_title=f"Page Not Found | {config.SITE_NAME}",
        description="Page Not Found",
        copyright=config.COPYRIGHT,
        google_analytics_id=config.GOOGLE_ANALYTICS_ID,
        full_url=f"{config.SITE_URL}/404.html",
        og_type="website"
    )
    with open(output_dir / '404.html', 'w', encoding='utf-8') as f:
        f.write(html_404)

    # RSSフィード生成（最新10件）
    feed_xml = feed_template.render(
        site_name=config.SITE_NAME,
        site_url=config.SITE_URL,
        site_description=config.SITE_DESCRIPTION,
        last_build_date=format_datetime(datetime.now()),
        posts=posts[:10]
    )
    with open(output_dir / 'feed.xml', 'w', encoding='utf-8') as f:
        f.write(feed_xml)

    # サイトマップ生成
    sitemap_xml = sitemap_template.render(
        site_url=config.SITE_URL,
        posts=posts
    )
    with open(output_dir / 'sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    if static_dir.exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', '__pycache__'))

    print(f"Build complete! Generated index and {len(posts)} posts to {output_dir}")

if __name__ == "__main__":
    generate()
