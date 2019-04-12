import pickle
import time

start_time = time.time()

pickle_in = open("Data/percentagesDict.pickle","rb")
percentagesDict = pickle.load(pickle_in)


def filters(percentagesDict, fatLevel = None, carbLevel = None, proteinLevel = None):
"""This function creates a dictionary based on the levels of each nutrient provided:
Low, Medium, High, and stores it in a dictionary (not pickled)
"""
    finalDict = {}

    for product in percentagesDict.items():
        fat = product[1]["fat"]
        carb = product[1]["carb"]
        protein = product[1]["protein"]
        bool = True

        if (fatLevel == "Low" and fat > 0.0 and fat < 0.3) or (fatLevel == "Medium" and fat >= 0.3 and fat < 0.6) or (fatLevel == "High" and fat >= 0.6) or (fatLevel == None):
            bool = bool * True

        else:
            bool = bool * False
        if (carbLevel == "Low" and carb > 0.0 and carb < 0.1) or (carbLevel == "Medium" and carb >= 0.1 and carb < 0.2) or (carbLevel == "High" and carb >= 0.2) or (carbLevel == None):
            bool = bool * True
        else:
            bool = bool * False
        if (proteinLevel == "Low" and protein > 0.0 and protein < 0.2) or (proteinLevel == "Medium" and protein >= 0.2 and protein < 0.4) or (proteinLevel == "High" and protein >= 0.4) or (proteinLevel == None):
            bool = bool * True
        else:
            bool = bool * False

        if bool == True:
            finalDict[product[0]] = product[1]
    return finalDict

filteredDict = filters(percentagesDict, fatLevel = None, carbLevel = None, proteinLevel = None) # Only put levels: "Low", "Medium", "High"

end_time = time.time()
time_elapsed = end_time - start_time
print("Time Elapsed:", time_elapsed, "seconds")
