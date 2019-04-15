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
# print(all_data)

with open("Data/title_to_index.pickle", "rb") as f:
	title_to_index = pickle.load(f)

with open("Data/titles_to_asin.pickle", "rb") as f:
	titles_to_asin = pickle.load(f)

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

@app.route('/filterLevels', methods=['POST'])
def filterLevels():
	fat =  request.form.get('fat');
	carb = request.form.get('carb');
	protein = request.form.get('protein');
	similarSnacks = request.form.get('similarSnacks');
	dumps = json.dumps({'status':'OK','fat':fat,'carb':carb,'protein':protein, 'similarSnacks':similarSnacks});
	return dumps;

@app.route('/filters', methods=['POST'])
def filters():
	pickle_in = open("Data/percentagesDict.pickle","rb");
	percentagesDict = pickle.load(pickle_in);
	fatLevel = request.form.get('fat');
	carbLevel = request.form.get('carb');
	proteinLevel = request.form.get('protein');
	query_snack = request.form.get('similarSnacks');

	filtered_snacks = {}
	# print(percentagesDict)
	# print('before filter')
	for product in percentagesDict.items():
		fat = product[1]["fat"]
		carb = product[1]["carb"]
		protein = product[1]["protein"]
		bool = True

		if (fatLevel == "Low" and fat > 0.0 and fat < 0.3) or (fatLevel == "Medium" and fat >= 0.3 and fat < 0.6) or (fatLevel == "High" and fat >= 0.6) or (fatLevel == "None"):
			bool = bool * True
		else:
			bool = bool * False
		if (carbLevel == "Low" and carb > 0.0 and carb < 0.1) or (carbLevel == "Medium" and carb >= 0.1 and carb < 0.2) or (carbLevel == "High" and carb >= 0.2) or (carbLevel == "None"):
			bool = bool * True
		else:
			bool = bool * False
		if (proteinLevel == "Low" and protein > 0.0 and protein < 0.2) or (proteinLevel == "Medium" and protein >= 0.2 and protein < 0.4) or (proteinLevel == "High" and protein >= 0.4) or (proteinLevel == "None"):
			bool = bool * True
		else:
			bool = bool * False
		if bool == True:
			filtered_snacks[product[0]] = product[1]
		# filteredDictTop10 = {k: finalDict[k] for k in list(finalDict)[:11]};
	# print('after filter')
	#START RANKING STUFF
	w1 = 1
	w2 = 1
	w3 = 1
	# print(all_data)
	# print('QUERY : ' + query_snack)
	# FIND SIM SNACK IF QUERY NOT IN DATABASE
	# print('snack sim')

	if query_snack not in list(all_data.keys()):
		all_titles = list(all_data.keys())
		all_titles.insert(0, query_snack)
		vectorizer=TfidfVectorizer()
		matrix=vectorizer.fit_transform(all_titles)
		cs=cosine_similarity(matrix[0], matrix)
		sorted_row = np.argsort(cs, axis=1)[0][::-1]
		query_snack = all_titles[sorted_row[1]]
	print('NEW QUERY : ' + query_snack)
	# SVD
	# print(filtered_snacks)
	# print('svd')
	data_lst = [(request, all_data[request]['description']) for request in filtered_snacks.keys()]
	print(len(data_lst))
	if len(data_lst) == 0:
		print('RETURN')
		return json.dumps([])
	data_lst.append((query_snack, all_data[query_snack]['description']))
	vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .7)
	my_matrix = vectorizer.fit_transform([x[1] for x in data_lst]).transpose()
	# print('SHAPE :' + str(my_matrix.shape))
	# print('usv')
	# u, s, v_trans = svds(my_matrix, k=len(data_lst)-1)

	if len(data_lst) <= 10:
		does_cooccur = snack in all_data[query_snack]['also_bought']
		# rating = all_data[snack]['rating']
		rating = 0
		score = w1*does_cooccur + w2*rating

		scores_lst.append((snack, score))
		scores_lst.sort(key=lambda tup: tup[1], reverse=True)
		return json.dumps([(snack_name, percentagesDict[snack_name]) for (snack_name, snack_score) in scores_lst])

	if len(data_lst) < 20:
		words_compressed, _, docs_compressed = svds(my_matrix, k=len(data_lst)-1)
	else:
		words_compressed, _, docs_compressed = svds(my_matrix, k=20)
	# print('after calc')
	docs_compressed = docs_compressed.transpose()
	word_to_index = vectorizer.vocabulary_
	words_compressed = normalize(words_compressed, axis = 1)
	docs_compressed = normalize(docs_compressed, axis = 1)
	curr_title_to_index = {tup[0] : index for index,tup in enumerate(data_lst)}
	snack_index_in = curr_title_to_index[query_snack]

	sims = docs_compressed.dot(docs_compressed[snack_index_in,:])
	asort = np.argsort(-sims)
	# print('svd sort')
	svd_sorted = [(data_lst[i][0],sims[i]/sims[asort[0]]) for i in asort[1:]]

	#Return sorted list of sim scores
	# print('sort')
	scores_lst = []

	for snack, svd_score in svd_sorted:
		does_cooccur = snack in all_data[query_snack]['also_bought']
		# rating = all_data[snack]['rating']
		rating = 0
		score = w1*does_cooccur + w2*rating + w3*svd_score

		scores_lst.append((snack, score))
		scores_lst.sort(key=lambda tup: tup[1], reverse=True)

	base_url = 'https://amazon.com/dp/'
	scored_filtered_lst = [(snack_name, percentagesDict[snack_name], base_url + titles_to_asin[snack_name]) for (snack_name, snack_score) in scores_lst]
	print(scored_filtered_lst)
	# print('finish')
	return json.dumps(scored_filtered_lst)

end_time = time.time()
time_elapsed = end_time - start_time
print("Time Elapsed:", time_elapsed, "seconds")
