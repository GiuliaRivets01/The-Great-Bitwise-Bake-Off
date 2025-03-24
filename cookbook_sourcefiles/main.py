import json
import os

from ga_implementation import *


def load_recipes(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def create_recipe():
    # Load inspirational dataset
    json_file_path = 'inspiration/Dessert_recipes.json'
    recipes = load_recipes(json_file_path)

    # Extract all the ingredients, so we can apply the mutation
    all_ingredients = []
    for recipe in recipes['recipes']:
        all_ingredients.extend(recipe['ingredients'])

    # Creating an initial population
    population_size = 20
    population = random.choices(recipes['recipes'], k=population_size)

    # Evaluating recipes (fitness function)
    evaluate_recipes(population)
    population = sorted(population, reverse=True, key=lambda r: r['fitness'])

    # Create a new recipes
    for i in range(5):
        R = generate_recipes(population_size, population, all_ingredients)
        population = select_population(population, R)

    # Directions for the recipe
    gen_recipe = generate_directions(R[0]['ingredients'])
    print(gen_recipe)
    return gen_recipe


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create output directory
    cook_book_directory = 'cookbook'
    if not os.path.exists(cook_book_directory):
        os.makedirs(cook_book_directory)

    # Save recipes in cookbook directory
    num_recipes = 3
    for i in range(num_recipes):
        recipe_content = create_recipe()
        recipe_filename = os.path.join(cook_book_directory, f'recipe{i + 1}.txt')
        with open(recipe_filename, 'w') as f:
            f.write(recipe_content)

print("Recipe book successfully generated")
