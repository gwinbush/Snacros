import pickle
import json


#Load snack JSON file
with open('Data/data_with_nutrients.json') as json_file:
    data = json.load(json_file)

# Store data (pickle)
with open('Data/snack_data.pickle', 'wb') as file:
    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

#Reopen the data
with open('Data/snack_data.pickle','rb') as f:
	old_titles_data = pickle.load(f) 

with open ('Data/asin_to_titles.pickle', 'rb') as f:
	asin_to_titles = pickle.load(f)

with open('Data/titles_to_asin.pickle', 'rb') as f:
	titles_to_asin = pickle.load(f)

with open('Data/old_to_new_title.pickle', 'rb') as f:
	old_to_new_title = pickle.load(f)

with open('Data/fixed_filtered_snacks.pickle', 'rb') as f:
	fixed_filtered_snacks = pickle.load(f)


# print(old_titles_data)

all_asin = asin_to_titles.keys()

new_titles_dict = {}
for old_title, data in old_titles_data.items():
	new_title = old_to_new_title[old_title]

	also_bought = fixed_filtered_snacks[new_title]['also_bought']

	also_bought = [asin_to_titles[x] for x in also_bought if x in all_asin]
	also_viewed = fixed_filtered_snacks[new_title]['also_viewed']
	also_viewed = [asin_to_titles[x] for x in also_viewed if x in all_asin]
	data['also_bought'] = also_bought
	data['also_viewed'] = also_viewed
	new_titles_dict[new_title] = data

with open('Data/FINAL_snacks_data.pickle', 'w') as f:
	pickle.dump(new_titles_dict, f)


title_to_ind = {}
ind_to_title = {}

new_titles_lst = new_titles_dict.keys()
for i, title in enumerate(new_titles_lst):
	title_to_ind[title] = i
	ind_to_title[i] = title

# print(title_to_ind)
# print(ind_to_title)

with open('Data/title_to_index', 'w') as f:
	pickle.dump(title_to_ind,f)

with open('Data/index_to_title', 'w') as f:
	pickle.dump(ind_to_title,f)



