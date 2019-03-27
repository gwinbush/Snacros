import json
import ast
import csv,os
import re
	
"""Returns list of dictionaries for every entry in the amazon dataset"""
def json_to_food_lst(file_name):
	food_file = open(file_name, 'r')
	food_file_str = food_file.read()
	food_file_str_lst = food_file_str.split('\n')
	food_file_str_lst = [x.strip() for x in food_file_str_lst]
	food_lst = []
	for i,line in enumerate(food_file_str_lst):
		if i != len(food_file_str_lst)-1:
			food_d = ast.literal_eval(line)
			food_lst.append(food_d)
	#print(len(food_lst))
	return food_lst

removed_fields = ['title', 'imUrl', 'asin', 'salesRank', 'categories']
wanted_fields = [('price', None), ('description',''), ('brand', ''), ('also_viewed', []), ('also_bought',[])]
# all_fields = ['asin', 'description', 'title', 'imUrl', 'related', 'salesRank', 'categories', 'price', 'brand']

"""Returns a dictionary of food items after filtering out non-snack items"""
def filter_snacks(data):

	"""Helper funtion to check if any words in a list appear in a given string"""
	def contains_word(text, word_list):
	    if text != '':
	        for word in word_list:
	            if word.lower() in text.lower():
	                return True
	    return False

	bad_words = ["Drink", "Oil", "Sauce", "Tea", "Coffee", "Dressing", "Candy", "Syrup", "Fluid"]

	filtered_products = {}

	for title, info in data.items():
	    desc = info["description"]
	    if "snack" in desc.lower() and not contains_word(desc, bad_words):
	    	filtered_products[title] = info

	return filtered_products

"""Turns list of dictionaries into a single dictionary with snack titles as keys and 
dictionary of other data as values"""
def food_lst_to_dict(lst):
	food_dict = {}
	for d in lst:
		d_keys = d.keys()
		if 'title' not in d_keys:
			continue
		title = d['title']
		if 'Clif Bar' in title:
			#print(title)
			pass
		for f1 in removed_fields:
			if f1 in d_keys:
				d.pop(f1)
		if 'related' in d_keys:
			if 'also_bought' in d['related'].keys():
				also_bought = d['related']['also_bought']
				d['also_bought'] = also_bought
			else:
				d['also_bought'] = []
			if 'also_viewed' in d['related'].keys():
				also_viewed = d['related']['also_viewed']
				d['also_viewed'] = also_viewed
			else:
				d['also_viewed'] = []
			d.pop('related')
		for (f2,val) in wanted_fields:
			if f2 not in d_keys:
				d[f2] = val
		food_dict[title] = d
	return food_dict


all_foods = json_to_food_lst("Data/meta_Grocery_and_Gourmet_Food.json")
filtered_snacks = filter_snacks(food_lst_to_dict(all_foods))

with open('Data/filtered_snacks.json', 'w') as file:
    json.dump(filtered_snacks, file)


    