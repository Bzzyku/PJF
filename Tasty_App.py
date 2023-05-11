import os
import requests
from dotenv import load_dotenv
from typing import Optional
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

def get_recipes_list(range_from: str, range_to: str, tags : Optional[str] = "0", Food_name_or_igredient: Optional[str] = "0"):
	url = "https://tasty.p.rapidapi.com/recipes/list"
	if tags == "0" and Food_name_or_igredient == "0":
		querystring = {"from": range_from, "size": range_to}
	elif tags == "0" and Food_name_or_igredient != "0":
		querystring = {"from": range_from, "size": range_to, "q": Food_name_or_igredient}
	elif tags != "0" and Food_name_or_igredient == "0":
		querystring = {"from": range_from, "size": range_to, "tags": tags}
	else:
		querystring = {"from": range_from, "size": range_to, "tags": tags, "q": Food_name_or_igredient}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result

def get_recipes_list_similarities(recipe_id: str):
	url = "https://tasty.p.rapidapi.com/recipes/list-similarities"
	querystring = {"recipe_id": recipe_id}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result


def get_recipes_get_more_info(recipe_id: str):
	url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
	querystring = {"recipe_id": recipe_id}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result


def get_tips_list(recipe_id: str, range_from: str, range_to: str):
	url = "https://tasty.p.rapidapi.com/tips/list"
	if range_from == "0" and range_to == "0":
		querystring = {"id": recipe_id}
	elif range_from == "0" and range_to != "0":
		querystring = {"id": recipe_id, "size": range_to}
	elif range_from != "0" and range_to == "0":
		querystring = {"id": recipe_id, "from": range_from}
	else:
		querystring = {"id": recipe_id, "from": range_from, "size": range_to}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result

def get_tags_list():
	url = "https://tasty.p.rapidapi.com/tags/list"
	response = requests.get(url, headers=headers)
	result = response.json()
	print(result)
	return result


def get_feeds_list(range_to: str, timezone: str, vegetarian: bool ,range_from: str):
	url = "https://tasty.p.rapidapi.com/feeds/list"
	querystring = {"size": range_to, "timezone": timezone, "vegetarian": vegetarian, "from": range_from}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result


def recipies_detail(recipe_id: str):
	url = "https://tasty.p.rapidapi.com/recipes/detail"
	querystring = {"id": recipe_id}
	response = requests.get(url, headers=headers, params=querystring)
	result = response.json()
	print(result)
	return result


get_recipies_auto_complete('chicken')
get_recipes_list("0","3","under_30_minutes","chicken")
get_recipes_list_similarities("8138")
