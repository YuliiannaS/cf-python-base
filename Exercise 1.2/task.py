recipe_1 = {
    "name": "Tea",
    "cooking_time_mins": 5,
    "ingredients": ["Tea leaves", "Sugar", "Water"]
}

all_recipes = []
all_recipes.append(recipe_1)

recipe_2 = {
    "name": "Coffee",
    "cooking_time": 10,
    "ingredients": ["Coffee beans", "Sugar", "Milk", "Water"]
}

recipe_3 = {
    "name": "Sandwich",
    "cooking_time": 5,
    "ingredients": ["Bread", "Cheese", "Ham", "Butter"]
}

recipe_4 = {
    "name": "Pasta",
    "cooking_time": 15,
    "ingredients": ["Pasta", "Tomato sauce", "Salt", "Olive oil", "Basil"]
}

recipe_5 = {
    "name": "Salad",
    "cooking_time": 7,
    "ingredients": ["Lettuce", "Tomato", "Cucumber", "Olive oil", "Salt"]
}

all_recipes.extend([recipe_2, recipe_3, recipe_4, recipe_5])

for i, recipe in enumerate(all_recipes, start=1):
    print(f"Ingredients of recipe_{i} ({recipe['name']}):")
    print(recipe['ingredients'])
    print()