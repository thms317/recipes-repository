import re
from pathlib import Path
from re import Match
from typing import Any, Dict, List, Optional, Tuple, cast

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class RecipePluginConfig(Config):
    """Configuration options for the RecipePlugin."""

    recipes_dir = config_options.Type(str, default="docs/recipes")
    images_dir = config_options.Type(str, default="docs/images")


class RecipePlugin(BasePlugin[RecipePluginConfig]):
    """
    MkDocs plugin that transforms recipe markdown files to include HTML tables and images.
    """

    # Override signature to match the BasePlugin's on_page_markdown method
    def on_page_markdown(  # type: ignore[override]
        self,
        markdown: str,
        page: Page,
        config: dict[str, Any],
        files: Files,
        **kwargs: Any,
    ) -> str:
        """Transform markdown for recipe pages."""
        # Debug
        print(f"Processing file: {page.file.src_path}")
        print(f"Config recipes_dir: {self.config.recipes_dir}")

        # Only process files in the recipes directory
        # Allow for both with and without the docs/ prefix
        file_path = page.file.src_path
        if not (
            file_path.startswith(self.config.recipes_dir)
            or file_path.startswith(f"docs/{self.config.recipes_dir}")
            or f"/{self.config.recipes_dir}/" in file_path
        ):
            print(f"Skipping {file_path} - not in recipes dir")
            return markdown

        # Skip files that are already in HTML format
        if "_html" in file_path:
            print(f"Skipping {file_path} - has _html suffix")
            return markdown

        # Extract recipe name from the first heading
        recipe_name_match: Match[str] | None = re.search(r"^# (.*?)$", markdown, re.MULTILINE)
        if not recipe_name_match:
            print(f"Skipping {file_path} - no recipe name found")
            return markdown

        recipe_name = recipe_name_match.group(1)
        print(f"Found recipe: {recipe_name}")

        # Create image path - assumes image has same name as markdown file
        image_filename = Path(file_path).stem + ".jpg"
        image_path = f"../images/{image_filename}"

        # Extract the recipe information section
        recipe_info_section_match = re.search(
            r"(## Recipe Information\s+)(.*?)(##)",
            markdown,
            re.DOTALL,
        )

        if not recipe_info_section_match:
            print(f"Skipping {file_path} - no recipe info section found")
            return markdown

        # Debug output
        print(f"Found recipe info section in {file_path}")

        # Get the content between "## Recipe Information" and the next "##" heading
        recipe_info_content = recipe_info_section_match.group(2).strip()
        original_section = recipe_info_section_match.group(1) + recipe_info_section_match.group(2)

        # Extract information items using a more flexible regex
        info_items: list[tuple[str, str]] = []
        print(f"Recipe info content: {recipe_info_content[:100]}...")

        # Use a more flexible pattern to match the list items
        pattern = r"- \*\*(.*?)\*\*:?\s*(.*?)(?:\r\n|\n|$)"
        matches = re.findall(pattern, recipe_info_content, re.MULTILINE)
        print(f"Found {len(matches)} matches with pattern: {pattern}")

        # Process each match and add it to info_items
        for key, value in matches:
            key = key.strip()
            # Remove any trailing colon from the key
            key = key.removesuffix(":")
            value = value.strip()
            if key and value:  # Ensure we have both key and value
                info_items.append((key, value))
                print(f"Found item: {key}: {value}")

        if not info_items:
            print(f"No valid info items found in {file_path}")
            # Dump the recipe info content for debugging
            print(f"Recipe info content:\n{recipe_info_content}")
            return markdown

        print(f"Found {len(info_items)} recipe info items: {info_items}")

        # Create HTML table
        table_html = '<div style="display: flex; flex-direction: row; align-items: center;">\n'
        table_html += '    <div style="flex: 1; display: flex; justify-content: center;">\n'
        table_html += "        <table>\n"
        table_html += "            <tr><th>Information</th><th>Details</th></tr>\n"

        for key, value in info_items:
            table_html += f"            <tr><td>{key}</td><td>{value}</td></tr>\n"

        table_html += "        </table>\n"
        table_html += "    </div>\n"
        table_html += '    <div style="flex: 1; padding-left: 20px; display: flex; justify-content: center;">\n'
        table_html += (
            f'        <img src="{image_path}" alt="{recipe_name}" style="max-width: 100%;">\n'
        )
        table_html += "    </div>\n"
        table_html += "</div>\n"

        print("Created HTML table")

        # Replace the original Recipe Information section with our HTML table
        next_section_start = recipe_info_section_match.start(3)
        transformed = (
            markdown[: recipe_info_section_match.start(0)]
            + recipe_info_section_match.group(1)  # Keep the "## Recipe Information" heading
            + table_html
            + markdown[
                next_section_start - 1 :
            ]  # Keep everything after, including the next "##" heading
        )

        print("Transformation complete")
        return transformed
