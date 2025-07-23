"""Recipes Repository package.

This package provides tools for:
1. Parsing markdown recipe files
2. Populating a database of recipes
3. Applying HTML styling to recipe markdown files via MkDocs plugin
"""

from recipes_repository.mkdocs_recipe_plugin import RecipePlugin
from recipes_repository.parse_recipes import RecipeDatabase, RecipeParser, populate_database

__all__ = [
    "RecipeDatabase",
    "RecipeParser",
    "RecipePlugin",
    "populate_database",
]
