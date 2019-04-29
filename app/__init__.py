# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
from flask import Flask, render_template, request, json
# from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
# import filters
import time
import pickle
import numpy as np
import json
import pickle
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import cosine_similarity
import math

start_time = time.time()
# Configure app
socketio = SocketIO()
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

net_id1 = "Judy Chen (jc2528)"
net_id2 = "Meghan Chen (mc2254)"
net_id3 = "Paula Moya Nieto (pm445)"
net_id4 = "Gabriel Winbush (gw262)"

with open('Data/FINAL_snacks_data.pickle', 'rb') as f:
	all_data = pickle.load(f)

with open('Data/index_to_title.pickle', 'rb') as f:
	index_to_title = pickle.load(f)

with open("Data/title_to_index.pickle", "rb") as f:
	title_to_index = pickle.load(f)

with open("Data/titles_to_asin.pickle", "rb") as f:
	titles_to_asin = pickle.load(f)

with open("Data/percentagesDict.pickle","rb") as f:
	percentagesDict = pickle.load(f);

with open('Data/docs_compressed.pickle', 'rb') as f:
	docs_compressed = pickle.load(f)

with open("Data/imagesDict.pickle","rb") as f:
	imagesDict = pickle.load(f);

with open('Data/reviews_dict.pickle', 'rb') as f:
	reviews_dict = pickle.load(f)
with open('Data/index_to_word.pickle', 'rb') as f:
	index_to_word = pickle.load(f)

with open('Data/word_to_index.pickle', 'rb') as f:
	word_to_index = pickle.load(f)
with open('Data/words_compressed.pickle', 'rb') as f:
	words_compressed = pickle.load(f)

with open('Data/ratings_dict.pickle', 'rb') as f:
	ratings = pickle.load(f)

with open('Data/servingAndCalorieDict.pickle', 'rb') as f:
	otherDict = pickle.load(f)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
# db = SQLAlchemy(app)

# Import + Register Blueprints
# from app.accounts import accounts as accounts
# app.register_blueprint(accounts)
# from app.irsystem import irsystem as irsystem
# app.register_blueprint(irsystem)

# Initialize app w/SocketIO
socketio.init_app(app)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404

@app.route("/")
def index():
	return render_template('index.html', net_id1=net_id1, net_id2=net_id2, net_id3=net_id3, net_id4=net_id4)

# @app.route('/filterLevels', methods=['POST'])
# def filterLevels():
# 	fat =  request.form.get('fat');
# 	carb = request.form.get('carb');
# 	protein = request.form.get('protein');
# 	similarSnacks = request.form.get('similarSnacks');
# 	dumps = json.dumps({'status':'OK','fat':fat,'carb':carb,'protein':protein, 'similarSnacks':similarSnacks});
# 	return dumps;

@app.route('/filters', methods=['GET'])
def filters():
	fatLevel = request.args.get('fat');
	carbLevel = request.args.get('carb');
	proteinLevel = request.args.get('protein');
	query = request.args.get('similarSnacks');
	sortingInput = request.args.get('sortingInput');
	vegetarian = request.args.get('vegetarian');
	vegan = request.args.get('vegan');
	peanut_free = request.args.get('peanut_free');
	gluten_free = request.args.get('gluten_free');

	#convert ints to levels
	if fatLevel<33:
		fatLevel = "Low"
	elif fatLevel >=33 and fatLevel<67:
		fatLevel = "Medium"
	else:
		fatLevel = "High"

	if carbLevel<33:
		carbLevel = "Low"
	elif carbLevel >=33 and carbLevel<67:
		carbLevel = "Medium"
	else:
		carbLevel = "High"

	if proteinLevel<33:
		proteinLevel = "Low"
	elif proteinLevel >=33 and proteinLevel<67:
		proteinLevel = "Medium"
	else:
		proteinLevel = "High"

	filtered_snacks = {}
	
	# nutrient_match = {}
	# non_nutrient_match = {}
	for product, d in percentagesDict.items():
		# print(product, d)
		fat = d["fat"]
		carb = d["carb"]
		protein = d["protein"]
		fat_bool = False
		carb_bool = False
		protein_bool = False

		if (fatLevel == "Low" and fat > 0.0 and fat < 0.3) or (fatLevel == "Medium" and fat >= 0.3 and fat < 0.6) or (fatLevel == "High" and fat >= 0.6) or (fatLevel == "None"):
			fat_bool = True
		if (carbLevel == "Low" and carb > 0.0 and carb < 0.1) or (carbLevel == "Medium" and carb >= 0.1 and carb < 0.2) or (carbLevel == "High" and carb >= 0.2) or (carbLevel == "None"):
			carb_bool = True
		if (proteinLevel == "Low" and protein > 0.0 and protein < 0.2) or (proteinLevel == "Medium" and protein >= 0.2 and protein < 0.4) or (proteinLevel == "High" and protein >= 0.4) or (proteinLevel == "None"):
			protein_bool = True


		serving = otherDict[product]["serving"]
		calories = otherDict[product]["calories"]
		description = otherDict[product]["description"]
		# print(calories)
		filtered_snacks[product] = (carb_bool, protein_bool, fat_bool, serving, calories, description)

	#START RANKING STUFF


	w1 = 0.3 #does occur
	w2 = 0.5 #rating
	w3 = 1 #snack svd score
	w4 = 0.5 #matches carb
	w5 = 0.5 #matches protein
	w6 = 0.5 #matches fat
	w7 = 0.15 #num ratings
	w8 = 0.8 #word svd score
	
	if ',' in query:
		query_lst = query.split(',')
	else:
		query_lst = query.split(' ')
	for i in range(len(query_lst)):
		query_lst[i] = query_lst[i].strip()

	query_snack = ' '.join(query_lst)

	# FIND SIM SNACK IF QUERY NOT IN DATABASE
	if query_snack not in list(all_data.keys()):
		all_titles = list(all_data.keys())
		all_titles.insert(0, query_snack)
		vectorizer=TfidfVectorizer()
		matrix=vectorizer.fit_transform(all_titles)
		cs=cosine_similarity(matrix[0], matrix)
		sorted_row = np.argsort(cs, axis=1)[0][::-1]
		query_snack = all_titles[sorted_row[1]]
	print('NEW QUERY : ' + query_snack)

	# SVD snack to snack
	snack_index_in = title_to_index[query_snack]

	sims = docs_compressed.dot(docs_compressed[snack_index_in,:])
	asort = np.argsort(-sims)
	svd_sorted = [(index_to_title[i],sims[i]/sims[asort[0]]) for i in asort[1:]]
	svd_sorted.append((query_snack, 1.0))

	#SVD word to snack
	word_sims_lst = []
	for word_in in query_lst:
		if word_in not in word_to_index.keys():
			word_sims_lst.append((word_in, np.zeros((docs_compressed.shape[0], 1))))
		else:
			sims = docs_compressed.dot(words_compressed[word_to_index[word_in],:])
			word_sims_lst.append((word_in, sims))
			asort = np.argsort(-sims)

	matched_str = {}
	#Return sorted list of sim scores
	scores = np.zeros((len(svd_sorted),1))
	for i in range(len(svd_sorted)):
		snack, snack_svd_score = svd_sorted[i]
		word_svd_score = 0
		snack_ind = title_to_index[snack]
		matched = ''
		for word, sim_lst in word_sims_lst:
			if sim_lst[snack_ind] > 0.7:
				matched = matched + ' ' + word + ','
			word_svd_score += sim_lst[snack_ind]
		does_cooccur = snack in all_data[query_snack]['also_bought']
		rating = all_data[snack]['rating']
		asin = titles_to_asin[snack]
		if asin in reviews_dict.keys():
			num_ratings = math.log(len(reviews_dict[asin]))
		else:
			num_ratings = math.log(1)
		carb, protein, fat, _, _, _ = filtered_snacks[snack]
		if carb:
			matched = matched + ' ' + carbLevel + ' ' + 'carb' + ','
		if protein:
			matched = matched + ' ' + proteinLevel + ' ' + 'protein' + ','
		if fat:
			matched = matched + ' ' + fatLevel + ' ' + 'fat' + ','

		score = w3*snack_svd_score + w8*word_svd_score + w7*num_ratings + w2*rating + w4*carb + w5*protein + w6*fat

		#Filter out dietary restrictions
		if vegetarian == 'true' and not all_data[snack]['vegetarian']:
			score = 0
		if vegan == 'true'and not all_data[snack]['vegan']:
			score = 0
		if peanut_free == 'true' and not all_data[snack]['peanut_free']:
			score = 0
		if gluten_free == 'true' and not all_data[snack]['gluten_free']:
			score = 0

		matched_str[snack] = matched[:-1]
		scores[i] = score

	scores = np.divide(scores, 7) #normalize

	scores_lst = []

	for j in range(len(svd_sorted)):
		snack, _ = svd_sorted[j]

		scores_lst.append((snack, round(float(scores[j,:]),2)))


	scores_lst.sort(key=lambda tup: tup[1], reverse=True)

	base_url = 'https://www.amazon.com/dp/'

	def avg_rating(snack):
		ratings_lst = ratings[titles_to_asin[snack]]
		average_rating = sum(ratings_lst) / len(ratings_lst)
		return round(average_rating,2)

	scored_filtered_lst = [(snack_name, otherDict[snack_name], base_url + titles_to_asin[snack_name], snack_score, imagesDict[snack_name], avg_rating(snack_name), otherDict[snack_name], sortingInput, matched_str[snack_name]) for (snack_name, snack_score) in scores_lst]

	return json.dumps(scored_filtered_lst)

end_time = time.time()
time_elapsed = end_time - start_time
print("Time Elapsed:", time_elapsed, "seconds")
