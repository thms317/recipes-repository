"""Recipes Repository package.

Provides:
- ``RecipePlugin``: MkDocs plugin that renders recipes from YAML frontmatter.
- ``populate_database``: CLI helper that builds an on-demand SQLite database.
"""

from recipes_repository.mkdocs_recipe_plugin import RecipePlugin
from recipes_repository.parse_recipes import populate_database

__all__ = ["RecipePlugin", "populate_database"]
