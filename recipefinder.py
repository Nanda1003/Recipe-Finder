import requests
import json

class RecipeFinder:
    def __init__(self):
        self.api_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
        self.recipe_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="
        self.favorites_file = "favorites.json"

    def search_recipes(self, ingredients):
        print(f"\nSearching for recipes with: {', '.join(ingredients)}...\n")
        response = requests.get(self.api_url + ",".join(ingredients))
        
        if response.status_code == 200:
            data = response.json()
            recipes = data.get("meals", [])
            if recipes:
                for index, recipe in enumerate(recipes, 1):
                    print(f"{index}. {recipe['strMeal']}")
                return recipes
            else:
                print("No recipes found with these ingredients.")
        else:
            print("Error fetching data. Please try again.")
        return []

    def view_recipe_details(self, recipe_id):
        response = requests.get(self.recipe_url + recipe_id)
        if response.status_code == 200:
            data = response.json().get("meals", [])[0]
            print(f"\nRecipe: {data['strMeal']}")
            print(f"Category: {data['strCategory']}")
            print(f"Cuisine: {data['strArea']}")
            print(f"Instructions: {data['strInstructions']}")
            print(f"\nIngredients:")
            for i in range(1, 21):
                ingredient = data.get(f"strIngredient{i}")
                measure = data.get(f"strMeasure{i}")
                if ingredient and ingredient.strip():
                    print(f"- {ingredient}: {measure}")
            print(f"\nYou can watch a tutorial here: {data['strYoutube']}\n")
        else:
            print("Error fetching recipe details.")

    def save_to_favorites(self, recipe):
        try:
            with open(self.favorites_file, "r") as file:
                favorites = json.load(file)
        except FileNotFoundError:
            favorites = []

        favorites.append(recipe)
        with open(self.favorites_file, "w") as file:
            json.dump(favorites, file)
        print(f"Recipe '{recipe['strMeal']}' saved to favorites.")

    def view_favorites(self):
        try:
            with open(self.favorites_file, "r") as file:
                favorites = json.load(file)
                if favorites:
                    print("\nYour Favorite Recipes:")
                    for recipe in favorites:
                        print(f"- {recipe['strMeal']}")
                else:
                    print("No favorites found.")
        except FileNotFoundError:
            print("No favorites found.")

if __name__ == "__main__":
    recipe_finder = RecipeFinder()

    while True:
        print("\nOptions:")
        print("1. Search Recipes by Ingredients")
        print("2. View Favorite Recipes")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ingredients = input("Enter ingredients (comma-separated): ").strip().split(",")
            recipes = recipe_finder.search_recipes(ingredients)

            if recipes:
                try:
                    recipe_choice = int(input("\nEnter the number of the recipe to view details: ")) - 1
                    if 0 <= recipe_choice < len(recipes):
                        recipe_finder.view_recipe_details(recipes[recipe_choice]["idMeal"])
                        save_choice = input("Save this recipe to favorites? (yes/no): ").strip().lower()
                        if save_choice == "yes":
                            recipe_finder.save_to_favorites(recipes[recipe_choice])
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "2":
            recipe_finder.view_favorites()
        elif choice == "3":
            print("Exiting Recipe Finder. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
