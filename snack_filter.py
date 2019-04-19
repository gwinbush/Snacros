import json
import ast
import csv,os
import re
import pickle
	

def parse_title(snack_title):
	snack_title = snack_title.replace('&amp;', '&')
	snack_title = snack_title.replace('&quot;', '\'')
	snack_title = snack_title.replace('&#12288;', ' ')
	parts = []
	if ',' in snack_title:
		parts = snack_title.split(',')
	elif '(' in snack_title:
		parts = snack_title.split('(')
	if len(parts) == 1 or parts == []:
		'TRUE'
		return snack_title

	final_title = ''
	parts = [x.strip() for x in parts]
	for i in range(len(parts)):
			if i == 0:
				final_title += parts[i]
			else:
				if (not any(char.isdigit() for char in parts[i])) and any(char.isalpha() for char in parts[i]):
					final_title = final_title + ' ' + parts[i]

	if '&amp;' in final_title:
		final_title.replace('&amp;', 'and')
		# print(final_title)
	return final_title

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

removed_fields = ['title', 'imUrl', 'salesRank', 'categories']
# removed_fields = ['title', 'asin', 'imUrl', 'salesRank', 'categories']

wanted_fields = [('price', None), ('description',''), ('brand', ''), ('also_viewed', []), ('also_bought',[])]
# all_fields = ['asin', 'description', 'title', 'imUrl', 'related', 'salesRank', 'categories', 'price', 'brand']


snack_titles = []
asin_to_title = {}
old_to_new_title = {}
title_to_asin = {}

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

	for old_title, info in data.items():
		desc = info["description"]

		if "snack" in desc.lower() and not contains_word(desc, bad_words):
			title = parse_title(old_title)
			old_to_new_title[old_title] = title
			snack_titles.append(title)
			asin_to_title[info['asin']] = title
			title_to_asin[title] = info['asin']
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
			if f2 not in d.keys():
				d[f2] = val
		food_dict[title] = d

	return food_dict

def reviews_lst_to_dict(lst):
	asin_to_data = {}
	for i in lst:
		asin = i['asin']
		review = i['reviewText']
		review = review.replace('&#34', '').lower()
		if asin in asin_to_data.keys():
			asin_to_data[asin].append(review)
		else:
			asin_to_data[asin] = [review]
	return asin_to_data
# all_foods = json_to_food_lst("/Users/Judy/Desktop/meta_Grocery_and_Gourmet_Food.json")
# filtered_snacks = filter_snacks(food_lst_to_dict(all_foods))
# # print(filtered_snacks)
# # print(snack_titles)
# with open('Data/snack_titles.pickle', 'w') as f:
# 	pickle.dump(snack_titles, f)

# with open ('Data/asin_to_titles.pickle', 'w') as f:
# 	pickle.dump(asin_to_title,f)

# with open('Data/titles_to_asin.pickle', 'w') as f:
# 	pickle.dump(title_to_asin, f)

# with open('Data/old_to_new_title.pickle', 'w') as f:
# 	pickle.dump(old_to_new_title,f)

# with open('Data/fixed_filtered_snacks.pickle', 'w') as f:
# 	pickle.dump(filtered_snacks, f)
# with open('Data/filtered_snacks.json', 'w') as file:
#     json.dump(filtered_snacks, file)

more_reviews = json_to_food_lst("/Users/Judy/Desktop/reviews_Grocery_and_Gourmet_Food_5.json")
reviews_dict = reviews_lst_to_dict(more_reviews)
with open('Data/reviews_dict.pickle', 'wb') as f:
	pickle.dump(reviews_dict, f)
# for title, lst in reviews_dict.items():
# 	print(len(lst)) 



	