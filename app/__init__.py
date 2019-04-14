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

start_time = time.time()
# Configure app
socketio = SocketIO()
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
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
    return render_template('index.html')

@app.route('/filterLevels', methods=['POST'])
def filterLevels():
    fat =  request.form['fatContent'];
    carb = request.form['carbContent'];
    protein =  request.form['proteinContent'];
    similarSnacks = request.form['similarSnacks'];
    dumps = json.dumps({'status':'OK','fat':fat,'carb':carb,'protein':protein, 'similarSnacks':similarSnacks});
    return dumps;

@app.route('/filters', methods=['POST'])
def filters():
    pickle_in = open("Data/percentagesDict.pickle","rb");
    percentagesDict = pickle.load(pickle_in);
    fatLevel =  request.form['fatContent'];
    carbLevel = request.form['carbContent'];
    proteinLevel =  request.form['proteinContent'];
    finalDict = {}
    # print(percentagesDict)
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
            finalDict[product[0]] = product[1]
        filteredDictTop10 = {k: finalDict[k] for k in list(finalDict)[:11]};
    return json.dumps(filteredDictTop10);


end_time = time.time()
time_elapsed = end_time - start_time
print("Time Elapsed:", time_elapsed, "seconds")
