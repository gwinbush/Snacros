import json
from myfitnesspal import Client


client = Client("gabewinbush@gmail.com")

#Load snack data
with open('Data/FINAL_snacks_data.json') as json_file:
    data = json.load(json_file)

new_data = {}
length = len(data)
count = 1

#Loop through each product and retrieve nutrient info
for title, info in data.items():
    try:
        food_items = client.get_food_search_results(title)
        print("{} of {} items processed".format(count, length))
        count += 1
        if len(food_items) == 0:
            continue

        food_info = client.get_food_item_details(food_items[0].mfp_id)
        #print(type(food_info.confirmations))
        #break
        
        def encode(s):
            if s == None:
                return ""
            return s.encode('utf-8')

        nutrient_dict = {
            "mfp_id": food_info.mfp_id,
            "name": encode(food_info.name),
            "brand": encode(food_info.brand),
            "verified": food_info.verified,
            "serving": str(food_info.servings[0]).replace("x ", ""),
            "calories": food_info.calories,
            "calcium": food_info.calcium,
            "carbohydrates": food_info.carbohydrates,
            "cholesterol": food_info.cholesterol,
            "fat": food_info.fat,
            "fiber": food_info.fiber,
            "iron": food_info.iron,
            "monounsaturated_fat": food_info.monounsaturated_fat,
            "polyunsaturated_fat": food_info.polyunsaturated_fat,
            "potassium": food_info.potassium,
            "protein": food_info.protein,
            "saturated_fat": food_info.saturated_fat,
            "sodium": food_info.sodium,
            "sugar": food_info.sugar,
            "trans_fat": food_info.trans_fat,
            "vitamin_a": food_info.vitamin_a,
            "vitamin_c": food_info.vitamin_c,
            "confirmations": food_info.confirmations,
        }

        new_data[title] = info
        new_data[title]["nutrients"] = nutrient_dict
    except:
        continue

with open('Data/data_with_nutrients.json', 'w') as file:
    json.dump(new_data, file)
