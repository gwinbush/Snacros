import json
import ast
	
def json_to_food_lst(file_name):
	food_file = open(file_name, 'r')
	food_file_str = food_file.read()
	food_file_str_lst = food_file_str.split('\n')
	food_file_str_lst = [x.strip() for x in food_file_str_lst]
	food_lst = []
	for i,line in enumerate(food_file_str_lst):
		if i != len(food_file_str_lst)-1:
			food_lst.append(ast.literal_eval(line))
	return food_lst

removed_fields = ['title', 'imUrl', 'categories', 'asin', 'salesRank']
wanted_fields = [('price', None), ('description',''), ('brand', ''), ('also_viewed', []), ('also_bought',[])]
# all_fields = ['asin', 'description', 'title', 'imUrl', 'related', 'salesRank', 'categories', 'price', 'brand']

def food_lst_to_dict(lst):
	food_dict = {}
	for d in lst:
		d_keys = d.keys()
		# for key in  d_keys:
		# 	if key not in all_fields:
		# 		all_fields.append(key)
		if 'title' not in d_keys:
			continue
		title = d['title']
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
		# if not (food_dict[title].keys()).sort() == ['description', 'price', 'also_bought', 'also_viewed', 'brand'].sort():
		# 	print(food_dict[title].keys())
	return food_dict

foods_filtered = food_lst_to_dict(json_to_food_lst("meta_Grocery_and_Gourmet_Food.json"))
# print(all_fields)
# print(len(foods_filtered.keys()))
# print(foods_filtered['Sour Punch Blue Raspberry Bite, 5 Ounce Bag -- 12 per case.'].keys())

