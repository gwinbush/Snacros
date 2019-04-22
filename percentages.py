import pickle
import time

start_time = time.time()
imagesDict = {}

pickle_in = open("Data/FINAL_snacks_data.pickle","rb")
AllFoodsDict = pickle.load(pickle_in)

with open('Data/fixed_filtered_snacks_withURLs.pickle', 'rb') as f:
	withURLs = pickle.load(f)

for p in withURLs:
     imagesDict[p] = withURLs[p]

def percentages(AllFoodsDict):
	""" This function calculates the percentages in each snack that correspond to
	carbs, fats, and proteins. These values are stored in a dictionary
	(pickled in file: percentagesDict.pickle) """

	AllFoodsDictCopy = dict(AllFoodsDict)
	# print(AllFoodsDictCopy["Roasted Salted Pepitas"]['nutrients'])

	percentages = {}
	fat_to_cal = 9
	carb_to_cal = 4
	protein_to_cal = 4

	for product_name, product in AllFoodsDictCopy.items():
		fat = product['nutrients']['fat'] * fat_to_cal
		carb = product['nutrients']['carbohydrates'] * carb_to_cal
		protein = product['nutrients']['protein'] * protein_to_cal
		calories = fat + carb + protein
		serving = product['nutrients']['serving']
		if calories != 0.0:
			fatPercentage = fat / calories
			carbPercentage = carb / calories
			proteinPercentage = protein / calories
		else:
			fatPercentage = 0.0
			carbPercentage = 0.0
			proteinPercentage = 0.0
		percentages[product_name] = {"fat": fatPercentage, "carb": carbPercentage, "protein": proteinPercentage, "calories": calories, "serving": serving}

		return percentages

def other(AllFoodsDict):
	AllFoodsDictCopy = dict(AllFoodsDict)

	fat_to_cal = 9
	carb_to_cal = 4
	protein_to_cal = 4
	info = {}

	for product_name, product in AllFoodsDictCopy.items():
		fatG = product['nutrients']['fat']
		fat = fatG * fat_to_cal
		carbG = product['nutrients']['carbohydrates']
		carb = carbG * carb_to_cal
		proteinG = product['nutrients']['protein']
		protein = proteinG * protein_to_cal
		# calories = fat + carb + protein
		calories = product['nutrients']['calories']
		serving = product['nutrients']['serving']
		description = product['description']
		price = product['price']

		info[product_name] = { "description": description, "calories": calories, "serving": serving, "fat": fatG, "carb": carbG, "protein": proteinG, "price": price}

	return info


percentagesDict = percentages(AllFoodsDict)
otherDict = other(AllFoodsDict)

# print(percentagesDict["Salba Smart Organic White Corn Tortilla Chips"])
# print(percentagesDict)

# pickle_out = open("Data/percentagesDict.pickle","wb")
# pickle.dump(percentagesDict, pickle_out)
# pickle_out.close()

pickle_out = open("Data/servingAndCalorieDict.pickle","wb")
pickle.dump(otherDict, pickle_out)
pickle_out.close()

# pickle_out = open("Data/imagesDict.pickle","wb")
# pickle.dump(imagesDict, pickle_out)
# pickle_out.close()

# end_time = time.time()
# time_elapsed = end_time - start_time
# print("Time Elapsed:", time_elapsed, "seconds")
