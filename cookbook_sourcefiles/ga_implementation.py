import random
import math


# Fitness function
def evaluate_recipes(recipes):
    for recipe in recipes:
        proteins_weight = 1  # Weight for proteins
        calories_weight = 0.1  # Weight for calories
        fat_weight = 0.5  # Weight for fat
        cost_weight = 0.2  # Weight for ingredient cost
        nutritional_weight = 0.8  # Weight for nutritional value
        no_ingredients_weight = 20  # Weight for time proportion (larger number of ingredients more time )

        total_proteins = sum(float(ingredient.get('proteins', 0)) for ingredient in recipe['ingredients'])
        total_calories = sum(float(ingredient.get('calories', 0)) for ingredient in recipe['ingredients'])
        total_fat = sum(float(ingredient.get('fat', 0)) for ingredient in recipe['ingredients'])
        total_cost = sum(float(ingredient.get('cost', 0)) for ingredient in recipe['ingredients'])

        if total_cost == 0:
            nutritional_value = 0
        else:
            nutritional_value = float(total_calories / total_cost)

        no_ingredients = len(recipe['ingredients'])

        # Fitness calculation
        recipe['fitness'] = int(
            proteins_weight * total_proteins +
            calories_weight * total_calories +
            fat_weight * total_fat +
            cost_weight * total_cost +
            nutritional_value * nutritional_weight -
            no_ingredients * no_ingredients_weight
        )


# Selecting recipes using Roulette Wheel
def select_recipe(recipes):
    sum_fitness = sum([recipe['fitness'] for recipe in recipes])
    f = random.randint(0, sum_fitness)
    for recipe in recipes:
        if f < recipe['fitness']:
            return recipe
        f -= recipe['fitness']
    return recipes[-1]


# Crossover function
recipe_number = 1
def crossover_recipes(r1, r2):
    global recipe_number

    # Handle the case where one of the recipes has only one ingredient
    if len(r1['ingredients']) <= 1 or len(r2['ingredients']) <= 1:
        return r1.copy() if len(r1['ingredients']) > 1 else r2.copy()

    p1 = random.randint(1, len(r1['ingredients']) - 1)
    p2 = random.randint(1, len(r2['ingredients']) - 1)
    r1a = r1['ingredients'][0:p1]
    r2b = r2['ingredients'][p2:-1]
    r = dict()
    r['name'] = "recipe {}".format(recipe_number)
    recipe_number += 1
    r['ingredients'] = r1a + r2b
    return r


# Mutate function
def mutate_recipe(r, all_ingredients):
    m = random.randint(0, 3)
    if m == 0:
        i = random.randint(0, len(r['ingredients']) - 1)
        r['ingredients'][i] = r['ingredients'][i].copy()
        if "/" in str(r['ingredients'][i]['amount']):
            temp = r['ingredients'][i]['amount'].split("/")
            r['ingredients'][i]['amount'] = int(temp[0]) / int(temp[1])
        r['ingredients'][i]['amount'] = int(r['ingredients'][i]['amount'])
        r['ingredients'][i]['amount'] += math.floor(r['ingredients'][i]['amount'] * 0.1)
        r['ingredients'][i]['amount'] = max(1, r['ingredients'][i]['amount'])
    elif m == 1:
        j = random.randint(0, len(r['ingredients']) - 1)
        r['ingredients'][j] = r['ingredients'][j].copy()
        r['ingredients'][j]['ingredient'] = random.choice(all_ingredients)['ingredient']
    elif m == 2:
        r['ingredients'].append(random.choice(all_ingredients).copy())
    else:
        if len(r['ingredients']) > 1:
            r['ingredients'].remove(random.choice(r['ingredients']))


# generate recipes
def generate_recipes(size, population, all_ingredients):
    R = []
    while len(R) < size:
        r1 = select_recipe(population)
        r2 = select_recipe(population)
        r = crossover_recipes(r1, r2)
        mutate_recipe(r, all_ingredients)
        # normalise_recipe(r)
        R.append(r)
    evaluate_recipes(R)
    return R


# Select a new population
def select_population(P, R):
    R = sorted(R, reverse=True, key=lambda r: r['fitness'])
    P = P[0:len(P) // 2] + R[0:len(R) // 2]
    P = sorted(P, reverse=True, key=lambda r: r['fitness'])
    return P


# Generate the directions for the recipe given its ingredients
def generate_directions(ingredients_and_qty):
    dry_ingr = []
    wet_ingr = []
    for elem in ingredients_and_qty:
        if elem['unit'] == 'g':
            dry_ingr.append(elem['ingredient'])
        else:
            wet_ingr.append(elem['ingredient'])
    temp = ['180', '190', '200']
    time = ['30', '35', '40']
    time_refrig = ['1', '2', '3']

    template_0 = "Preheat the oven at " + random.choice(temp) + " degrees."
    template_1 = "Mix together {dry_ingredients} in a bowl."
    template_2 = "In another bowl, beat together {wet_ingredients}."
    template_3 = "Now combine and mix all the ingredients together."
    template_3_1 = "Chill the cookie dough in the refrigerator for " + random.choice(time_refrig) + " hour."
    template_4 = "Spread the batter into a cake pan."
    template_4_1 = "Now roll the cookie dough into balls and place them on a baking tray."
    template_5 = "Bake for " + random.choice(time) + " minutes."

    dry_ingredients = ""
    wet_ingredients = ""

    for elem in dry_ingr:
        if dry_ingr.index(elem) == (len(dry_ingr) - 1):
            dry_ingredients += "and " + elem
        else:
            dry_ingredients += elem + ", "

    for elem in wet_ingr:
        if wet_ingr.index(elem) == (len(wet_ingr) - 1):
            wet_ingredients += "and " + elem
        else:
            wet_ingredients += elem + ", "

    # Create a dictionary of ingredient names and other details
    recipe_details = {
        "dry_ingredients": dry_ingredients,
        "wet_ingredients": wet_ingredients,
        "temperature": temp,
        "time": time,
        "time_refrig": time_refrig
    }

    # Replace placeholders in templates with actual details
    template_0 = template_0.format(**recipe_details)
    template_1 = template_1.format(**recipe_details)
    template_2 = template_2.format(**recipe_details)
    template_3 = template_3.format(**recipe_details)
    template_3_1 = template_3_1.format(**recipe_details)
    template_4_1 = template_4_1.format(**recipe_details)
    template_4 = template_4.format(**recipe_details)
    template_5 = template_5.format(**recipe_details)

    # Generate either a cookie recipe or a cake recipe with probability = cookie_to_cake_ratio
    cookie_to_cake_ration = 0.5

    if random.randint(0, 1) < cookie_to_cake_ration:
        # Combine the modified templates to create a recipe description
        cake_description = f"{template_0}\n{template_1}\n{template_2}\n{template_3}\n{template_4}\n{template_5}"
        return cake_description
    else:
        cookie_description = f"{template_0}\n{template_1}\n{template_2}\n{template_3_1}\n{template_4_1}\n{template_5}"
        return cookie_description
