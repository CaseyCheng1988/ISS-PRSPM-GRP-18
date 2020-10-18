# Map ingredients from specific names to categories that was manually labelled
import pandas as pd
import json

class MapIngred:

    def __init__(self):
        self.ingredMap_filename = "ingred_decode_label.xlsx"
        self._getIngredMap()

    # Function to get the ingedient map and load into the class
    def _getIngredMap(self):
        self.map = pd.read_excel(self.ingredMap_filename, index_col=0)
        # print(self.map)

    # Does the actual mapping of ingredient based on category in "General Category" column
    def _mapIngredient(self, ingredient):
        try:
            label = self.map.loc[self.map["Ingredients"] == ingredient, "General Category"].iloc[0]
        except:
            label = ""
        return label

    # Inputs a recipe and returns a recipe with mapped ingredients
    def _mapRecipeIngred(self, recipe):
        temp_ingred = []
        for item in recipe["Ingredients"]:
            mapped_ingred = self._mapIngredient(item["Ingredient"])
            if mapped_ingred == "" or pd.isna(mapped_ingred):
                continue
            else:
                item["Ingredient"] = mapped_ingred
                temp_ingred.append(item)
        return temp_ingred



if __name__ == '__main__':
    recipe_filename = "recipes_rated.json"
    recipeMapped_filename = "recipes_mapped_2.json"

    with open(recipe_filename, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    mapIng = MapIngred()

    counter = 1
    mapped_recipes = []
    for recipe in recipes:
        print("Encoding ingredients for recipe #" + str(counter))
        recipe["Ingredients"] = mapIng._mapRecipeIngred(recipe)
        mapped_recipes.append(recipe)
        counter = counter + 1

    print(len(mapped_recipes))
    with open(recipeMapped_filename, 'w', encoding='utf-8') as f:
        json.dump(mapped_recipes, f, ensure_ascii=False, indent=4)
