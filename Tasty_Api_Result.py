import os
import requests
from dotenv import load_dotenv
from typing import Optional
load_dotenv()
class Tasty_App:
	def __init__(self):
		self.headers = {
			"X-RapidAPI-Key": os.getenv("X_RapidAPI_Key"),
			"X-RapidAPI-Host": os.getenv('X_RapidAPI_Host')
		}
	def get_recipies_auto_complete(self, Food_name_or_igredient: str):
		url = "https://tasty.p.rapidapi.com/recipes/auto-complete"
		querystring = {"prefix": Food_name_or_igredient}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def get_recipes_list(self, range_from: str, range_to: str, tags : Optional[str] = "0", Food_name_or_igredient: Optional[str] = "0"):
		url = "https://tasty.p.rapidapi.com/recipes/list"
		if tags == "0" and Food_name_or_igredient == "0":
			querystring = {"from": range_from, "size": range_to}
		elif tags == "0" and Food_name_or_igredient != "0":
			querystring = {"from": range_from, "size": range_to, "q": Food_name_or_igredient}
		elif tags != "0" and Food_name_or_igredient == "0":
			querystring = {"from": range_from, "size": range_to, "tags": tags}
		else:
			querystring = {"from": range_from, "size": range_to, "tags": tags, "q": Food_name_or_igredient}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def get_recipes_list_similarities(self, recipe_id: str):
		url = "https://tasty.p.rapidapi.com/recipes/list-similarities"
		querystring = {"recipe_id": recipe_id}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def get_recipes_get_more_info(self, recipe_id: str):
		url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
		querystring = {"recipe_id": recipe_id}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def get_tips_list(self, recipe_id: str, range_from: str, range_to: str):
		url = "https://tasty.p.rapidapi.com/tips/list"
		if range_from == "0" and range_to == "0":
			querystring = {"id": recipe_id}
		elif range_from == "0" and range_to != "0":
			querystring = {"id": recipe_id, "size": range_to}
		elif range_from != "0" and range_to == "0":
			querystring = {"id": recipe_id, "from": range_from}
		else:
			querystring = {"id": recipe_id, "from": range_from, "size": range_to}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def get_tags_list(self):
		url = "https://tasty.p.rapidapi.com/tags/list"
		response = requests.get(url, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def get_feeds_list(self, range_to: str, timezone: str, vegetarian: bool ,range_from: str):
		url = "https://tasty.p.rapidapi.com/feeds/list"
		querystring = {"size": range_to, "timezone": timezone, "vegetarian": vegetarian, "from": range_from}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
	def recipies_detail(self, recipe_id: str):
		url = "https://tasty.p.rapidapi.com/recipes/detail"
		querystring = {"id": recipe_id}
		response = requests.get(url, headers=self.headers, params=querystring)
		result = response.json()
		print(result)
		return result
class Bespoke_Diet_Generator:
	def __init__(self):
		self.headers = {
			'content-type': 'application/json',
			'X-RapidAPI-Key': '396c88a5admshccd77e097b048c9p1ee005jsn313488fd1765',
			'X-RapidAPI-Host': 'bespoke-diet-generator.p.rapidapi.com'
	}
	def create_new_user(self, height: int, weight: int, date_of_birth: str,  sex: str ,activity_level: str):
		url = 'https://bespoke-diet-generator.p.rapidapi.com/user'
		payload = {
			"height": height,
			"weight": weight,
			"dateOfBirth": date_of_birth,
			"sex": sex,
			"activityLevel": activity_level
		}
		response = requests.post(url, json=payload, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def get_users_information(self, userId: str ):
		url = f"https://bespoke-diet-generator.p.rapidapi.com/user/{userId}"
		response = requests.get(url, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def update_user(self, userid: str, weight: int, activity_level: str):
		url = f"https://bespoke-diet-generator.p.rapidapi.com/user/{userid}"
		payload = {
			"weight": weight,
			"activityLevel": activity_level
		}
		response = requests.get(url, headers=self.headers.update({"Content-Type":"application/json"}))
		result = response.json()
		print(result)
		return result
class gym_calculator:
	def __init__(self):
		self.headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "396c88a5admshccd77e097b048c9p1ee005jsn313488fd1765",
		"X-RapidAPI-Host": "gym-calculations.p.rapidapi.com"
	}
	def bmi(self, weight: int, height: float):
		url = "https://gym-calculations.p.rapidapi.com/bmi"

		payload = {
			"weight": weight,
			"height": height
		}
		response = requests.post(url, json=payload, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def calculate_macronutrient_ratios(self, goal:str, weight: int, height: float, age: int, sex: str, activity_level: str):
		url = "https://gym-calculations.p.rapidapi.com/calculate-macronutrient-ratios"
		payload = {
			"goal": goal,
			"weight": weight,
			"height": height,
			"age": age,
			"gender": sex,
			"activity_level": activity_level
		}
		response = requests.post(url, json=payload, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def bmr(self, weight: float, height: float, age: int, sex: str):
		url = "https://gym-calculations.p.rapidapi.com/bmr"
		payload = {
			"weight": 70,
			"height": 1.8,
			"age": 30,
			"gender": "male"
		}
		response = requests.post(url, json=payload, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def orm(self, weight_lifted: float, reps: int):
		url = "https://gym-calculations.p.rapidapi.com/1rm"

		payload = {
			"weight_lifted": weight_lifted,
			"reps": reps
		}
		response = requests.post(url, json=payload, headers=self.headers)
		result = response.json()
		print(result)
		return result
class Exercise:
	def __init__(self):
		self.headers = {"X-RapidAPI-Key": "396c88a5admshccd77e097b048c9p1ee005jsn313488fd1765",
		"X-RapidAPI-Host": "musclewiki.p.rapidapi.com"
		}
	def get_exercise_by_id(self, id: int):
		url = f"https://musclewiki.p.rapidapi.com/exercises/{id}"
		response = requests.get(url, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def get_attribiutes(self):
		url = "https://musclewiki.p.rapidapi.com/exercises/attributes"
		response = requests.get(url, headers=self.headers)
		result = response.json()
		print(result)
		return result
	def get_exercises(self):
		url = "https://musclewiki.p.rapidapi.com/exercises"
		response = requests.get(url, headers=self.headers)
		result = response.json()
		result = [p['Category']for p in result]
		print(result)
		return result



Exercise_instance = Exercise()
# Exercise_instance.get_exercise_by_id(1)
# Exercise_instance.get_attribiutes()
Exercise_instance.get_exercises()
# Tasty_App_Object = Tasty_App()
# Tasty_App_Object.get_recipies_auto_complete('chicken')
# generator = Bespoke_Diet_Generator()
# generator.get_users_information('A5soqCXOD0PwrwUgjNATC')
# gym_calculator_instance = gym_calculator()
# gym_calculator_instance.bmr(80.2, 172, 22, 'male')