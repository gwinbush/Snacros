import numpy as np
import json
import pickle
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds

with open ('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

#there are 6466 snacks
data_lst = [(x, all_data[x]['description']) for x in all_data.keys()]

vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .7, min_df = 75)
my_matrix = vectorizer.fit_transform([x[1] for x in data_lst]).transpose()

u, s, v_trans = svds(my_matrix, k=100)

#PLOT
# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# plt.plot(s[::-1])
# plt.xlabel("Singular value number")
# plt.ylabel("Singular value")
# plt.show()

words_compressed, _, docs_compressed = svds(my_matrix, k=20)
docs_compressed = docs_compressed.transpose()

word_to_index = vectorizer.vocabulary_
index_to_word = {i:t for t,i in word_to_index.iteritems()}

words_compressed = normalize(words_compressed, axis = 1)

# print(word_to_index.keys())

"""Returns the 10 closest words to the input word and their scores"""
def closest_words(word_in, k = 10):
	if word_in not in word_to_index: 
		return "Not in vocab."
	sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
	asort = np.argsort(-sims)[:k+1]
	return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]

# print(closest_words("cookie"))

docs_compressed = normalize(docs_compressed, axis = 1)
"""Returns the 10 closest snacks to the input snack index and their scores."""
def closest_snacks(snack_index_in, k = 5):
    sims = docs_compressed.dot(docs_compressed[snack_index_in,:])
    asort = np.argsort(-sims)[:k+1]
    return [(data_lst[i][0],sims[i]/sims[asort[0]]) for i in asort[1:]]

#prints the 10 closest snacks for the first 10 snacks
for i in range(10):
    print(data_lst[i][0])
    for title, score in closest_snacks(i):
        print("{}:{:.3f}".format(title[:40], score))
    print()

