import Yummly
import os
import json
import itertools
import sys

cuisineList = ["american", "asian", "barbeque-bbq", "cajun", "chinese",
                "cuban", "english", "french", "german", "greek",
                "hawaiian", "hungarian", "indian", "irish", "italian",
                "japanese", "kid-friendly", "mediterranean", "mexican", "moroccan"
                "portuguese", "southern", "southwestern", "spanish", "swedish"
                "thai"]

ingredientList = ["steak", "salmon", "chicken", "broccoli", "cabbage","carrot",
                   "celery", "corn", "cucumber", "eggplant", "green bean", "green pepper",
                   "olive", "onion", "potato", "spinach", "tomato", "apple",
                   "avocado", "banana", "lemon", "bread", "cheese", "mushroom",
                   "egg"]

# cuisineList = ["american", "asian"]
#
# ingredientList = ["steak", "salmon"]

if __name__ == '__main__':
    ingredientSearchList = []
    count = 0
    for i in range(1, 3):
        for item in list(itertools.combinations(ingredientList, i)):
            ingredientSearchList.append(item)
            # print(str(count) + ". " + str(item))
            # count = count + 1
    print("Total combination: " + str(len(ingredientSearchList)))
    start = int(input("Start: "))
    end = int(input("End: "))
    ingredientSearchList = ingredientSearchList[start:end]
    for item in ingredientSearchList: print(item)
    for itemList in ingredientSearchList:
        ingredients = []
        for ingredient in itemList:
            ingredients.append(ingredient)
        print("Scrapping information for ")
        print(ingredients)
        print(".............")

        recipe_filenm = ingredients[0]
        for i in range(1, len(ingredients)):
            recipe_filenm = recipe_filenm + "_" + ingredients[i]
        if not os.path.exists("recipes"): os.makedirs("recipes")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        recipe_filenm = os.path.join(dir_path, "recipes", recipe_filenm + '_recipes.json')

        for cuisine in cuisineList:
            yum = Yummly.Yummly(ingredients, cuisine)
            recipes = yum._getRecipeList(40)

            if not os.path.exists(recipe_filenm):
                with open(recipe_filenm, 'w', encoding='utf-8') as f:
                    json.dump(recipes, f, ensure_ascii=False, indent=4)
            else:
                with open(recipe_filenm, 'r', encoding='utf-8') as f:
                    recipes_cur = json.load(f)
                for item in recipes:
                    if item not in recipes_cur:
                        recipes_cur.append(item)
                with open(recipe_filenm, 'w', encoding='utf-8') as f:
                    json.dump(recipes_cur, f, ensure_ascii=False, indent=4)

            print("Number of URLs found from Yummly: " + str(len(recipes)))
