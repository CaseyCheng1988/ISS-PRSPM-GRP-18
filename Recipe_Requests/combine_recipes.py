import glob2
import os
import json

json_filenm = glob2.glob(os.path.join("recipes", "*.json"))
comb_recipe_filenm = "recipes.json"

recipes_num = 0
recipes = []
for file in json_filenm:
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)

    print(file + ": " + str(len(data)))
    recipes_num = recipes_num + len(data)

    for item in data:
        # if item not in recipes:
        recipes.append(item)

# if not os.path.exists(comb_recipe_filenm):
#     with open(comb_recipe_filenm, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
# else:
#     with open(comb_recipe_filenm, 'r', encoding='utf-8') as f:
#         recipes = json.load(f)
#     for item in data:
#         # if item not in recipes:
#         recipes.append(item)
with open(comb_recipe_filenm, 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)

print("Total number of recipes: " + str(len(recipes)))
