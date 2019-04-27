import pandas as pd
import pickle
import time

with open('Data/titles_to_ingredients.pickle', 'rb') as f:
	titles_to_ingredients = pickle.load(f)

with open('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

def jaccard(title, product):
	"""Return the jaccard similarity score between two strings of words"""
	a = set(title.split())
	b = set(product.split())
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))

def get_ingredients():
	"""Returns a dict mapping titles to their corresponding USDA product and ingreient list"""

	pd.set_option('max_colwidth',1000)
	data = pd.read_csv('Data/products.csv', low_memory=False)

	titles = list(all_data.keys())
	products = list(data.long_name)

	titles_to_ingredients = {}

	count = 1
	length = len(titles)

	#Find each corresponding USDA product and ingredient list
	for i in range(length):
		print("Processing {} of {}".format(count, length))
		count += 1

		distances = [jaccard(titles[i].lower(), p.lower()) for p in products]
		matching_product = products[distances.index(max(distances))]

		titles_to_ingredients[titles[i]] = {}
		titles_to_ingredients[titles[i]]['USDA Product'] = matching_product

		product_loc = data[data['long_name'] == matching_product].index[0]
		ingredients = data.loc[product_loc]['ingredients_english']
		titles_to_ingredients[titles[i]]['ingredients'] = ingredients


	with open('Data/titles_to_ingredients.pickle', 'wb') as f:
		pickle.dump(titles_to_ingredients, f)

def helper(title, ingredients, diet):
	"""Returns True if food is allowed by diet and False otherwise"""
	
	diet_list = {
	'vegetarian': ['meat', 'beef', 'lamb', 'pork', 'pig', 'bacon', 'buffalo', 'veal', 'horse', 'chicken', 'turkey', 'duck', 'quail', 'goose', 'beef', 'fish', 'salmon', 'flounder', 'shrimp', 'lobster', 'crab', 'anchovie', 'squid', 'scallops', 'calmari', 'mussel','kipper', 'herring', 'gelatin', 'sausage'],
	'vegan': ['meat', 'beef', 'lamb', 'pork', 'pig', 'bacon', 'buffalo', 'veal', 'horse', 'chicken', 'turkey', 'duck', 'quail', 'goose', 'beef', 'fish', 'salmon', 'flounder', 'shrimp', 'lobster', 'crab', 'anchovie', 'squid', 'scallops', 'calmari', 'mussel', 'mussel','kipper', 'herring', 'gelatin', 'milk', 'yogurt', 'cheese', 'butter', 'cream', 'whey', 'casein', 'lactose', 'eggs', 'honey', 'sausage'],
	'gluten_free': ['wheat', 'barley', 'rye', 'oats', 'flour'],
	'peanut_free': ['peanut', 'nut']
	}
	

	restricted_items = diet_list[diet]

	for food in restricted_items:
		if food in ingredients.lower() or food in title.lower() or food in all_data[title]['description'].lower():
			return False
	return True

def restrict_foods():
	"""Return a dictionary mapping dietary restriction names to lists of amazon products that are allowed by the restrictions"""
	restrictions = ['vegetarian', 'vegan', 'peanut_free', 'gluten_free']

	for title, info in titles_to_ingredients.items():
		ingredients = str(titles_to_ingredients[title]['ingredients'])

		for diet in restrictions:
			if diet == 'vegetarian':
				is_vegetarian = helper(title, ingredients, diet)
			elif diet == 'vegan':
				is_vegan = helper(title, ingredients, diet)
			elif diet == 'peanut_free':
				peanut_free = helper(title, ingredients, diet)
			elif diet == 'gluten_free':
				gluten_free = helper(title, ingredients, diet)
		if title == "Sausage Stick Sampler":
			print(is_vegetarian)
		all_data[title]['vegetarian'] = is_vegetarian
		all_data[title]['vegan'] = is_vegan
		all_data[title]['peanut_free'] = peanut_free
		all_data[title]['gluten_free'] = gluten_free

	with open('Data/FINAL_snacks_data.pickle', 'wb') as f:
		pickle.dump(all_data, f)


restrict_foods()

with open('Data/titles_to_ingredients.pickle', 'rb') as f:
	titles_to_ingredients = pickle.load(f)

with open('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

num_veggie = 0
num_vegan = 0
num_peanut_free = 0
num_gluten_free = 0
for key, value in all_data.items():
	if all_data[key]['vegetarian'] == True:
		num_veggie+=1
	if all_data[key]['vegan'] == True:
		num_vegan+=1
	if all_data[key]['peanut_free'] == True:
		num_peanut_free +=1
	if all_data[key]['gluten_free']==True:
		num_gluten_free+=1
print("num veggie: {}, num vegan: {}, num_peanut_free: {}, num_gluten_free: {}".format(num_veggie, num_vegan, num_peanut_free, num_gluten_free))
#print(all_data)