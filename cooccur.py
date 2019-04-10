import pickle
import numpy as np

with open ('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

with open('Data/title_to_index.pickle', 'rb') as f:
	title_to_ind = pickle.load(f)
# print(title_to_ind)

# print(all_data['Dried Fruit Kiwi-Strawberry Mix'])
def create_term_doc_mat(data):
	term_doc_mat = np.zeros((len(data), len(data)))
	for key, data_dict in data.items():
		curr_snack_ind = title_to_ind[key]
		related_snacks = data_dict['also_bought']
		# print(related_snacks)
		# print(related_snacks)
		related_snacks_ind = [title_to_ind[x] for x in related_snacks]
		for i in related_snacks_ind:
			# print("BEFORE" + str(term_doc_mat[curr_snack_ind, i]))
			term_doc_mat[curr_snack_ind, i] += 1
			# print("AFTER" + str(term_doc_mat[curr_snack_ind, related_snacks_ind]))
	return term_doc_mat

def create_cooccurence_mat(term_doc_mat):
	pass

def PMI(cooccurence_mat):
	pass

def pmi_sim(snack_title, pmi_mat):
	pass

# def cos_sim(snack_title, term_doc_mat):
# 	pass

term_doc_mat = create_term_doc_mat(all_data)
# test_ind = title_to_ind['Frito Lay Sabritas Japanese Style Peanuts']
# print(all_data['Frito Lay Sabritas Japanese Style Peanuts'])
# print(np.sum(term_doc_mat[test_ind, :]))
