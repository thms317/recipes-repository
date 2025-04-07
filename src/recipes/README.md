# MkDocs Recipe Plugin

A MkDocs plugin that transforms recipe markdown files to include HTML tables and images.

## Features

- Automatically converts recipe information sections into HTML tables
- Places images alongside recipe information
- Preserves original markdown for ingredients and instructions

## Installation

### Using uv (recommended)

```bash
make install-recipe-plugin
```

Or manually:

```bash
uv pip install -e .
```

### Using pip (alternative)

```bash
pip install -e .
```

## Development

For a complete development workflow:

```bash
# Clean environment, install plugin, run tests, and serve docs
make dev-recipe-plugin
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - recipes:
      recipes_dir: recipes
```

## Recipe Format

Your markdown recipes should follow this format:

```markdown
# Recipe Name

> *Recipe description*

## Recipe Information

- **Prep Time:** 10 minutes
- **Cook Time:** 25 minutes
- **Total Time:** 35 minutes
- **Servings:** 4 servings

## Ingredients

- Ingredient 1
- Ingredient 2

## Instructions

1. Step 1
2. Step 2
```

The plugin will convert the "Recipe Information" section to an HTML table and add an image of the dish.

## Configuration

- `recipes_dir`: Directory where recipe markdown files are located (default: `docs/recipes`)
- `images_dir`: Directory where recipe images are located (default: `docs/images`)

## Image Convention

Images should be named the same as the markdown file (with .jpg extension).
