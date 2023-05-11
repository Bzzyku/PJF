import os
import requests
from dotenv import load_dotenv
load_dotenv()

headers = {
	"X-RapidAPI-Key": os.getenv("X_RapidAPI_Key"),
	"X-RapidAPI-Host": os.getenv('X_RapidAPI_Host')
}

def get_recipies_auto_complete(Food_name_or_igredient: str):
	url = "https://tasty.p.rapidapi.com/recipes/auto-complete"
	querystring = {"prefix": Food_name_or_igredient}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result

def get_recipes_list(range_from: str, range_to: str, tags: str, Food_name_or_igredient: str):
	url = "https://tasty.p.rapidapi.com/recipes/list"
	querystring = {"from": range_from, "size": range_to, "tags": tags, "q": Food_name_or_igredient}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result
def get_recipes_list_similarities():
	pass



get_recipies_auto_complete('chicken')
get_recipes_list("0","3","under_30_minutes","chicken")