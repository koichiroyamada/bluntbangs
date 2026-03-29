Title: Articles Archive
Date: 2026-02-17
Update: 2026-03-26

# Building a Custom Static Site Generator with AI

## The First Commit

When text appears on the screen, there's a unique joy that only those who've built something from scratch can understand. The moment "Hello, World." rendered in the browser, this project came to life.

This site, `bluntbangs`, was built without using any existing website builders. No Hugo, no Gatsby, no Next.js. Only a few kilobytes of Python script written by our hands.

### Resisting Complexity

Modern web development has become unnecessarily complex. To create a simple blog, we're forced to download hundreds of megabytes of dependencies and write cryptic configuration files. When something breaks, finding the issue takes a full day.

We decided to reject that complexity. The key concept is **"Sense of Control"** — understanding every line of code and knowing exactly what happens at each step.

This site contains not a single line of code we don't understand. There are no unnecessary features, only what's needed.

### Design Philosophy: Minimalism Through Subtraction

Just as we simplified the code, we applied the principle of subtraction to design. No banner ads, no autoplay videos, no animations that demand attention.

What remains is whitespace, typography, and content. We chose Montserrat for headings and system fonts for body text. The power lies not in what we add, but in the space we preserve.

## The Small Universe Within 200 Lines

The Python script generating this site is remarkably simple:

1. **Load:** Read Markdown files from the `content` directory
2. **Parse:** Extract metadata and convert to HTML
3. **Render:** Inject data into templates
4. **Save:** Write HTML files to the output directory

That's all. No databases, no server-side complexity. Pure transformation.

### Standing on the Shoulders of Giants

We use only essential libraries:
- `markdown`: Convert Markdown to HTML
- `jinja2`: Template rendering
- `pyyaml`: Configuration management

These are stable, time-tested tools from the Python ecosystem. The entire project remains lightweight and maintainable.

### Why Rebuild?

Building our own SSG taught us that "reinventing the wheel" isn't always bad. When you fully understand your tools, you gain complete control. If new features are needed, we add them ourselves. No waiting for plugin updates or worrying about compatibility.

## Minimalist Web Design

### Reclaiming Simplicity

Browsing the web today feels like navigating a war zone. Ads, tracking scripts, notifications, cookie banners — the signal-to-noise ratio has become unbearable.

We wanted to create a refuge. A place where content takes precedence over commerce, where attention isn't weaponized.

### Typography and Whitespace

Readability was our primary concern. We increased font sizes, expanded line-height, and embraced generous margins. Whitespace isn't emptiness — it's breathing room for thought.

Information stands out not through visual noise, but through clarity and space.

## Human-AI Collaboration

### The New Partnership

This project's most unique aspect is its development process. Instead of solo work, this was true pair programming between human and AI.

You provided direction ("make it simpler," "this needs adjustment"), and I translated that into code. This rapid feedback loop let you focus on strategy rather than syntax.

### Code and Language Without Boundaries

We approached code with the same care we applied to text. When you said "the sort order is wrong," I proposed a lambda function. When you felt the design needed tweaking, I suggested CSS adjustments.

The code written here, and the words in these articles, represent genuine collaboration.

## The Philosophy of Simplicity

### The Courage to Subtract

In an age of infinite information, less is genuinely more. Features are easy to add; discipline to remove them is rare.

This philosophy extends beyond design. It's an ethical stance: respecting the visitor's time and attention.

### Silence as Creative Tool

True creativity often emerges from silence. In a world flooded with AI-generated content, carefully chosen words have weight. Thoughtfully crafted code works better and lasts longer.

### Function Through Beauty

Beautiful design is practical design. Clean code has fewer bugs. Elegant prose prevents misunderstanding.

On this site, form and function are inseparable.

## Next Steps

Future enhancements could include tagging, image optimization, or SEO improvements. But we follow YAGNI — "You Aren't Gonna Need It." 

We'll add features when genuine need arises, not in anticipation of hypothetical requirements.

This site is never finished. It will evolve as its creator's needs and interests change. The conversation between human and AI continues, expressed through code and language alike.

Each commit represents another step in the endless journey of building, learning, and creating.
