import sqlite3

# Connect to the database
conn = sqlite3.connect("docs/database/recipes.db")
cursor = conn.cursor()

# Query all recipes
cursor.execute("SELECT title, language, prep_time, cook_time FROM recipes")
recipes = cursor.fetchall()
print(recipes)

# Print recipes
for recipe in recipes:
    print(f"Recipe: {recipe[0]} ({recipe[1]})")
    print(f"Prep time: {recipe[2]}, Cook time: {recipe[3]}")
    print("---")

# Close the connection
conn.close()
