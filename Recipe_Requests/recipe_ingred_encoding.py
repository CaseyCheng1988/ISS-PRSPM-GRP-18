from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import json
import pandas as pd

with open('recipes_rated.json', 'r', encoding='utf-8') as f:
    recipes_train_json = json.load(f)

#get list of ingredients
ingredients = set()
recipes_ingred_list = []

for recipe in recipes_train_json:
    ingred_list = [item["Ingredient"] for item in recipe["Ingredients"]]
    recipes_ingred_list.append(ingred_list)
    for ingred in ingred_list:
        ingredients.add(ingred)

ingredients = list(ingredients)

ingredients.sort()
print(len(ingredients))
print(ingredients[0:10])
ingred_df = pd.DataFrame(ingredients)
ingred_df.to_csv("ingred_decode.csv")


values = np.array(ingredients)

label_encoder = LabelEncoder()

#gives a unique int value for each string ingredient, and saves the #mapping. you need that for the encoder. something like:
#['banana'] -> [1]
integer_encoded = label_encoder.fit_transform(values)
print(integer_encoded)

onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
print(integer_encoded)
#here you encode something like : [2] -> [0,1,0,0,...]
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded)
def transform_value(s):

    l = np.array([s])
    integer_encoded = label_encoder.transform(l)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.transform(integer_encoded)

    return onehot_encoded[0]

recipes_ingred_list_vec = []
counter = 1
for ingred_list in recipes_ingred_list:
    print("Working on recipe #" + str(counter))
    transformed_list = []
    for item in ingred_list:
        transformed_list.append(transform_value(item))

    results = transformed_list[0]
    for array in transformed_list: results = np.logical_or(results, array)
    recipes_ingred_list_vec.append(results.astype(np.int))
    counter = counter + 1

recipes_encoded_df = pd.DataFrame(recipes_ingred_list_vec)
print(recipes_encoded_df.shape)
recipes_encoded_df.to_csv("recipes_encoded.csv")
