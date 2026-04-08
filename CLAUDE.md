# CLAUDE.md

## Project Overview

**iOSBlogCN** is a community-curated list of Chinese iOS/Mac development blogs. It is maintained as a simple GitHub repository with a Markdown table of blog entries and an auto-generated OPML file for RSS reader import.

- **Repository**: `tangqiaoboy/iOSBlogCN`
- **License**: GNU GPLv2
- **Primary language**: Chinese (content), English (filenames/code)

## Repository Structure

```
iOSBlogCN/
├── README.md        # Main content: blog list in Markdown table format
├── Export.py        # Python 3 script to generate OPML from README.md
├── blogcn.opml     # Auto-generated OPML subscription file (do not edit manually)
├── LICENSE          # GNU GPLv2
├── CLAUDE.md        # This file
└── .gitignore       # Ignores .idea/, __pycache__/
```

## Key Files

### README.md
The core of the project. Contains:
- Project description and contribution instructions (in Chinese)
- A Markdown table with columns: `博客地址 (Blog URL) | RSS地址 (RSS URL)`
- Each row follows the format: `[Blog Name](url) | <rss-feed-url>`
- Entries without RSS use `无` (meaning "none") instead of a URL

### Export.py
Python 3 script that parses README.md and generates `blogcn.opml`:
- Uses only stdlib (`os`, `re`) — no external dependencies
- Reads README.md, extracts blog entries via regex
- Outputs XML in OPML format for RSS reader import
- Run with: `python Export.py`
- **Must be run from the repository root directory** (uses `os.getcwd()`)

### blogcn.opml
Generated output file. **Do not edit manually** — regenerate by running `Export.py` after modifying README.md.

## Common Tasks

### Adding a new blog entry
1. Edit `README.md`
2. Add a new row to the table following the format: `[Blog Name](https://example.com) | <https://example.com/feed.xml>`
3. If no RSS feed exists, use `无` for the RSS column
4. Run `python Export.py` to regenerate `blogcn.opml`
5. Commit both `README.md` and `blogcn.opml` together

### Removing a blog entry
1. Delete the row from the Markdown table in `README.md`
2. Run `python Export.py` to regenerate `blogcn.opml`
3. Commit both files together

### Regenerating the OPML file
```bash
python Export.py
```

## Development Notes

- **No build system, CI/CD, tests, or linting** — this is a curated content repository
- **No external dependencies** — Export.py uses Python stdlib only
- **Python version**: Python 3 (uses `decode()`/`encode()` for UTF-8 handling)
- **Contributions**: Community members submit blog recommendations via [GitHub Issue #1](https://github.com/tangqiaoboy/iOSBlogCN/issues/1)

## Commit Message Conventions

Based on repository history, commit messages use these patterns:
- `ADD: description` — for new blog entries or features
- `DEL: description` — for removing entries
- `MOD: description` — for modifications/adjustments
- `FIX: description` — for fixes (often referencing issues, e.g., `fix #36`)
- Chinese descriptions are also common (e.g., `增加博客：Blog Name`)

## Important Conventions

- Always keep `README.md` and `blogcn.opml` in sync — run `Export.py` after any README change to the blog table
- Blog entries in `README.md` that lack RSS feeds (marked `无`) are skipped by `Export.py` since they don't match the `<...>` regex pattern
- The OPML file uses `\r\n` line endings for entry separators
- The primary branch is `master` (not `main`)
