import pandas as pd
import csv
import pickle
import time

def get_average_ratings():
	data = pd.read_csv('Data/ratings_Grocery_and_Gourmet_Food.csv')
	data.columns = ['user', 'product', 'rating', 'timestamp']

	data = data.drop(data.columns[[0,3]], axis=1)

	data = data.groupby('product', as_index=False)['rating'].mean()
	data.set_index('product', inplace = True)

	return data


def add_ratings():
	
	with open ('Data/FINAL_snacks_data.pickle', 'rb') as f:
		snacks_data = pickle.load(f)

	with open ('Data/titles_to_asin.pickle', 'rb') as f:
		titles_to_asin = pickle.load(f)

	ratings = get_average_ratings()

	new_dict = {}
	for title, info in snacks_data.items():
		try:
			info['rating'] = ratings.loc[titles_to_asin[title]]['rating']
			new_dict[title] = info
		except:
			pass

	with open('Data/FINAL_snacks_data.pickle', 'wb') as f:
		pickle.dump(new_dict,f)


	 
add_ratings()


