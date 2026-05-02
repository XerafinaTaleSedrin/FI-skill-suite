#!/usr/bin/env python3
"""Rogue Reads — static site generator.

Reads audits from ../book-audits/ (relative to the website folder).
Writes HTML to /website/.

Adapted from the Vera Wren / Basil Brightmoor build pattern.
"""

from __future__ import annotations

import json
import os
import re
import html
from datetime import datetime
from pathlib import Path

WEBSITE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = WEBSITE_ROOT.parent
AUDITS_SRC = REPO_ROOT / "book-audits"
OUTPUT_ROOT = WEBSITE_ROOT
TEMPLATE_PATH = WEBSITE_ROOT / "templates" / "base.html"
CONFIG_PATH = WEBSITE_ROOT / "config" / "site.json"


# ---------------------------------------------------------------------------
# Frontmatter + markdown parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML-ish frontmatter. Returns (meta_dict, body_str). Handles
    simple key: value lines plus list values starting with '-'."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    yaml_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")

    meta: dict = {}
    current_key: str | None = None
    for line in yaml_block.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key is not None:
            meta.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            current_key = key
            if val:
                meta[key] = val
            else:
                meta[key] = []
    return meta, body


def process_inline(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def markdown_to_html(md: str) -> str:
    """Lightweight markdown → HTML. Handles headers, lists, blockquotes,
    code blocks, paragraphs, tables, hr."""
    lines = md.split("\n")
    out: list[str] = []
    in_code = False
    in_list = False
    list_type: str | None = None
    in_quote = False
    quote_lines: list[str] = []
    in_table = False
    table_rows: list[list[str]] = []

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def close_quote():
        nonlocal in_quote, quote_lines
        if in_quote:
            content = " ".join(quote_lines)
            out.append(f"<blockquote><p>{process_inline(content)}</p></blockquote>")
            in_quote = False
            quote_lines = []

    def close_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            header = table_rows[0]
            body_rows = table_rows[2:] if len(table_rows) > 2 else []
            thead = "<tr>" + "".join(f"<th>{process_inline(c.strip())}</th>" for c in header) + "</tr>"
            tbody = "\n".join(
                "<tr>" + "".join(f"<td>{process_inline(c.strip())}</td>" for c in row) + "</tr>"
                for row in body_rows
            )
            out.append(f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>")
        in_table = False
        table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            close_list(); close_quote(); close_table()
            if not in_code:
                out.append("<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            out.append(html.escape(line))
            i += 1
            continue

        # Empty
        if not stripped:
            close_list(); close_quote(); close_table()
            i += 1
            continue

        # HR (--- or ___ etc., 3+)
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            close_list(); close_quote(); close_table()
            out.append("<hr>")
            i += 1
            continue

        # Headers
        m = re.match(r"^(#{1,6})\s+(.+)", stripped)
        if m:
            close_list(); close_quote(); close_table()
            level = len(m.group(1))
            out.append(f"<h{level}>{process_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Tables (rough — line starts with | and has at least one | inside)
        if stripped.startswith("|") and stripped.count("|") >= 2:
            close_list(); close_quote()
            cells = [c for c in stripped.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            close_table()

        # Blockquote
        if stripped.startswith(">"):
            close_list()
            content = stripped[1:].strip()
            if not in_quote:
                in_quote = True
                quote_lines = [content]
            else:
                quote_lines.append(content)
            i += 1
            continue

        # Unordered list
        ul = re.match(r"^[\-\*\+]\s+(.+)", stripped)
        if ul:
            close_quote()
            if not in_list or list_type != "ul":
                close_list()
                out.append("<ul>")
                in_list = True
                list_type = "ul"
            out.append(f"<li>{process_inline(ul.group(1))}</li>")
            i += 1
            continue

        # Ordered list
        ol = re.match(r"^\d+\.\s+(.+)", stripped)
        if ol:
            close_quote()
            if not in_list or list_type != "ol":
                close_list()
                out.append("<ol>")
                in_list = True
                list_type = "ol"
            out.append(f"<li>{process_inline(ol.group(1))}</li>")
            i += 1
            continue

        # Paragraph (gather consecutive non-special lines)
        close_list(); close_quote()
        para = [stripped]
        while i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if (not nxt or nxt.startswith("#") or nxt.startswith(">") or nxt.startswith("```")
                    or re.match(r"^[\-\*\+]\s+", nxt) or re.match(r"^\d+\.\s+", nxt)
                    or re.match(r"^(-{3,}|\*{3,}|_{3,})$", nxt) or nxt.startswith("|")):
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{process_inline(' '.join(para))}</p>")
        i += 1

    close_list(); close_quote(); close_table()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Audit-specific extraction
# ---------------------------------------------------------------------------

def extract_hearth_verdict(meta: dict, body_html: str) -> dict | None:
    """Pull Hearth's verdict tag from frontmatter. Returns dict with 'tag' or None."""
    tag = meta.get("hearth_verdict", "")
    if not tag:
        return None
    return {"tag": tag}


def load_audits() -> list[dict]:
    audits = []
    if not AUDITS_SRC.exists():
        return audits
    for path in sorted(AUDITS_SRC.glob("*.md")):
        if path.name.startswith("_"):
            continue  # skip _audit-template.md and other underscore-prefixed
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta.get("book"):
            continue
        slug = path.stem
        audits.append({
            "filename": path.name,
            "slug": slug,
            "book": meta.get("book", "Untitled"),
            "author": meta.get("author", ""),
            "published": meta.get("published", ""),
            "audited": meta.get("audited", ""),
            "auditor": meta.get("auditor", "Marika Olson"),
            "hearth_verdict": meta.get("hearth_verdict", ""),
            "status": meta.get("status", ""),
            "body_md": body,
            "body_html": markdown_to_html(body),
        })
    audits.sort(key=lambda a: a["audited"], reverse=True)
    return audits


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_page(template: str, config: dict, page_title: str, content: str,
                meta_description: str = "") -> str:
    return template.format(
        page_title=page_title,
        site_name=config["site_name"],
        tagline=config["tagline"],
        meta_description=meta_description or config["tagline"],
        base_url=config.get("base_url", ""),
        google_fonts_url=config.get("google_fonts_url", ""),
        content=content,
        footer_text=config.get("footer_text", ""),
        year=datetime.now().year,
    )


def render_audit_page(audit: dict, config: dict) -> str:
    base_url = config.get("base_url", "")
    verdict_html = ""
    if audit["hearth_verdict"]:
        verdict_html = (
            f'<div class="hearth-verdict">'
            f'<p><em>"Hearth naps through the book. Approves the tools from the windowsill."</em></p>'
            f'<span class="verdict-tag">{html.escape(audit["hearth_verdict"])}</span>'
            f'</div>'
        )
    content = f"""<article>
<header class="audit-header">
    <div class="audit-meta">{html.escape(audit['audited'])} &middot; Audit by {html.escape(audit['auditor'])}</div>
    <h1 class="audit-title">{html.escape(audit['book'])}</h1>
    <p class="audit-byline">{html.escape(audit['author'])} &middot; {html.escape(audit['published'])}</p>
</header>
<div class="audit-content">
{audit['body_html']}
</div>
</article>
"""
    return render_page(
        load_template(),
        config,
        audit["book"],
        content,
        meta_description=f"Rogue Reads audit of {audit['book']} by {audit['author']}.",
    )


def render_index(audits: list[dict], config: dict) -> str:
    base_url = config.get("base_url", "")
    if not audits:
        items_html = "<p>No audits yet. The first one is in the kiln.</p>"
    else:
        items = []
        for a in audits:
            verdict_chip = (
                f'<span class="audit-item-verdict">{html.escape(a["hearth_verdict"])}</span>'
                if a["hearth_verdict"] else ""
            )
            items.append(f"""<li class="audit-item">
    <div class="audit-item-meta">{html.escape(a['audited'])}</div>
    <h2 class="audit-item-title"><a href="{base_url}/audits/{a['slug']}.html">{html.escape(a['book'])}</a></h2>
    <p class="audit-item-author">{html.escape(a['author'])} &middot; {html.escape(a['published'])}</p>
    {verdict_chip}
</li>""")
        items_html = '<ul class="audit-list">' + "\n".join(items) + "</ul>"

    intro = """<section class="intro">
<p>Rogue Reads is the editorial-audit shelf where Marika Olson harvests the load-bearing mechanics from finance, business, and systems books — separated from their rhetorical packaging, with Hearth's verdict on whether the book is worth the time. Honest, blunt, and occasionally undiplomatic.</p>
</section>
<hr class="deco-divider">
"""
    return render_page(load_template(), config, "Audits", intro + items_html)


def render_about(config: dict) -> str:
    body = f"""<div class="about-content">
<h1>About Rogue Reads</h1>
<p>Rogue Reads is the book-audit shelf attached to <a href="{config.get("author_url", "https://marikaolson.com")}">Marika Olson Consulting</a>. Each audit takes one finance, business, or systems book and runs it through a fixed extraction format: strip the persona, surface the load-bearing mechanic, separate what aged well from what aged poorly, name what the book ignores, and give an honest verdict on who should read it.</p>

<p>Every audit closes with <strong>Hearth's verdict</strong> — a one-line read from the cat that lives on the desk. Tonal range: <em>nap-worthy</em>, <em>hiss-worthy</em>, <em>windowsill-approved</em>, <em>would-knock-off-the-desk</em>. Hearth has standards.</p>

<h2>What this isn't</h2>
<ul>
<li>Stock tips, market timing, or get-rich-quick patterns.</li>
<li>Affiliate-bait disguised as criticism. (Bookshop.org links may appear; revenue isn't the point.)</li>
<li>Sponsored content. Ever.</li>
</ul>

<h2>What this is</h2>
<ul>
<li>Editorial book audits, written by Marika Olson, in a single voice.</li>
<li>Closed to outside-author submissions — the voice integrity is the point. If you want to write audits, write them on your own platform; we'll happily link to good ones.</li>
<li>Free to read, forever. Content is licensed CC BY-NC-SA 4.0.</li>
</ul>

<h2>The skill suite</h2>
<p>The audit pipeline runs on the <a href="https://github.com/XerafinaTaleSedrin/FI-skill-suite">FI-skill-suite</a> — a free, open-source set of Claude Code skills for navigating financial independence. Anyone can clone the suite, run the audit skill against a book they've read, and produce their own audit on their own platform.</p>

<h2>Why "Rogue"</h2>
<p>Rogue Reads is part of the same editorial family as <a href="https://roguebureaucrat.com">Rogue Bureaucrat</a> — Marika's political-commentary shelf written under the Xerafina Tale'Sedrin pen name. <em>Rogue</em> is the family marker. It signals: refusing softness, naming things plainly, and bringing structural critique to spaces that prefer not to look at it.</p>

<p>Rogue Reads is published under Marika Olson by name. Rogue Bureaucrat is published pseudonymously. Different shelves, different voices, same sensibility.</p>
</div>
"""
    return render_page(load_template(), config, "About", body, "About Rogue Reads.")


# ---------------------------------------------------------------------------
# Build orchestration
# ---------------------------------------------------------------------------

_template_cache: str | None = None


def load_template() -> str:
    global _template_cache
    if _template_cache is None:
        _template_cache = TEMPLATE_PATH.read_text(encoding="utf-8")
    return _template_cache


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build():
    print(f"Building Rogue Reads from {WEBSITE_ROOT}")
    config = load_config()
    audits = load_audits()
    print(f"  Loaded {len(audits)} audit(s) from {AUDITS_SRC}")

    # Audit pages
    audit_dir = OUTPUT_ROOT / "audits"
    audit_dir.mkdir(exist_ok=True)
    for audit in audits:
        out = audit_dir / f"{audit['slug']}.html"
        write_file(out, render_audit_page(audit, config))
        print(f"  Wrote {out.relative_to(OUTPUT_ROOT)}")

    # Index
    write_file(OUTPUT_ROOT / "index.html", render_index(audits, config))
    print(f"  Wrote index.html")

    # About
    write_file(OUTPUT_ROOT / "about.html", render_about(config))
    print(f"  Wrote about.html")

    # GitHub Pages: needs a .nojekyll to skip Jekyll processing
    (OUTPUT_ROOT / ".nojekyll").touch()

    print("Build complete.")


if __name__ == "__main__":
    build()
