# bluntbangs

A minimal Static Site Generator (SSG) built with Python.
Designed for simplicity, readability, and "Sense of Control".

## Philosophy

*   **Less is More:** No complex frameworks, no heavy dependencies.
*   **Control:** Understand every single line of code.
*   **Co-creation:** Built through a dialogue between a Human and an AI (Gemini).

## Requirements

*   Python 3.8+
*   Markdown
*   Jinja2

## Installation

```bash
pip install markdown jinja2
```

## Usage

1.  Place your markdown files in `content/`.
2.  Run the build script:

```bash
python build.py
```

3.  The generated website will be in `docs/`.

## Project Structure

*   `build.py`: The core logic (approx. 200 lines).
*   `config.py`: Configuration settings.
*   `content/`: Markdown source files.
*   `templates/`: HTML templates (Jinja2).
*   `static/`: Static assets (CSS, images, etc.).
*   `docs/`: Generated output (ready for GitHub Pages).

## License

MIT