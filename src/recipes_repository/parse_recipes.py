"""Recipe markdown → SQLite builder.

Reads YAML frontmatter plus ingredient/instruction sections from each
recipe markdown file and writes a small relational SQLite database.

The database is an on-demand analytical artefact — it is *not* used by
the MkDocs build. Run it via the ``recipe-db`` CLI (see pyproject.toml).
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

import yaml

RECIPES_DIR = Path("docs/recipes")
DB_PATH = Path("docs/database/recipes.db")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_recipe(path: Path) -> dict[str, Any] | None:
    """Split a recipe markdown file into frontmatter and section data."""
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        return None
    body = match.group(2)
    return {
        "meta": meta,
        "ingredients": _extract_ingredients(body),
        "instructions": _extract_instructions(body),
    }


def _extract_section(body: str, heading: str) -> str:
    match = re.search(rf"## {heading}\b\s*(.*?)(?=\n## |\Z)", body, re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_ingredients(body: str) -> list[tuple[str, str]]:
    section = _extract_section(body, "Ingredients")
    if not section:
        return []
    items: list[tuple[str, str]] = []
    current = ""
    for line in section.splitlines():
        if line.startswith("### "):
            current = line.removeprefix("### ").strip()
            continue
        match = re.match(r"-\s*(?:\[\s*\]\s*)?(.+)", line)
        if match:
            items.append((current, match.group(1).strip()))
    return items


def _extract_instructions(body: str) -> list[tuple[str, int, str]]:
    section = _extract_section(body, "Instructions")
    if not section:
        return []
    steps: list[tuple[str, int, str]] = []
    current = ""
    step_num = 0
    for line in section.splitlines():
        if line.startswith("### "):
            current = line.removeprefix("### ").strip()
            step_num = 0
            continue
        match = re.match(r"(?:\d+\.|-)\s+(.+)", line)
        if match:
            step_num += 1
            steps.append((current, step_num, match.group(1).strip()))
    return steps


def create_schema(conn: sqlite3.Connection) -> None:
    """Create tables (idempotent)."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            image TEXT,
            course TEXT,
            cuisine TEXT,
            difficulty TEXT,
            prep_minutes INTEGER,
            cook_minutes INTEGER,
            servings TEXT,
            language TEXT
        );
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
            category TEXT,
            ingredient TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS instructions (
            id INTEGER PRIMARY KEY,
            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
            phase TEXT,
            step_number INTEGER NOT NULL,
            instruction TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tags (
            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
            tag TEXT NOT NULL,
            PRIMARY KEY (recipe_id, tag)
        );
    """)


def insert_recipe(conn: sqlite3.Connection, path: Path, parsed: dict[str, Any]) -> int:
    """Insert a parsed recipe and its ingredients/instructions/tags."""
    meta = parsed["meta"]
    cursor = conn.execute(
        """
        INSERT INTO recipes (
            file_path, title, description, image, course, cuisine,
            difficulty, prep_minutes, cook_minutes, servings, language
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(path),
            meta.get("title", path.stem),
            meta.get("description"),
            meta.get("image"),
            meta.get("course"),
            meta.get("cuisine"),
            meta.get("difficulty"),
            meta.get("prep_minutes"),
            meta.get("cook_minutes"),
            meta.get("servings"),
            meta.get("language"),
        ),
    )
    recipe_id = cursor.lastrowid
    if recipe_id is None:
        msg = f"Failed to insert recipe: {path}"
        raise RuntimeError(msg)

    conn.executemany(
        "INSERT INTO ingredients (recipe_id, category, ingredient) VALUES (?, ?, ?)",
        [(recipe_id, cat, ing) for cat, ing in parsed["ingredients"]],
    )
    conn.executemany(
        "INSERT INTO instructions (recipe_id, phase, step_number, instruction) VALUES (?, ?, ?, ?)",
        [(recipe_id, phase, n, text) for phase, n, text in parsed["instructions"]],
    )
    conn.executemany(
        "INSERT INTO tags (recipe_id, tag) VALUES (?, ?)",
        [(recipe_id, tag) for tag in meta.get("tags") or []],
    )
    return recipe_id


def populate_database() -> None:
    """Entry point: build `docs/database/recipes.db` from recipe frontmatter."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        create_schema(conn)
        for table in ("tags", "instructions", "ingredients", "recipes"):
            conn.execute(f"DELETE FROM {table}")
        count = 0
        for path in sorted(RECIPES_DIR.rglob("*.md")):
            parsed = parse_recipe(path)
            if parsed is None or not parsed["meta"].get("course"):
                continue
            insert_recipe(conn, path, parsed)
            count += 1
        conn.commit()
        print(f"Built {DB_PATH} with {count} recipes.")
    finally:
        conn.close()


if __name__ == "__main__":
    populate_database()
