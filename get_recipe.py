import requests

def search_recipe(query):
    API_KEY = "708f5ac87cc44277ae7f6e0097a0764f"
    endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

    params = {
	'addRecipeInformation': True,
        'query': query,
        'apiKey': API_KEY,
        'number': 5,
        'instructionsRequired': True,
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        return f"Error {response.status_code}: {response.text}"

def get_recipe_by_id(id):
    API_KEY = "708f5ac87cc44277ae7f6e0097a0764f"
    base_url = "https://api.spoonacular.com/recipes/{}/information".format(id)
    params = {
        "Content-Type": "application/json",
        "apiKey": API_KEY
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"

def search_by_ingredients(ingredients_str):
    def format_ingredients(ingredients_str):
        # Split the string by spaces to get individual ingredients
        ingredients_list = ingredients_str.split()
        # Join the ingredients with commas
        formatted_ingredients = ",".join(ingredients_list)
        return formatted_ingredients
    
    # Format the input ingredients
    formatted_ingredients = format_ingredients(ingredients_str)
    
    # Your Spoonacular API key
    api_key = "708f5ac87cc44277ae7f6e0097a0764f"

    # Base URL for the "Search Recipes by Ingredients" endpoint
    url = "https://api.spoonacular.com/recipes/findByIngredients"

    # Parameters for the API call
    params = {
        "apiKey": api_key,
        "ingredients": formatted_ingredients,
        "number": 5,

        "ignorePantry": True,
    }
    print(formatted_ingredients)
    # Make the GET request to the Spoonacular API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        recipes = response.json()
        return recipes
    else:
        return None

def recipe_info(response):
    recipe = {}
    recipes = []
    for _ in response:
        recipe = {}
        recipe['title'] = _['title']
        recipe['id'] = _['id']
        recipe['healthScore'] = _['healthScore']
        recipe['cuisines'] = _['cuisines']
        recipe['readyInMinutes'] = _['readyInMinutes']
        recipe['summary'] = _['summary']
        recipe['analyzedInstructions'] = _['analyzedInstructions']
        recipe['image'] = _['image']
        recipes.append(recipe)
    return recipes
        
