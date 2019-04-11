import pickle
import numpy as np

with open ('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

with open('Data/title_to_index.pickle', 'rb') as f:
	title_to_ind = pickle.load(f)
# print(title_to_ind)

"""Takes in our dictionary of snack data and returns a matrix where element [i,j]
means that product j was also bought with product i"""
def create_term_doc_mat(data):
	term_doc_mat = np.ones((len(data), len(data)))
	for key, data_dict in data.items():
		curr_snack_ind = title_to_ind[key]
		related_snacks = data_dict['also_bought']
		related_snacks_ind = [title_to_ind[x] for x in related_snacks]
		for i in related_snacks_ind:
			term_doc_mat[curr_snack_ind, i] += 1
	return term_doc_mat

def create_cooccurence_mat(term_doc_mat):
	return np.dot(term_doc_mat.T, term_doc_mat)

def PMI(cooccurence_mat, term_doc_mat):
	sum_term_doc = np.sum(term_doc_mat, axis = 0)
	PMI_1 = np.divide(cooccurence_mat, sum_term_doc)
	return np.divide(PMI_1.transpose(), sum_term_doc)

def pmi_sim(snack_title, pmi_mat):
	pass

# def cos_sim(snack_title, term_doc_mat):
# 	pass

term_doc_mat = create_term_doc_mat(all_data)
cooccur_mat = create_cooccurence_mat(term_doc_mat)
pmi = PMI(cooccur_mat, term_doc_mat)
print(pmi)
# test_ind = title_to_ind['Frito Lay Sabritas Japanese Style Peanuts']
# print(all_data['Frito Lay Sabritas Japanese Style Peanuts'])
# print(np.sum(term_doc_mat[test_ind, :]))
