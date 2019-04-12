import pickle
import time

start_time = time.time()

pickle_in = open("Data/FINAL_snacks_data.pickle","rb")
AllFoodsDict = pickle.load(pickle_in)

def percentages(AllFoodsDict):
"""This function calculates the percentages in each snack that correspond to
carbs, fats, and proteins. These values are stored in a dictionary
(pickled in file: percentagesDict.pickle)
"""
    AllFoodsDictCopy = dict(AllFoodsDict)
    print(AllFoodsDictCopy["Salba Smart Organic White Corn Tortilla Chips"]['nutrients'])

    fat = 0.0
    carb = 0.0
    protein = 0.0
    percentages = {}
    fat_to_cal = 9
    carb_to_cal = 4
    protein_to_cal = 4

    for product in AllFoodsDictCopy.items():
        calories = 0.0
        fat = 0.0
        carb = 0.0
        protein = 0.0
        for t in product[1]['nutrients'].items():
            if t[0] == "calories":
                calories = t[1]
            if t[0] == "fat":
                fat = t[1]
            elif t[0] == "carbohydrates":
                carb = t[1]
            elif t[0] == "protein":
                protein = t[1]
        if calories != 0.0:
            fatPercentage = (fat * fat_to_cal)/calories
            carbPercentage = (carb * carb_to_cal)/calories
            proteinPercentage = (protein * protein_to_cal)/calories
        else:
            fatPercentage = 0.0
            carbPercentage = 0.0
            proteinPercentage = 0.0
        percentages[product[0]] = {"fat": fatPercentage, "carb": carbPercentage, "protein": proteinPercentage}

        # Snacks where percentages sum up to more than 1.0
        if fatPercentage+carbPercentage+proteinPercentage > 1.0:
            print(fatPercentage+carbPercentage+proteinPercentage, product[0], percentages[product[0]])

    return percentages

percentagesDict = percentages(AllFoodsDict)
# print(percentagesDict["Salba Smart Organic White Corn Tortilla Chips"])
# print(percentagesDict)

pickle_out = open("Data/percentagesDict.pickle","wb")
pickle.dump(percentagesDict, pickle_out)
pickle_out.close()

end_time = time.time()
time_elapsed = end_time - start_time
print("Time Elapsed:", time_elapsed, "seconds")
