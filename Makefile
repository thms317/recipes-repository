.PHONY: setup clean test tree docs recipe_db test-recipe-plugin install-recipe-plugin serve-docs dev-recipe-plugin lint

.DEFAULT_GOAL := setup


PROFILE_NAME := "DEFAULT"

setup:
	@echo "Setting up the project..."
	@uv sync;

	@if [ ! -d ".git" ]; then \
		echo "Setting up git..."; \
		git init -b main > /dev/null; \
	fi

	@echo "Setting up pre-commit..."
	@uv run pre-commit install --hook-type pre-commit --hook-type commit-msg

	@echo "Setup completed successfully!"

clean:
	@echo "Uninstalling local packages..."
	@rm -rf uv.lock
	@uv sync

	@echo -e "Cleaning up project artifacts..."
	@find . \( \
		-name ".pytest_cache" -o \
		-name ".mypy_cache" -o \
		-name ".ruff_cache" -o \
		-name "dist" -o \
		-name "__pycache__" -o \
		-name ".ipynb_checkpoints" \) \
		-type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".coverage" -type f -delete 2>/dev/null || true

	@echo "Cleanup completed."
	@reset

test:
	@echo "Running tests..."
	@uv build
	@uv sync
	@uv run pytest -v tests --cov=src --cov-report=term

tree:
	@echo "Generating project tree..."
	@tree -I '.venv|__pycache__|archive|scratch|.databricks|.ruff_cache|.mypy_cache|.pytest_cache|.git|htmlcov|site|dist|.DS_Store|fixtures' -a

recipe_db:
	@echo "Generating recipe database from markdown files..."
	@if [ ! -f "docs/database/recipes.db" ]; then \
		echo "Creating new recipe database..."; \
		uv run python -c "import sqlite3; conn = sqlite3.connect('docs/database/recipes.db'); conn.close()"; \
	fi
	@echo "Parsing recipe markdown files and populating database..."
	@PYTHONPATH=$(CURDIR) uv run python -c "from src.recipes_repository import populate_database; populate_database()"

docs: recipe_db
	@echo "Serving recipes..."
	@uv run mkdocs serve

test-recipe-plugin:
	@echo "Running recipe plugin tests..."
	@uv run pytest tests/test_recipe_plugin.py -v

serve-docs:
	@echo "Serving documentation with MkDocs..."
	@uv run mkdocs serve

dev-recipe-plugin: clean test-recipe-plugin serve-docs

lint:
	@echo "Linting the project..."
	@uv sync
	@echo "Building the project..."
	@uv build >/dev/null 2>&1
	@echo "Running ruff..."
	-@uv run ruff check --output-format=concise .
	@echo "Running mypy..."
	-@uv run mypy .
	@echo "Running pydoclint..."
	-@uv run pydoclint .
	@echo "Linting completed!"
