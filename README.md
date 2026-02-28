# bluntbangs SSG

**AIとのペアプログラミングによって生まれた、ミニマルな静的サイトジェネレーター（SSG）。**

既存のフレームワーク（Hugo, Gatsby等）を使用せず、Python標準ライブラリと最小限の依存関係（Markdown, Jinja2）のみで構築されています。
「掌握感」と「デジタル・ミニマリズム」をテーマに、コードもデザインも極限までシンプルに保たれています。

## Philosophy

*   **Simplicity:** ビルドスクリプトはわずか100行程度。ブラックボックスを排除し、すべてを理解できる状態に保つ。
*   **Minimalism:** 不要な機能（コメント、検索、トラッキング）を削ぎ落とし、コンテンツ（テキスト）そのものに焦点を当てる。
*   **Co-Creation:** 人間がディレクションし、AI（Gemini Code Assist）が実装する。新しい時代の開発スタイルを実践。

## Directory Structure

```
bluntbangs/
├── content/        # 記事のMarkdownファイル置き場
├── templates/      # Jinja2テンプレート (base.html, article.html)
├── static/         # CSSや画像などの静的ファイル
├── docs/           # 生成されたHTMLが出力される (GitHub Pages公開用)
├── generate.py     # SSGの本体スクリプト
├── config.py       # サイト設定（タイトル、URL、GAタグなど）
├── Makefile        # ビルド・サーバー起動用コマンド
└── requirements.txt
```

## 必要要件

- Python 3.x

## セットアップ

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate

# 依存ライブラリのインストール
pip install -r requirements.txt
```

## 使い方

### サイトのビルド
```bash
make build
```

### ローカルプレビュー
```bash
make serve
```