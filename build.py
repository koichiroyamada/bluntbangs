import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import config
from datetime import datetime

def build():
    # 設定読み込み
    content_dir = Path(config.CONTENT_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    template_dir = Path(config.TEMPLATE_DIR)
    static_dir = Path(config.STATIC_DIR)

    # 1. 出力ディレクトリを初期化（クリーンビルド）
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 2. テンプレートの準備
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('base.html')

    # 日付整形用関数
    def fmt_iso(d):
        if not d: return ""
        try:
            dt = datetime.strptime(d, '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except ValueError: return d

    # 3. Content（記事）をスキャンして情報を収集
    pages = []
    for md_file in sorted(content_dir.glob('*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Markdown変換（Meta情報取得付き）
        md = markdown.Markdown(extensions=['meta', 'fenced_code'])
        html_content = md.convert(text)
        meta = md.Meta if hasattr(md, 'Meta') else {}

        # 下書きはスキップ
        if meta.get('status', [''])[0].lower() == 'draft':
            continue

        # メタデータ不足の警告
        if 'title' not in meta:
            print(f"Warning: '{md_file.name}' is missing 'Title'. Using filename.")
        if 'date' not in meta:
            print(f"Warning: '{md_file.name}' is missing 'Date'.")

        title = meta.get('title', [md_file.stem])[0]
        output_filename = f"{md_file.stem}.html"

        pages.append({
            'title': title,
            'url': output_filename,
            'content': html_content,
            'meta': meta,
            'date_iso': fmt_iso(meta.get('date', [''])[0]),
            'update_iso': fmt_iso(meta.get('update', [''])[0]),
        })

    # 4. 記事リストを日付順（降順）にソート
    # Static処理の前にソートすることで、index.html生成時に正しい順序のrecent_pagesを渡せる
    pages.sort(key=lambda x: x['meta'].get('date', [''])[0], reverse=True)

    # トップページ用に更新日順（更新日がなければ作成日）でソートしたリストを作成
    recent_pages = sorted(pages, key=lambda x: x['update_iso'] or x['date_iso'], reverse=True)[:5]

    # 5. Static（固定生成）の処理
    # mdファイル以外はコピー、mdファイルはHTMLに変換して配置
    if static_dir.exists():
        for file_path in static_dir.rglob('*'):
            # 出力先のパスを計算
            rel_path = file_path.relative_to(static_dir)
            dest_path = output_dir / rel_path

            if file_path.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
                continue

            if file_path.suffix == '.md':
                # Markdownなら変換してHTML配置
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                md = markdown.Markdown(extensions=['meta', 'fenced_code'])
                html_content = md.convert(text)
                meta = md.Meta if hasattr(md, 'Meta') else {}
                
                # 出力ファイル名を .html に変更
                dest_html_path = dest_path.with_suffix('.html')

                # 日付データの生成
                date_iso = fmt_iso(meta.get('date', [''])[0])
                update_iso = fmt_iso(meta.get('update', [''])[0])
                
                context = {
                    'site_name': config.SITE_NAME,
                    'title': meta.get('title', [file_path.stem])[0],
                    'page_title': f"{meta.get('title', [file_path.stem])[0]} | {config.SITE_NAME}",
                    'content': html_content,
                    'meta': meta,
                    'copyright': config.COPYRIGHT,
                    'google_analytics_id': config.GOOGLE_ANALYTICS_ID,
                    'menu_items': config.MENU_ITEMS,
                    'all_pages': pages, # 記事リストも渡しておく
                    'recent_pages': recent_pages, # 最新記事リスト（更新日順）
                    'date_iso': date_iso,
                    'update_iso': update_iso,
                    'current_url': str(dest_html_path.relative_to(output_dir)).replace('\\', '/'),
                }
                
                output_html = template.render(context)
                with open(dest_html_path, 'w', encoding='utf-8') as f:
                    f.write(output_html)
            else:
                # それ以外（画像、CSSなど）はそのままコピー
                shutil.copy2(file_path, dest_path)

    # 6. Content（記事）の各ページを生成
    count = 0
    for i, page in enumerate(pages):
        # 前後の記事を取得 (pagesは降順: 新しい -> 古い)
        # newer (新しい記事) は index が小さい方
        newer_post = pages[i-1] if i > 0 else None
        # older (古い記事) は index が大きい方
        older_post = pages[i+1] if i < len(pages) - 1 else None

        # テンプレートに渡すデータ
        context = {
            'site_name': config.SITE_NAME,
            'title': page['title'],
            'page_title': f"{page['title']} | {config.SITE_NAME}",
            'content': page['content'],
            'meta': page['meta'],
            'copyright': config.COPYRIGHT,
            'google_analytics_id': config.GOOGLE_ANALYTICS_ID,
            'menu_items': config.MENU_ITEMS,
            'all_pages': pages,
            'recent_pages': recent_pages,
            'newer_post': newer_post,
            'older_post': older_post,
            'date_iso': page['date_iso'],
            'update_iso': page['update_iso'],
            'current_url': page['url'],
        }

        # HTML書き出し
        output_html = template.render(context)
        with open(output_dir / page['url'], 'w', encoding='utf-8') as f:
            f.write(output_html)
        count += 1

    # 7. アーカイブページの生成
    archive_list_html = '<ul class="archive-list">'
    for page in pages:
        date_html = f'<span class="date">{page["date_iso"]}</span>'
        if page['update_iso']:
            date_html += f'<span class="update">{page["update_iso"]}<span class="update-label">UPDATE</span></span>'

        archive_list_html += f'<li><div class="date-container">{date_html}</div><a href="{page["url"]}">{page["title"]}</a></li>'
    archive_list_html += "</ul>"

    archive_context = {
        'site_name': config.SITE_NAME,
        'page_title': f"Archives | {config.SITE_NAME}",
        'content': f"<h2>Archives</h2>{archive_list_html}",
        'meta': {},
        'copyright': config.COPYRIGHT,
        'google_analytics_id': config.GOOGLE_ANALYTICS_ID,
        'menu_items': config.MENU_ITEMS,
        'all_pages': pages,
        'recent_pages': recent_pages,
        'current_url': 'archive.html',
    }
    with open(output_dir / 'archive.html', 'w', encoding='utf-8') as f:
        f.write(template.render(archive_context))

    # 8. index.html の自動生成（static/index.md がない場合のプレースホルダー）
    if not (output_dir / 'index.html').exists():
        recent_posts_html = '<ul class="archive-list">'
        # 簡易的にリストの上位を表示
        for page in recent_pages:
            recent_posts_html += f'<li><div class="date-container"><span class="date">{page["date_iso"]}</span></div><a href="{page["url"]}">{page["title"]}</a></li>'
        recent_posts_html += "</ul>"
        
        index_context = {
            'site_name': config.SITE_NAME,
            'page_title': config.SITE_NAME,
            'content': f"<h2>Welcome</h2><p>Welcome to {config.SITE_NAME}.</p><h3>Recent Pages</h3>{recent_posts_html}",
            'meta': {},
            'copyright': config.COPYRIGHT,
            'google_analytics_id': config.GOOGLE_ANALYTICS_ID,
            'menu_items': config.MENU_ITEMS,
            'all_pages': pages,
            'recent_pages': recent_pages,
            'current_url': 'index.html',
        }
        with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(template.render(index_context))
        count += 1
            
    print(f"Build complete. {count} pages generated in '{output_dir}'.")

if __name__ == "__main__":
    build()