import numpy as np
import json
import pickle
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from snack_filter import reviews_dict

with open('Data/titles_to_asin.pickle', 'rb') as f:
	titles_to_asin = pickle.load(f)

with open('Data/reviews_dict.pickle', 'rb') as f:
	reviews_dict = pickle.load(f)

#remove the snacks we dont want
def remove_snacks():
	with open('Data/FINAL_snacks_data.pickle', 'rb') as f:
		all_data = pickle.load(f)
	# print(all_data)
	with open('Data/percentagesDict.pickle', 'rb') as f:
		percentagesDict = pickle.load(f)

	# percentagesDict.pop('')
	# all_data.pop('')
	titles_to_remove = []

	# titles_to_remove = ['Jell-O Cook and Serve Pudding and Pie Filling Lemon', 
	# 						'Fleischmann\'s Simply Homemade Baking Mix Pretzel Creations',
	# 						'Gourmet Fishing Gear | Fishing Creel Deluxe Gourmet Snacks | Great Fishing Gift Idea!',
	# 						'Pizza Bar']
	for title, data in all_data.items():
		if 'gerber' in title.lower():
			titles_to_remove.append(title)
		if 'lactation cookies' in title.lower():
			titles_to_remove.append(title)
		if 'pet' in title.lower():
			titles_to_remove.append(title)
		if 'little yums' in title.lower():
			titles_to_remove.append(title)	
		if 'baby food' in title.lower():
			titles_to_remove.append(title)	
		if 'mum-mum' in title.lower():
			titles_to_remove.append(title)	
		if 'happy baby' in title.lower():
			titles_to_remove.append(title)	
		if 'nurturme' in title.lower():
			titles_to_remove.append(title)
		if 'Ella\'s Kitchen' in title:
			titles_to_remove.append(title)
		if 'Plum Organics' in title:
			titles_to_remove.append(title)
		if 'mum mum' in title.lower():
			titles_to_remove.append(title)
		if 'ellas kitchen' in title.lower():
			titles_to_remove.append(title)
		if 'gift basket' in title.lower():
			titles_to_remove.append(title)
		if 'baby wipes' in title.lower():
			titles_to_remove.append(title)
		if 'tastybaby' in title.lower():
			titles_to_remove.append(title)
		if 'happybaby' in title.lower():
			titles_to_remove.append(title)
		if 'gift' in title.lower():
			titles_to_remove.append(title)
		if 'seasoning' in title.lower():
			titles_to_remove.append(title)
		if title == 'Sistema Microwave Noodle Bowl 940ml':
			titles_to_remove.append(title)
		if titles_to_asin[title] == 'B00DGXB3AE':
			titles_to_remove.append(title)

	for t in titles_to_remove:
		all_data.pop(t)
		percentagesDict.pop(t)

	# for title, data in all_data.items():
	# 	if ')' in title and '(' not in title:
	# 		all_data[title.replace(')', '')] = data
	# 	if title == 'Pizza Bar Full Size)':
	# 		all_data['Pizza Bar'] = data


	with open('Data/FINAL_snacks_data.pickle', 'wb') as f:
		pickle.dump(all_data, f)

	with open('Data/percentagesDict.pickle', 'wb') as f:
		pickle.dump(percentagesDict, f)
remove_snacks()

with open('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

# create reverse indices
title_to_ind = {}
ind_to_title = {}
new_titles_lst = all_data.keys()
for i, title in enumerate(new_titles_lst):
	title_to_ind[title] = i
	ind_to_title[i] = title

with open('Data/index_to_title.pickle', 'wb') as f:
	pickle.dump(ind_to_title, f)

with open('Data/title_to_index.pickle', 'wb') as f:
	pickle.dump(title_to_ind, f)

data_lst = []
for i in range(len(ind_to_title)):
	title = ind_to_title[i]
	asin = titles_to_asin[title]
	if asin in reviews_dict.keys():
		add = ''
		for rev in reviews_dict[asin]:
			add += rev
		data_lst.append((title, all_data[title]['description'] + " " + add))
	else:
		data_lst.append((title, all_data[title]['description']))

#do svd
vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .7)
my_matrix = vectorizer.fit_transform([descrip for t, descrip in data_lst]).transpose()

words_compressed, _, docs_compressed = svds(my_matrix, k=20)
docs_compressed = docs_compressed.transpose()
words_compressed = normalize(words_compressed, axis = 1)
word_to_index = vectorizer.vocabulary_

index_to_word = {i:t for t,i in word_to_index.items()}

docs_compressed = normalize(docs_compressed, axis = 1)

with open('Data/docs_compressed.pickle', 'wb') as f:
	pickle.dump(docs_compressed, f)

with open('Data/words_compressed.pickle', 'wb') as f:
	pickle.dump(words_compressed, f)

with open('Data/index_to_word.pickle', 'wb') as f:
	pickle.dump(index_to_word, f)

with open('Data/word_to_index.pickle', 'wb') as f:
	pickle.dump(word_to_index, f)


"""Returns the 10 closest words to the input word and their scores"""
def closest_words(word_in, k = 10):
	if word_in not in word_to_index: 
		return "Not in vocab."
	sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
	asort = np.argsort(-sims)[:k+1]
	return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]

# word_to_index = vectorizer.vocabulary_
"""Returns the 10 closest snacks to the input word and their scores"""
def closest_snacks_to_word(word_in, k =  10):
	if word_in not in word_to_index: 
		return "Not in vocab."
	sims = docs_compressed.dot(words_compressed[word_to_index[word_in],:])
	asort = np.argsort(-sims)[:k+1]
	return [(data_lst[i][0],sims[i]/sims[asort[0]]) for i in asort[1:]]

# print(closest_words("cookie"))
# print(closest_projects_to_word(''))


"""Returns the 10 closest snacks to the input snack index and their scores."""
def closest_snacks_to_snack(snack_index_in, k = 5):
    sims = docs_compressed.dot(docs_compressed[snack_index_in,:])
    asort = np.argsort(-sims)[:k+1]
    return [(data_lst[i][0],sims[i]/sims[asort[0]]) for i in asort[1:]]
# print(closest_snacks_to_snack(title_to_ind['Shultz Pretzels Thin Pretzels']))
# print(closest_snacks_to_word('protein'))

#prints the 10 closest snacks for the first 10 snacks
# for i in range(10):
#     print(data_lst[i][0])
#     for title, score in closest_snacks(i):
#         print("{}:{:.3f}".format(title[:40], score))
#     print()

