recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients separated by commas: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe

n = int(input("How many recipes would you like to enter? "))
for _ in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    ingredients_count = len(recipe['ingredients'])
    cooking_time = recipe['cooking_time']
    
    if cooking_time < 10 and ingredients_count < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and ingredients_count >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and ingredients_count < 4:
        difficulty = 'Intermediate'
    else:
        difficulty = 'Hard'
    
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(f"- {ingredient}")
    print(f"Difficulty level: {difficulty}")
    print()

ingredients_list.sort()
print("Ingredients Available Across All Recipes")
print("-----------------------------------")
for ingredient in ingredients_list:
    print(ingredient)
