#!/usr/bin/env python

"""
Recipe Markdown Parser and Formatter.

This module:
1. Parses markdown recipe files
2. Populates a SQLite database with structured data
3. Provides a markdown preprocessing extension that applies HTML styling

Usage:
- As a standalone script to populate the database
- As a MkDocs extension for formatting
"""

import os
import re
import sqlite3
from pathlib import Path
from typing import Any


class RecipeParser:
    """Parser for recipe markdown files."""

    def __init__(self, file_path: str):
        """Initialize with the path to a markdown recipe file."""
        self.file_path = file_path
        with open(file_path, encoding="utf-8") as f:
            self.content = f.read()

        self.recipe_data: dict[str, Any] = {
            "title": "",
            "description": "",
            "info": {},
            "ingredients": {},
            "instructions": {},
            "storage_tips": [],
            "serving_suggestions": [],
            "recipe_notes": [],
        }
        self.parse()

    def parse(self) -> None:
        """Parse the markdown content into structured data."""
        # Extract title (H1)
        title_match = re.search(r"^# (.+)$", self.content, re.MULTILINE)
        if title_match:
            self.recipe_data["title"] = title_match.group(1).strip()

        # Extract description (italicized text after title)
        desc_match = re.search(r"^# .+\n\n\*(.+)\*", self.content, re.MULTILINE | re.DOTALL)
        if desc_match:
            self.recipe_data["description"] = desc_match.group(1).strip()

        # Extract recipe information
        info_section = self._extract_section(
            r"## Recipe Information\n(.*?)(?:\n##|\Z)",
            self.content,
        )
        if info_section:
            info_lines = re.findall(r"- \*\*(.+?):\*\* (.+)", info_section)
            self.recipe_data["info"] = {
                key.lower().replace(" ", "_"): value for key, value in info_lines
            }

        # Extract ingredients
        ingredients_section = self._extract_section(
            r"## Ingredients\n(.*?)(?:\n##|\Z)",
            self.content,
        )
        if ingredients_section:
            # Find all ingredient categories (### headers)
            categories = re.findall(r"### (.+)\n(.*?)(?=\n###|\Z)", ingredients_section, re.DOTALL)
            for category, items in categories:
                ingredient_items = re.findall(r"- (.+)", items)
                self.recipe_data["ingredients"][category.strip()] = [
                    item.strip() for item in ingredient_items
                ]

        # Extract instructions
        instructions_section = self._extract_section(
            r"## Instructions\n(.*?)(?:\n##|\Z)",
            self.content,
        )
        if instructions_section:
            # Find all instruction phases (### headers)
            phases = re.findall(r"### (.+)\n(.*?)(?=\n###|\Z)", instructions_section, re.DOTALL)
            for phase, items in phases:
                step_items = re.findall(r"\d+\.\s+(.+)", items)
                self.recipe_data["instructions"][phase.strip()] = [
                    item.strip() for item in step_items
                ]

        # Extract storage tips
        storage_section = self._extract_section(r"## Storage Tips\n(.*?)(?:\n##|\Z)", self.content)
        if storage_section:
            self.recipe_data["storage_tips"] = [
                item.strip() for item in re.findall(r"- (.+)", storage_section)
            ]

        # Extract serving suggestions
        serving_section = self._extract_section(
            r"## Serving Suggestions\n(.*?)(?:\n##|\Z)",
            self.content,
        )
        if serving_section:
            self.recipe_data["serving_suggestions"] = [
                item.strip() for item in re.findall(r"- (.+)", serving_section)
            ]

        # Extract recipe notes
        notes_section = self._extract_section(r"## Recipe Notes\n(.*?)(?:\n##|\Z)", self.content)
        if notes_section:
            self.recipe_data["recipe_notes"] = [
                item.strip() for item in re.findall(r"- (.+)", notes_section)
            ]

    def _extract_section(self, pattern: str, text: str) -> str | None:
        """Extract a section of text using a regex pattern."""
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    def get_data(self) -> dict[str, Any]:
        """Return the parsed recipe data."""
        return self.recipe_data

    def get_formatted_markdown(self) -> str:
        """Convert the clean markdown to styled markdown with HTML elements."""
        formatted_md = []

        # Add title
        formatted_md.append(f"# {self.recipe_data['title']}\n")

        # Add description (blockquote)
        formatted_md.append(f"> *{self.recipe_data['description']}*\n")

        # Add info table and image container
        formatted_md.append(
            '<div style="display: flex; flex-direction: row; align-items: center;">',
        )
        formatted_md.append('    <div style="flex: 1; display: flex; justify-content: center;">')
        formatted_md.append("        <table>")
        formatted_md.append("            <tr><th>Information</th><th>Details</th></tr>")

        # Map internal field names to display names
        field_display_names = {
            "prep_time": "Prep Time",
            "cook_time": "Cook Time",
            "cooling_time": "Cooling Time",
            "total_time": "Total Time",
            "servings": "Servings",
        }

        # Add table rows
        for field, display_name in field_display_names.items():
            if field in self.recipe_data["info"]:
                formatted_md.append(
                    f"            <tr><td>{display_name}</td><td>{self.recipe_data['info'][field]}</td></tr>",
                )

        formatted_md.append("        </table>")
        formatted_md.append("    </div>")

        # Extract image name from file path to determine image path
        image_name = os.path.splitext(os.path.basename(self.file_path))[0]

        # Add image container
        formatted_md.append(
            '    <div style="flex: 1; padding-left: 20px; display: flex; justify-content: center;">',
        )
        formatted_md.append(
            f'        <img src="../images/{image_name}.jpg" alt="{self.recipe_data["title"]}" style="max-width: 100%;">',
        )
        formatted_md.append("    </div>")
        formatted_md.append("</div>\n")

        # Add section separator
        formatted_md.append("---\n")

        # Add ingredients section
        formatted_md.append("## Ingredients\n")
        for category, ingredients in self.recipe_data["ingredients"].items():
            formatted_md.append(f"### {category}")
            for ingredient in ingredients:
                formatted_md.append(f"- {ingredient}")
            formatted_md.append("")

        # Add section separator
        formatted_md.append("---\n")

        # Add instructions section
        formatted_md.append("## Instructions\n")
        step_counter = 1
        for phase, steps in self.recipe_data["instructions"].items():
            formatted_md.append(f"### {phase}")
            for step in steps:
                # Bold the first word of each instruction
                first_word_end = step.find(" ")
                if first_word_end > 0:
                    bolded_step = f"**{step[:first_word_end]}** {step[first_word_end + 1 :]}"
                else:
                    bolded_step = step

                formatted_md.append(f"{step_counter}. {bolded_step}")
                step_counter += 1
            formatted_md.append("")

        # Add section separator and additional sections if they exist
        for section_title, items in [
            ("Storage Tips", self.recipe_data["storage_tips"]),
            ("Serving Suggestions", self.recipe_data["serving_suggestions"]),
            ("Recipe Notes", self.recipe_data["recipe_notes"]),
        ]:
            if items:
                formatted_md.append("---\n")
                formatted_md.append(f"## {section_title}\n")
                for item in items:
                    formatted_md.append(f"- {item}")
                formatted_md.append("")

        # Add final separator and footer
        formatted_md.append("---\n")
        formatted_md.append("*Recipe formatted with automatic styling*")

        return "\n".join(formatted_md)


class RecipeDatabase:
    """Database handler for recipes."""

    def __init__(self, db_path: str):
        """Initialize with the path to the SQLite database."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the necessary database tables if they don't exist."""
        # Main recipe table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            file_path TEXT NOT NULL,
            language TEXT,
            prep_time TEXT,
            cook_time TEXT,
            total_time TEXT,
            servings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Ingredients table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            recipe_id INTEGER,
            category TEXT,
            ingredient TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
        )
        """)

        # Instructions table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructions (
            id INTEGER PRIMARY KEY,
            recipe_id INTEGER,
            phase TEXT,
            step_number INTEGER,
            instruction TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
        )
        """)

        # Tips and notes tables
        for table in ["storage_tips", "serving_suggestions", "recipe_notes"]:
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                recipe_id INTEGER,
                text TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
            )
            """)

        self.conn.commit()

    def clear_all_data(self) -> None:
        """Clear all data from all tables."""
        tables = [
            "recipe_notes",
            "serving_suggestions",
            "storage_tips",
            "instructions",
            "ingredients",
            "recipes",
        ]
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()

    def add_recipe(self, recipe_data: dict[str, Any], file_path: str) -> int:
        """Add a recipe to the database and return its ID."""
        # Determine language by checking for Dutch keywords in the title or description
        language = (
            "nl"
            if any(
                dutch_word in recipe_data["title"].lower()
                for dutch_word in ["nederlandse", "hollandse", "recept"]
            )
            else "en"
        )

        # Insert main recipe info
        self.cursor.execute(
            """
        INSERT INTO recipes (title, description, file_path, language, prep_time, cook_time, total_time, servings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                recipe_data["title"],
                recipe_data["description"],
                file_path,
                language,
                recipe_data["info"].get("prep_time", ""),
                recipe_data["info"].get("cook_time", ""),
                recipe_data["info"].get("total_time", ""),
                recipe_data["info"].get("servings", ""),
            ),
        )

        recipe_id = self.cursor.lastrowid
        if recipe_id is None:
            raise ValueError("Failed to get recipe ID after insertion")

        # Insert ingredients
        for category, ingredients in recipe_data["ingredients"].items():
            for ingredient in ingredients:
                self.cursor.execute(
                    """
                INSERT INTO ingredients (recipe_id, category, ingredient)
                VALUES (?, ?, ?)
                """,
                    (recipe_id, category, ingredient),
                )

        # Insert instructions
        for phase, steps in recipe_data["instructions"].items():
            for step_num, instruction in enumerate(steps, 1):
                self.cursor.execute(
                    """
                INSERT INTO instructions (recipe_id, phase, step_number, instruction)
                VALUES (?, ?, ?, ?)
                """,
                    (recipe_id, phase, step_num, instruction),
                )

        # Insert tips and notes
        for field in ["storage_tips", "serving_suggestions", "recipe_notes"]:
            for item in recipe_data.get(field, []):
                self.cursor.execute(
                    f"""
                INSERT INTO {field} (recipe_id, text)
                VALUES (?, ?)
                """,
                    (recipe_id, item),
                )

        self.conn.commit()
        return recipe_id

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


# MkDocs extension for recipe formatting
class RecipePreprocessor:
    """Preprocessor for MkDocs that converts clean markdown recipes to styled ones."""

    def __init__(self, recipes_dir: str = "docs/recipes"):
        self.recipes_dir = recipes_dir

    def on_page_markdown(
        self,
        markdown_content: str,
        page: Any,
        config: dict[str, Any],
        **kwargs: Any,
    ) -> str:
        """MkDocs hook to process the markdown content before rendering."""
        # Check if this is a recipe page (in recipes directory)
        if not page.file.src_path.startswith("recipes/") or not page.file.src_path.endswith(".md"):
            return markdown_content

        # If this is 'granola copy.md', leave it untouched as requested
        if page.file.src_path == "recipes/granola copy.md":
            return markdown_content

        try:
            # Parse the recipe file
            file_path = os.path.join(config["docs_dir"], page.file.src_path)
            parser = RecipeParser(file_path)

            # Return the HTML-enhanced markdown
            return parser.get_formatted_markdown()
        except Exception as e:
            print(f"Error processing recipe {page.file.src_path}: {e}")
            return markdown_content


# Function to create a MkDocs extension
def makeExtension(*args: Any, **kwargs: Any) -> RecipePreprocessor:
    """Create a MkDocs extension."""
    return RecipePreprocessor(*args, **kwargs)


def populate_database() -> None:
    """Populate the recipe database from markdown files."""
    print("Starting recipe parser...")

    # Setup paths
    recipes_dir = Path("docs/recipes")
    db_path = Path("docs/database/recipes.db")
    db_path.parent.mkdir(exist_ok=True, parents=True)

    # Initialize database
    db = RecipeDatabase(str(db_path))

    # Clear existing data
    db.clear_all_data()

    # Process all markdown files in the recipes directory
    recipe_files = list(recipes_dir.glob("*.md"))
    print(f"Found {len(recipe_files)} recipe files")

    for file_path in recipe_files:
        # Skip the 'granola copy.md' as requested
        if file_path.name == "granola copy.md":
            continue

        print(f"Processing {file_path}...")
        try:
            parser = RecipeParser(str(file_path))
            recipe_data = parser.get_data()
            recipe_id = db.add_recipe(recipe_data, str(file_path))
            print(f"Added recipe ID {recipe_id}: {recipe_data['title']}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    db.close()
    print("Recipe database generation complete!")


if __name__ == "__main__":
    populate_database()
