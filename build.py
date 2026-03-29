import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import config
from datetime import datetime

def build():
    # Load configuration
    content_dir = Path(config.CONTENT_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    template_dir = Path(config.TEMPLATE_DIR)
    static_dir = Path(config.STATIC_DIR)

    # 1. Initialize output directory (clean build)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 2. Prepare templates
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('base.html')

    # 日付整形用関数（英語形式: "Mar 29, 2026"）
    def fmt_iso(d):
        if not d: return ""
        try:
            dt = datetime.strptime(d, '%Y-%m-%d')
            return dt.strftime('%b %d, %Y')
        except ValueError: return d

    # 3. Scan Content directory and collect metadata
    pages = []
    for md_file in sorted(content_dir.glob('*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Convert Markdown (with metadata extraction)
        md = markdown.Markdown(extensions=['meta', 'fenced_code'])
        html_content = md.convert(text)
        meta = md.Meta if hasattr(md, 'Meta') else {}

        # Skip draft posts
        if meta.get('status', [''])[0].lower() == 'draft':
            continue

        # Warn if metadata is missing
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

    # 4. Sort pages by date (descending)
    # Sort before static processing to ensure correct order for index.html
    pages.sort(key=lambda x: x['meta'].get('date', [''])[0], reverse=True)

    # Create sorted list for recent pages (by update date, or creation date if not updated)
    recent_pages = sorted(pages, key=lambda x: x['update_iso'] or x['date_iso'], reverse=True)[:5]

    # 5. Process static files
    # Copy non-Markdown files as-is; Markdown files are converted to HTML
    if static_dir.exists():
        for file_path in static_dir.rglob('*'):
            # Calculate output path
            rel_path = file_path.relative_to(static_dir)
            dest_path = output_dir / rel_path

            if file_path.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
                continue

            if file_path.suffix == '.md':
                continue  # Don't process .md files (migrated to content/)
            else:
                # Copy other files (images, CSS, etc.) as-is
                shutil.copy2(file_path, dest_path)

    # 6. Generate each content page
    count = 0
    for i, page in enumerate(pages):
        # Get adjacent pages (pages are sorted newest to oldest)
        # newer_post has smaller index
        newer_post = pages[i-1] if i > 0 else None
        # older_post has larger index
        older_post = pages[i+1] if i < len(pages) - 1 else None

        # Prepare data for template
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

        # Write HTML output
        output_html = template.render(context)
        with open(output_dir / page['url'], 'w', encoding='utf-8') as f:
            f.write(output_html)
        count += 1

    # 7. Generate archive page
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

    # 8. Auto-generate index.html if not already created by processing content files
    if not (output_dir / 'index.html').exists():
        recent_posts_html = '<ul class="archive-list">'
        # Display recent posts
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