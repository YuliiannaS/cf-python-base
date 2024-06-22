import pickle

def take_recipe():
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter ingredients separated by a comma: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    return {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}

def calc_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"

filename = input("Enter the filename to open: ")
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {'recipes_list': [], 'all_ingredients': []}
except Exception:
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    file.close()

recipes_list, all_ingredients = data['recipes_list'], data['all_ingredients']

num_recipes = int(input("How many recipes would you like to enter? "))
for _ in range(num_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

with open(filename, 'wb') as file:
    pickle.dump(data, file)