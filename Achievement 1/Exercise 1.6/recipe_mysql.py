import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='task_database'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"

def create_recipe(conn, cursor):
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter ingredients separated by commas: ").strip().split(',')
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ', '.join(ingredient.strip() for ingredient in ingredients)
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
    conn.commit()
    print("Recipe added successfully.")

def search_recipe(cursor):
    # Query to fetch all ingredients from the Recipes table
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    
    # Extract unique ingredients from the query results
    all_ingredients = set()
    for (ingredients,) in results:
        all_ingredients.update([ingredient.strip() for ingredient in ingredients.split(',')])

    # Display the ingredients as a numbered list
    sorted_ingredients = sorted(all_ingredients)
    print("Available Ingredients:")
    for index, ingredient in enumerate(sorted_ingredients, start=1):
        print(f"{index}. {ingredient}")

    # User selects an ingredient to search for
    try:
        choice = int(input("Enter the number of the ingredient to search for: ")) - 1
        search_ingredient = sorted_ingredients[choice]
    except (IndexError, ValueError):
        print("Invalid selection.")
        return

    # Perform search with the selected ingredient
    query = "SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s"
    search_pattern = f"%{search_ingredient}%"
    cursor.execute(query, (search_pattern,))
    matched_recipes = cursor.fetchall()

    # Display search results
    if matched_recipes:
        print(f"Recipes containing '{search_ingredient}':")
        for id, name, ingredients, cooking_time, difficulty in matched_recipes:
            print(f"ID: {id}, Name: {name}, Ingredients: {ingredients}, Cooking Time: {cooking_time} mins, Difficulty: {difficulty}")
    else:
        print("No recipes found containing that ingredient.")

def display_all_recipes(cursor):
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
    recipes = cursor.fetchall()
    if not recipes:
        print("No recipes found in the database.")
        return None

    print("Available Recipes:")
    for recipe in recipes:
        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} mins, Difficulty: {recipe[4]}")
    return recipes

def update_recipe(conn, cursor):
    recipes = display_all_recipes(cursor)
    if not recipes:
        return  # No recipes to update

    recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    print("Which column would you like to update?")
    print("1. Name")
    print("2. Cooking Time")
    print("3. Ingredients")
    column_choice = input("Choose 1, 2, or 3: ")

    if column_choice == '1':
        new_value = input("Enter the new name: ")
        column = "name"
    elif column_choice == '2':
        new_value = int(input("Enter the new cooking time: "))
        column = "cooking_time"
    elif column_choice == '3':
        new_value = input("Enter the new ingredients (comma-separated): ")
        column = "ingredients"
    else:
        print("Invalid choice.")
        return

    # Prepare and execute the update query
    update_query = f"UPDATE Recipes SET {column} = %s WHERE id = %s"
    cursor.execute(update_query, (new_value, recipe_id))

    # Recalculate difficulty if necessary
    if column in ['cooking_time', 'ingredients']:
        ingredients_query = "SELECT ingredients, cooking_time FROM Recipes WHERE id = %s"
        cursor.execute(ingredients_query, (recipe_id,))
        ingredients, cooking_time = cursor.fetchone()
        ingredients = ingredients.split(', ')
        difficulty = calculate_difficulty(cooking_time, ingredients)
        difficulty_update_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(difficulty_update_query, (difficulty, recipe_id))

    # Commit the changes
    conn.commit()
    print("Recipe updated successfully.")


def delete_recipe(conn, cursor):
    recipes = display_all_recipes(cursor)
    if not recipes:
        return  # No recipes to delete

    try:
        recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
        delete_query = "DELETE FROM Recipes WHERE id = %s"
        cursor.execute(delete_query, (recipe_id,))
        conn.commit()
        print("Recipe deleted successfully.")
    except ValueError:
        print("Invalid input; please enter a numerical ID.")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

def main_menu(conn):
    cursor = conn.cursor()
    while True:
        print("\nWhat would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit the program!")

        choice = input("Enter your choice (1-4) or 'quit' to exit: ")

        if choice == 'quit':
            print("Exiting the program.")
            break
        elif choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        else:
            print("Invalid choice. Please select a valid option.")
    
    cursor.close()
    conn.close()

conn = create_connection()
if conn is not None:
    main_menu(conn)
