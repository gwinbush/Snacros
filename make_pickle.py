import pickle
import json


#Load snack JSON file
with open('Data/data_with_nutrients.json') as json_file:
    data = json.load(json_file)

# Store data (pickle)
with open('Data/snack_data.pickle', 'wb') as file:
    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
