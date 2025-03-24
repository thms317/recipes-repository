# Recipe Database

This page displays all recipes currently in the database, automatically extracted from the markdown files in the recipes directory.

## Recipe List

Each recipe is parsed from its markdown file and stored in a SQLite database. This allows us to:

1. Search recipes by ingredient, cooking time, or category
2. Filter recipes by language (English/Dutch)
3. Generate statistics about our recipe collection
4. Potentially build a recipe API in the future

## Available Recipes

The table below shows all recipes currently available in the database:

| Recipe Name | Language | Prep Time | Cook Time | Total Time |
|-------------|----------|-----------|-----------|------------|
| Banana-Peanut Butter Granola with Whole Nuts | English | 10 minutes | 25-30 minutes | 1 hour 30 minutes |
| Nederlandse Vegetarische Chili | Dutch | 15 minutes | 30-40 minutes | 55 minutes |

## Database Schema

The recipe database uses the following schema:

```
recipes
├── id (PRIMARY KEY)
├── title
├── description
├── file_path
├── language
├── prep_time
├── cook_time
├── total_time
├── servings
└── created_at

ingredients
├── id (PRIMARY KEY)
├── recipe_id (FOREIGN KEY -> recipes.id)
├── category
└── ingredient

instructions
├── id (PRIMARY KEY)
├── recipe_id (FOREIGN KEY -> recipes.id)
├── phase
├── step_number
└── instruction

storage_tips, serving_suggestions, recipe_notes
├── id (PRIMARY KEY)
├── recipe_id (FOREIGN KEY -> recipes.id)
└── text
```

## Using the Database

If you want to use the recipe database in Python, you can do so with the following code:

```python
import sqlite3

# Connect to the database
conn = sqlite3.connect('docs/database/recipes.db')
cursor = conn.cursor()

# Query all recipes
cursor.execute("SELECT title, language, prep_time, cook_time FROM recipes")
recipes = cursor.fetchall()

# Print recipes
for recipe in recipes:
    print(f"Recipe: {recipe[0]} ({recipe[1]})")
    print(f"Prep time: {recipe[2]}, Cook time: {recipe[3]}")
    print("---")

# Close the connection
conn.close()
```

This database is automatically regenerated each time the documentation is built, ensuring it always stays in sync with the markdown recipe files.
