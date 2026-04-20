"""Tests for the recipe plugin."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from mkdocs.config import load_config

from recipes_repository.mkdocs_recipe_plugin import RecipePlugin


@dataclass
class FakePage:
    """Minimal Page stub exposing only the attributes the plugin reads."""

    title: str = "Test Recipe"
    meta: dict[str, Any] = field(default_factory=dict)


def _render(meta: dict[str, Any], markdown: str = "# Body\n") -> str:
    plugin = RecipePlugin()
    page = FakePage(title="Test Recipe", meta=meta)
    return plugin.on_page_markdown(markdown, page)  # type: ignore[arg-type]


def test_skips_page_without_course() -> None:
    """Pages without recipe frontmatter are returned unchanged."""
    markdown = "# Regular Page\n\nNo recipe here.\n"
    assert _render({}, markdown) == markdown


def test_injects_grid_card_and_jsonld() -> None:
    """A full recipe emits both a grid card and a schema.org JSON-LD block."""
    meta = {
        "title": "Spaghetti Carbonara",
        "description": "Classic Italian pasta.",
        "image": "carbonara.png",
        "course": "main",
        "prep_minutes": 20,
        "cook_minutes": 15,
        "servings": "4 servings",
        "difficulty": "easy",
        "language": "en",
    }
    result = _render(meta)
    assert '<div class="grid cards" markdown>' in result
    assert "![Spaghetti Carbonara](images/carbonara.png)" in result
    assert "| Prep | 20 min |" in result
    assert "| Cook | 15 min |" in result
    assert "| Servings | 4 servings |" in result
    assert "| Difficulty | easy |" in result

    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', result, re.DOTALL)
    assert match is not None
    payload = json.loads(match.group(1))
    assert payload["@type"] == "Recipe"
    assert payload["name"] == "Spaghetti Carbonara"
    assert payload["prepTime"] == "PT20M"
    assert payload["cookTime"] == "PT15M"
    assert payload["recipeCategory"] == "main"
    assert payload["image"] == "images/carbonara.png"


def test_missing_timings_render_as_dash() -> None:
    """Absent minute values render as em-dashes in the info card."""
    meta = {"course": "dessert", "difficulty": "medium"}
    result = _render(meta)
    assert "| Prep | — |" in result
    assert "| Cook | — |" in result
    assert "| Servings | — |" in result


def test_mkdocs_config_registers_plugin() -> None:
    """mkdocs.yml registers the recipes plugin via the entry point."""
    config = load_config(config_file_path="mkdocs.yml")
    plugin_names = list(config["plugins"].keys())
    assert "recipes" in plugin_names
