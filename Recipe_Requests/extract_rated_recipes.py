import json
import time

start_time = time.localtime()
print("Start time: " + str(start_time))

comb_recipe_filenm = "recipes.json"
noDup_recipe_filenm = "recipes_noDup.json"
rated_recipe_filenm ="recipes_rated.json"

with open(noDup_recipe_filenm, 'r', encoding='utf-8') as f:
    recipes = json.load(f)
print(len(recipes))

print("Data loaded... Extracting rated recipes")
res_list = []
ratings = {}
for item in recipes:
    rating = item["Rating"]
    if rating == "":
        continue
    elif float(rating) > 3:
        res_list.append(item)
        if rating in ratings:
            ratings[rating] = ratings[rating] + 1
        else:
            ratings[rating] = 1

print(len(res_list))
for key, value in ratings.items():
    print ("% f : % d"%(key, value))




with open(rated_recipe_filenm, 'w', encoding='utf-8') as f:
    json.dump(res_list, f, ensure_ascii=False, indent=4)

end_time = time.localtime()
print("Start time: " + str(end_time))
