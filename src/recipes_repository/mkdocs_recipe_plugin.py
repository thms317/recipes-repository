"""MkDocs plugin for recipes_repository.

Injects a Material grid-card info panel and schema.org Recipe JSON-LD into
pages that carry recipe frontmatter (``course`` is the marker), and groups
the Recipes nav section by that same ``course`` field.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.nav import Section

if TYPE_CHECKING:
    from mkdocs.structure.nav import Navigation
    from mkdocs.structure.pages import Page

log = get_plugin_logger(__name__)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
COURSE_TITLES: dict[str, str] = {
    "breakfast": "Breakfast",
    "starter": "Starters",
    "main": "Main Dishes",
    "side": "Side Dishes",
    "dessert": "Desserts",
    "cocktail": "Cocktails",
}


def _extract_course(abs_src_path: str | None) -> str | None:
    if not abs_src_path:
        return None
    try:
        text = Path(abs_src_path).read_text(encoding="utf-8")
    except OSError:
        return None
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    meta = yaml.safe_load(match.group(1)) or {}
    return meta.get("course") if isinstance(meta, dict) else None


class RecipePlugin(BasePlugin):  # type: ignore[type-arg]
    """Render recipe metadata from YAML frontmatter."""

    def on_page_markdown(self, markdown: str, page: Page, **_: Any) -> str:
        """Prepend info card and JSON-LD block to recipe pages."""
        meta: dict[str, Any] = dict(page.meta)
        if not meta.get("course"):
            return markdown
        if not meta.get("image"):
            log.warning("Recipe %s is missing an image.", page.file.src_path)
        return self._jsonld(page, meta) + self._card(meta) + markdown

    def on_nav(self, nav: Navigation, **_: Any) -> Navigation:
        """Group the Recipes section by `course` frontmatter."""
        section = next(
            (item for item in nav.items if getattr(item, "title", None) == "Recipes"),
            None,
        )
        if section is None or not hasattr(section, "children"):
            return nav
        buckets: dict[str, list[Any]] = {c: [] for c in COURSE_TITLES}
        for child in list(section.children):
            course = _extract_course(getattr(getattr(child, "file", None), "abs_src_path", None))
            if course in buckets:
                buckets[course].append(child)
        new_children: list[Any] = []
        for course, title in COURSE_TITLES.items():
            pages = sorted(buckets[course], key=lambda c: c.file.src_path)
            if not pages:
                continue
            group = Section(title=title, children=pages)
            for p in pages:
                p.parent = group
            group.parent = section
            new_children.append(group)
        section.children = new_children
        return nav

    @staticmethod
    def _fmt(value: Any, suffix: str = "") -> str:
        return f"{value}{suffix}" if value not in (None, "", []) else "—"

    def _card(self, m: dict[str, Any]) -> str:
        image = m.get("image", "")
        image_md = f"![{m.get('title', '')}](images/{image})" if image else ""
        rows = [
            ("Prep", self._fmt(m.get("prep_minutes"), " min")),
            ("Cook", self._fmt(m.get("cook_minutes"), " min")),
            ("Servings", self._fmt(m.get("servings"))),
            ("Difficulty", self._fmt(m.get("difficulty"))),
        ]
        table = "\n".join(f"    | {k} | {v} |" for k, v in rows)
        header = "    |   |   |\n    |---|---|"
        return (
            '<div class="grid cards" markdown>\n\n'
            f"-   {image_md}\n\n"
            f"-   {header[4:]}\n{table}\n\n"
            "</div>\n\n"
        )

    def _jsonld(self, page: Page, m: dict[str, Any]) -> str:
        data: dict[str, Any] = {
            "@context": "https://schema.org",
            "@type": "Recipe",
            "name": m.get("title") or page.title,
            "description": m.get("description"),
            "image": f"images/{m['image']}" if m.get("image") else None,
            "recipeCategory": m.get("course"),
            "recipeCuisine": m.get("cuisine"),
            "prepTime": f"PT{m['prep_minutes']}M" if m.get("prep_minutes") else None,
            "cookTime": f"PT{m['cook_minutes']}M" if m.get("cook_minutes") else None,
            "recipeYield": m.get("servings"),
            "inLanguage": m.get("language"),
            "keywords": ", ".join(m["tags"]) if m.get("tags") else None,
        }
        clean = {k: v for k, v in data.items() if v}
        payload = json.dumps(clean, ensure_ascii=False)
        return f'<script type="application/ld+json">{payload}</script>\n\n'
