Title: たった100行の魔法：Python SSGの内部構造
Date: 2026-02-17

## シンプルさの極み

前回の記事で「100行程度のスクリプト」と書きましたが、具体的にどのような仕組みで動いているのか、少し技術的な話をしましょう。

この静的サイトジェネレーター（SSG）の構造は、驚くほど単純です。

1.  **Load:** `content` ディレクトリ内のMarkdownファイルを読み込む。
2.  **Parse:** ファイルの先頭にあるメタデータ（タイトルや日付）と本文を分離する。
3.  **Render:** Jinja2テンプレートにデータを流し込み、HTMLを生成する。
4.  **Save:** `docs` ディレクトリにHTMLファイルとして保存する。

これだけです。データベースもなければ、複雑なルーティング処理もありません。

---

## アーキテクチャの解剖

では、各ステップをコードレベルで掘り下げてみましょう。

### 1. Load & Parse: メタデータの抽出

Markdownファイルの先頭には、YAML形式のようなメタデータを記述しています。これを解析するために、Pythonの標準ライブラリや正規表現を駆使することもできますが、今回は `python-markdown` ライブラリの `Meta` 拡張機能を使用しています。

```python
import markdown

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # MarkdownをHTMLに変換しつつ、メタデータを抽出
    md = markdown.Markdown(extensions=['meta'])
    html_content = md.convert(text)
    
    # メタデータは辞書型で返ってくる（値はリスト形式なので注意）
    meta = md.Meta
    
    return {
        'title': meta.get('title', ['No Title'])[0],
        'date': meta.get('date', ['1970-01-01'])[0],
        'content': html_content,
        'slug': file_path.stem  # ファイル名をURLの一部として使用
    }
```

この関数のポイントは、ファイルシステム上の「ファイル」を、Pythonプログラムで扱いやすい「辞書オブジェクト」に変換している点です。一度辞書になってしまえば、あとはリストに格納して日付順にソートしたり、フィルタリングしたりと、Pythonの強力なリスト操作機能をフル活用できます。

### 2. Render: Jinja2によるHTML生成

HTMLの生成には、Python界隈でデファクトスタンダードとなっている `Jinja2` を採用しました。

Jinja2の最大の強みは「テンプレートの継承」です。
Webサイトには、ヘッダーやフッター、ナビゲーションなど、全ページで共通する部分があります。これらを `base.html` という親テンプレートに定義し、個別の記事ページ（`article.html`）では中身だけを差し替えるという手法をとります。

**base.html (親):**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <title>{% block title %}{% endblock %} - My Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>...</header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>...</footer>
</body>
</html>
```

**article.html (子):**
```html
{% extends "base.html" %}

{% block title %}{{ article.title }}{% endblock %}

{% block content %}
    <article>
        <h1>{{ article.title }}</h1>
        <time>{{ article.date }}</time>
        <div class="post-body">
            {{ article.content }}
        </div>
    </article>
{% endblock %}
```

Python側では、このテンプレートに辞書データを渡すだけです。

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('article.html')

html = template.render(article=article_data)
```

ロジック（Python）とデザイン（HTML/CSS）が完全に分離されているため、デザインを変更したいときはPythonコードを一切触る必要がありません。これがメンテナンス性の高さに繋がります。

---

### 依存ライブラリは最小限に

使用している外部ライブラリも厳選しました。

*   `markdown`: MarkdownテキストをHTMLに変換するため。
*   `jinja2`: HTMLのテンプレートエンジンのため。

これらはPythonのエコシステムにおいて枯れた（安定した）技術であり、数年後に動かなくなるリスクは非常に低いです。

Node.jsベースのSSG（GatsbyやNext.jsなど）は、`node_modules` フォルダが数百メガバイトに膨れ上がり、依存ライブラリのバージョン不整合に悩まされることが少なくありません。対して、私たちのSSGは `pip install` するライブラリが数個だけ。環境構築も一瞬で終わります。

---

### なぜ自作するのか？

「車輪の再発明」は悪いことだとされがちです。しかし、学習目的や、自分だけの特別な要件がある場合には、再発明こそが最短の道になることがあります。

既存のSSGは「あらゆる人のあらゆる要望」に応えるために肥大化しがちです。
しかし、私たちが欲しいのは「このブログを表示するためだけの機能」です。

例えば、このサイトにはコメント欄がありません。検索機能もありません。
必要ないからです。

機能がないということは、メンテナンスするコードが少ないということであり、バグが潜む場所が少ないということです。

このシンプルさが、開発の速度と楽しさを支えています。
100行のコードなら、週末の午後だけで書き上げることができます。そして、そのコードは完全にあなたのコントロール下にあります。もし「タグ機能が欲しい」と思えば、自分で実装すればいいのです。誰かが作ったプラグインを探す必要はありません。

プログラミングの原点である「モノ作り」の喜びを、この小さなSSGは思い出させてくれます。
