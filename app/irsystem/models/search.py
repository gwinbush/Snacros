import pickle
import time

def cooccur(snack_data, snack_1, snack_2):
	if snack_1 in snack_data[snack_2]['also_bought']:
		return True
	return False

def get_score(snack, snack_query, protein_query, carb_query, fat_query):
	"""
	Returns the similarity score between the query data and a snack

	Arguments:
		snack: string representing the title of a snack document
		snack_query: string representing the title of a snack query
		protein_query: string "high", "med", or "low"
		carb_query: string "high", "med", or "low"
		fat_query: string "high", "med", or "low"
	
	"""
	start_time = time.time()

	#Load necessary data
	with open ('../../../Data/percentagesDict.pickle', 'rb') as f:
		percentage_data = pickle.load(f)

	with open ('../../../Data/FINAL_snacks_data.pickle', 'rb') as f:
		snack_data = pickle.load(f)

	#Set constants
	LOW_FAT = .3
	HIGH_FAT = .6
	LOW_CARB = .1
	HIGH_CARB = .2
	LOW_PRO = .2
	HIGH_PRO = .4

	#Convert macro percentages to 'high', 'med', 'low' categories
	fat = percentage_data[snack]['fat']
	protein = percentage_data[snack]['protein']
	carb = percentage_data[snack]['carb']

	if fat > HIGH_FAT:
		fat_content = 'high'
	elif fat < LOW_FAT:
		fat_content = 'low'
	else:
		fat_content = 'med'

	if protein > HIGH_PRO:
		protein_content = 'high'
	elif protein < LOW_PRO:
		protein_content = 'low'
	else:
		protein_content = 'med'

	if carb > HIGH_CARB:
		carb_content = 'high'
	elif carb < LOW_CARB:
		carb_content = 'low'
	else:
		carb_content = 'med'

	#Set x values
	x1 = fat_query == fat_content
	x2 = carb_query == carb_content
	x3 = protein_query == protein_content
	x4 = cooccur(snack_data, snack, snack_query) 
	x5 = snack_data[snack]['rating']

	w1 = 1
	w2 = 1
	w3 = 1
	w4 = 1
	w5 = 1
	
	#print('x1: {}, x2: {}, x3: {}, x4: {}, x5: {}'.format(x1, x2, x3, x4, x5))
	print("--- %s seconds ---" % (time.time() - start_time))


	return w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5

def top_n_scores(snack_data, n, snack_query, protein_query, carb_query, fat_query):
	"""
	Returns the top n snacks with the highest similarity scores to the query snack
	
	Arguments:
		snack_data: dictionary containing all the snacks and info
		n: number of snacks to return
		snack_query: string representing the title of a snack query
		protein_query: string "high", "med", or "low"
		carb_query: string "high", "med", or "low"
		fat_query: string "high", "med", or "low"
	"""

	#Loop through the snacks in dictionary and compute the score for each one
	scores_list = []
	
	for title, info in snack_data.items():
		score = get_score(title, snack_query, protein_query, carb_query, fat_query)
		scores_list.append((title, score))

	scores.sort(key=lambda tup: tup[1], reverse=True)

	return scores_list[0:n]







