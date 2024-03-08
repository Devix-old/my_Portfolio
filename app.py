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
