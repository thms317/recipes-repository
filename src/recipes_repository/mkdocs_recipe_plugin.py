"""MkDocs plugin for recipes_repository.

Injects a Material grid-card info panel and schema.org Recipe JSON-LD into
pages that carry recipe frontmatter (``course`` is the marker).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from mkdocs.plugins import BasePlugin

if TYPE_CHECKING:
    from mkdocs.structure.pages import Page


class RecipePlugin(BasePlugin):  # type: ignore[type-arg]
    """Render recipe metadata from YAML frontmatter."""

    def on_page_markdown(self, markdown: str, page: Page, **_: Any) -> str:
        """Prepend info card and JSON-LD block to recipe pages."""
        meta: dict[str, Any] = dict(page.meta)
        if not meta.get("course"):
            return markdown
        return self._jsonld(page, meta) + self._card(meta) + markdown

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
