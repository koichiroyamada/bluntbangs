import os
import shutil
import markdown
import config
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime
from email.utils import format_datetime

def setup_output_dir(output_path: Path):
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

def generate():
    content_dir = Path(config.CONTENT_DIR)
    template_dir = Path(config.TEMPLATE_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    static_dir = Path(config.STATIC_DIR)

    setup_output_dir(output_dir)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    index_template = env.get_template('index.html')
    post_template = env.get_template('post.html')
    feed_template = env.get_template('feed.xml')

    posts = []
    # コンテンツディレクトリがない場合のハンドリング
    if not content_dir.exists():
        print(f"Warning: Content directory '{content_dir}' not found.")
        return

    # 1. まず全記事を読み込んでリストを作成
    for md_file in content_dir.glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
            # Meta拡張を使ってタイトルや日付を取得
            md = markdown.Markdown(extensions=['meta', 'fenced_code'])
            html_content = md.convert(text)
            meta = md.Meta if hasattr(md, 'Meta') else {}
            
            date_str = meta.get('date', [None])[0]
            if date_str:
                try:
                    post_date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    post_date = datetime.fromtimestamp(md_file.stat().st_mtime)
            else:
                post_date = datetime.fromtimestamp(md_file.stat().st_mtime)

            # タイトル取得（メタデータになければファイル名）
            title = meta.get('title', [md_file.stem])[0]
            page_type = meta.get('type', ['post'])[0]
            # 出力ファイル名（slug.html）
            slug = md_file.stem
            output_filename = f"{slug}.html"
            full_url = f"{config.SITE_URL}/{output_filename}"

            post_data = {
                'content': html_content,
                'title': title,
                'date': post_date,
                'formatted_date': post_date.strftime('%Y.%m.%d'),
                'rss_date': format_datetime(post_date), # RSS用の日付形式
                'url': output_filename,
                'full_url': full_url,
                'excerpt': ''.join(html_content.splitlines())[:100], # 簡易的な抜粋
                'meta': meta
            }
            
            if page_type != 'page':
                posts.append(post_data)

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
        full_url=config.SITE_URL,
        og_type="website"
    )

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

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

    if static_dir.exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)

    print(f"Build complete! Generated index and {len(posts)} posts to {output_dir}")

if __name__ == "__main__":
    generate()
