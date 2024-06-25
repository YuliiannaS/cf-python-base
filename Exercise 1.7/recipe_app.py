from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('mysql+mysqlconnector://root:root@localhost/task_database')
Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"

    def __str__(self):
        return (f"Recipe ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Ingredients: {self.ingredients}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Difficulty: {self.difficulty}\n"
                f"{'-'*40}")

    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if self.ingredients:
            return self.ingredients.split(', ')
        return []
    
Base.metadata.create_all(engine)

def create_recipe(session):
    name = input("Enter the recipe name (max 50 chars): ")
    if len(name) > 50 or not name.isalpha():
        print("Invalid name. Please ensure it is alphanumeric and up to 50 characters long.")
        return

    num_ingredients = int(input("How many ingredients? "))
    ingredients = []
    for _ in range(num_ingredients):
        ingredient = input("Enter an ingredient: ")
        ingredients.append(ingredient)
    ingredients_str = ', '.join(ingredients)

    cooking_time = input("Enter cooking time in minutes: ")
    if not cooking_time.isnumeric():
        print("Invalid cooking time. Please enter a number.")
        return
    cooking_time = int(cooking_time)

    recipe_entry = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time, difficulty='Unknown')
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("Recipe created successfully!")

def view_all_recipes(session):
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no entries in your database.")
        return None
    for recipe in recipes:
        print(recipe.__str__())

def search_by_ingredients(session):
    count = session.query(Recipe).count()
    if count == 0:
        print("No entries in the database.")
        return

    results = session.query(Recipe.ingredients).all()
    all_ingredients = set()
    for (ingredients,) in results:
        all_ingredients.update(ingredients.split(', '))

    for idx, ingredient in enumerate(sorted(all_ingredients)):
        print(f"{idx + 1}. {ingredient}")

    selected_numbers = input("Select ingredients by number (separated by space): ")
    selected_indices = [int(num) - 1 for num in selected_numbers.split()]

    search_ingredients = [list(sorted(all_ingredients))[index] for index in selected_indices]
    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    recipes = session.query(Recipe).filter(*conditions).all()
    for recipe in recipes:
        print(recipe.__str__())

def edit_recipe(session):
    results = session.query(Recipe.id, Recipe.name).all()
    if not results:
        print("No recipes available.")
        return

    for result in results:
        print(f"ID: {result.id}, Name: {result.name}")

    recipe_id = int(input("Enter the ID of the recipe you want to edit: "))
    recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()

    print(f"1. Name: {recipe_to_edit.name}\n2. Ingredients: {recipe_to_edit.ingredients}\n3. Cooking Time: {recipe_to_edit.cooking_time}")
    choice = int(input("Which attribute to edit (1-3): "))
    if choice == 1:
        new_name = input("Enter new name: ")
        recipe_to_edit.name = new_name
    elif choice == 2:
        new_ingredients = input("Enter new ingredients (comma-separated): ")
        recipe_to_edit.ingredients = new_ingredients
    elif choice == 3:
        new_time = int(input("Enter new cooking time: "))
        recipe_to_edit.cooking_time = new_time

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")

def delete_recipe(session):
    results = session.query(Recipe.id, Recipe.name).all()
    if not results:
        print("No recipes available.")
        return

    for result in results:
        print(f"ID: {result.id}, Name: {result.name}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))
    recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()

    confirmation = input("Are you sure you want to delete this recipe? (yes/no): ")
    if confirmation.lower() == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully.")

def main_menu(session):
    while True:
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to quit the application.")

        choice = input("Enter your choice or 'quit' to exit: ")

        if choice == 'quit':
            print("Exiting the application.")
            break
        elif choice == '1':
            create_recipe(session)
        elif choice == '2':
            view_all_recipes(session)
        elif choice == '3':
            search_by_ingredients(session)
        elif choice == '4':
            edit_recipe(session)
        elif choice == '5':
            delete_recipe(session)
        else:
            print("Invalid input. Please try again.")

    session.close()

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    main_menu(session)
    session.close()