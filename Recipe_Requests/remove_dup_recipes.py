import json
import time

start_time = time.localtime()
print("Start time: " + str(start_time))

comb_recipe_filenm = "recipes.json"
noDup_recipe_filenm = "recipes_noDup.json"

with open(noDup_recipe_filenm, 'r', encoding='utf-8') as f:
    recipes = json.load(f)
print(len(recipes))
links = [d['Link'] for d in recipes]
print(len(links))
links = list(dict.fromkeys(links))
print(len(links))

print("Data loaded... Removing duplicates")
res_list = []
for link in links:
    i = 0
    for i in range(len(recipes)):
        if recipes[i]["Link"] == link:
            res_list.append(recipes[i])
            break
        else:
            i = i + 1
print(len(res_list))

with open(noDup_recipe_filenm, 'w', encoding='utf-8') as f:
    json.dump(res_list, f, ensure_ascii=False, indent=4)

end_time = time.localtime()
print("Start time: " + str(end_time))
