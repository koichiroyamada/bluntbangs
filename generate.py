import os
import shutil
import markdown
import config
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime

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
    template = env.get_template('base.html')

    posts = []
    # コンテンツディレクトリがない場合のハンドリング
    if not content_dir.exists():
        print(f"Warning: Content directory '{content_dir}' not found.")
        return

    for md_file in content_dir.glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
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

            posts.append({
                'content': html_content,
                'date': post_date,
                'formatted_date': post_date.strftime('%Y.%m.%d'),
                'meta': meta
            })

    posts.sort(key=lambda x: x['date'], reverse=True)

    html = template.render(
        site_name=config.SITE_NAME,
        description=config.SITE_DESCRIPTION,
        copyright=config.COPYRIGHT,
        posts=posts
    )

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    if static_dir.exists():
        shutil.copytree(static_dir, output_dir / 'static')

    print(f"Build complete! Generated {len(posts)} posts to {output_dir}")

if __name__ == "__main__":
    generate()
