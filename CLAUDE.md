    # CLAUDE.md

    This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

    ## Development Commands

    This project uses Make for task automation and uv for Python package management.

    ### Setup and Installation
    - `make setup` - Install prerequisites and set up development environment (installs tools, syncs dependencies, sets up pre-commit hooks)
    - `make clean` - Remove virtual environment, lock files, and caches

    ### Testing and Quality
    - `make test` - Run all tests with coverage using pytest
    - `make lint` - Run all linting tools (ruff, mypy, pydoclint, bandit)
    - `uv run pytest tests/test_recipe_plugin.py -v` - Run specific plugin tests
    - `uv run pytest -v tests --cov=src --cov-report=term` - Run tests with coverage

    ### Documentation and Serving
    - `make docs` - Generate recipe database and serve documentation locally
    - `make serve-docs` - Install plugin and serve documentation with MkDocs
    - `PYTHONPATH=$(pwd) uv run mkdocs serve` - Serve docs directly

    ### Database Operations
    - `make recipe_db` - Generate SQLite database from markdown recipe files

    ## Architecture Overview

    This is a recipe documentation system that converts markdown recipe files into a beautiful HTML website using MkDocs.

    ### Core Components

    1. **Recipe Parser** (`src/recipes_repository/parse_recipes.py`): Parses markdown recipe files and populates a SQLite database
    2. **MkDocs Plugin** (`src/recipes_repository/mkdocs_recipe_plugin.py`): Custom MkDocs plugin that transforms recipe markdown into HTML tables with images
    3. **Recipe Database** (`docs/database/recipes.db`): SQLite database storing parsed recipe data
    4. **Documentation Site**: MkDocs-powered website with Material theme

    ### Project Structure

    - `docs/recipes/` - Organized recipe markdown files by category (breakfast, main, side, dessert, starter)
    - `docs/images/` - Recipe images organized by category
    - `src/recipes_repository/` - Python package containing parser and MkDocs plugin
    - `tests/` - Test files for the recipe plugin
    - `notebooks/` - Jupyter notebooks for database queries

    ### Key Features

    - Automatic recipe parsing from markdown to database
    - Custom MkDocs plugin for recipe formatting
    - Image integration with recipes
    - Categorized recipe organization
    - Semantic release workflow
    - Pre-commit hooks with comprehensive linting (ruff, mypy, pydoclint, bandit)

    ### Python Environment

    - Uses uv for dependency management
    - Python 3.12 required
    - Virtual environment in `.venv/`
    - Entry point for MkDocs plugin defined in pyproject.toml

    ### Quality Tools Configuration

    - **Ruff**: Line length 100, numpy docstring convention, extensive rule selection
    - **MyPy**: Strict type checking enabled
    - **Pytest**: Tests in `tests/` directory with coverage reporting
    - **Bandit**: Security linting for `src/` directory
    - **Pre-commit**: Automated on commit and commit message hooks
