import json
import ast
import requests
from bs4 import BeautifulSoup
from lxml import html  
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep
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
	print(len(food_lst))
	return food_lst

removed_fields = ['title', 'imUrl', 'asin', 'salesRank', 'categories']
wanted_fields = [('price', None), ('description',''), ('brand', ''), ('also_viewed', []), ('also_bought',[])]
# all_fields = ['asin', 'description', 'title', 'imUrl', 'related', 'salesRank', 'categories', 'price', 'brand']

"""Returns a list of dictionaries for only the snack foods we want"""
def filter_snacks(lst):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	url_part = 'https://amazon.com/dp/'
	snacks = []
	for i in range(len(lst)): #CHANGE THIS TO SOMETHING LOWER IF YOU WANT TO TEST
		d = lst[i]
		asin = d['asin']
		print(asin)
		if 'title' in d.keys():
			print(d['title']) 

		url = url_part + asin

		html = requests.get(url, headers = headers)

		data = html.text
		soup = BeautifulSoup(data, features="lxml")
		if not soup.findAll(text=re.compile('Snack Foods'), limit = 1) == []:
			snacks.append(d)
	return snacks


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
			print(title)
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


all_foods = json_to_food_lst("/Users/Judy/Desktop/meta_Grocery_and_Gourmet_Food.json")
filtered_snacks = filter_snacks(all_foods)
print(len(filtered_snacks))
snack_dict = food_lst_to_dict(filtered_snacks)
print(len(snack_dict.keys()))
print(snack_dict.keys())
# print(all_fields)
# print(len(foods_filtered.keys()))
# print(foods_filtered['Sour Punch Blue Raspberry Bite, 5 Ounce Bag -- 12 per case.'].keys())

