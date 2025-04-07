"""Recipes package.

This package provides tools for:
1. Parsing markdown recipe files
2. Populating a database of recipes
3. Applying HTML styling to recipe markdown files via MkDocs plugin
"""

from recipes.parse_recipes import RecipeDatabase, RecipeParser, populate_database

__all__ = ["RecipeDatabase", "RecipeParser", "populate_database"]
