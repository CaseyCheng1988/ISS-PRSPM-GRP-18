# One Hot encoding script for ingredients
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import json
import pandas as pd
import pickle
import os
import sys

class OneHotEncodeIngred:

    # Class initializer. There are 2 modes: Training & Encode/Decode. Mode depends on whether user inputs paths to encoder
    def __init__(self, label_encoder = None, onehot_encoder = None):
        if label_encoder == None or onehot_encoder == None:
            print("No encoder maps detected... Going into training mode...")
            self.recipesTrain_filename = "recipes_mapped.json"

            self.ingredients = set()

            self._loadTrainData()
            self._extractInfo()
            self._oneHotEncodeTrain()
        elif not os.path.isfile(label_encoder) or not os.path.isfile(onehot_encoder):
            print("Unable to find indicated encoder maps... Exiting...")
            sys.exit()
        else:
            print("Encoder maps detected! Going into encode decode mode...")
            self.label_encoder = pickle.load(open(label_encoder, 'rb'))
            self.onehot_encoder = pickle.load(open(onehot_encoder, 'rb'))



    ################## Generic Functions to Extract Info from Recipes ###################
    def _getIngreds(self, recipe):
        return [item["Ingredient"] for item in recipe["Ingredients"]]

    def _getPrepTime(self, recipe):
        prep_time = recipe["CookingTime"]["Value"]
        prep_time_unit = recipe["CookingTime"]["Unit"]
        if prep_time != "":
            if prep_time_unit == "Seconds":
                prep_time = int(prep_time) / 60
            elif prep_time_unit == "Hours":
                prep_time = int(prep_time) * 60
            else:
                prep_time = int(prep_time)
        return prep_time

    def _getRating(self, recipe):
        return recipe["Rating"]

    def _getCuisine(self, recipe):
        return recipe["Cuisine"]


    ################## Functions to Generate Map for One Hot Encoding ###################
    def _loadTrainData(self):
        with open(self.recipesTrain_filename, 'r', encoding='utf-8') as f:
            self.recipesTrain = json.load(f)

    def _extractInfo(self):
        for recipe in self.recipesTrain:
            ingred_list = self._getIngreds(recipe)
            for ingred in ingred_list:
                if ingred == None: print(recipe["Name"])
                self.ingredients.add(ingred)

        self.ingredients = list(self.ingredients)

        # print(len(self.ingredients))
        # print(self.ingredients[0:10])
        self.ingredients.sort()
        # print(len(self.ingredients))
        # print(self.ingredients[0:10])

    def _saveIngredDecode(self):
        ingred_df = pd.DataFrame(self.ingredients)
        ingred_df.to_csv("ingred_decode.csv")

    def _oneHotEncodeTrain(self):
        values = np.array(self.ingredients)
        self.label_encoder = LabelEncoder()

        #gives a unique int value for each string ingredient, and saves the #mapping. you need that for the encoder. something like:
        #['banana'] -> [1]
        integer_encoded = self.label_encoder.fit_transform(values)
        print(integer_encoded)

        self.onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        print(integer_encoded)
        #here you encode something like : [2] -> [0,1,0,0,...]
        onehot_encoded = self.onehot_encoder.fit_transform(integer_encoded)
        print(onehot_encoded)

        pickle.dump(self.label_encoder, open('label_encoder.pkl', 'wb'))
        pickle.dump(self.onehot_encoder, open('onehot_encoder.pkl', 'wb'))

        self._saveIngredDecode()

    ################## Functions to One Hot encode recipes ###############################
    def _transform_value(self, s):
        l = np.array([s])
        integer_encoded = self.label_encoder.transform(l)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        onehot_encoded = self.onehot_encoder.transform(integer_encoded)

        return onehot_encoded[0]

    def _encodeRecipe(self, recipe):
        ingred_list = self._getIngreds(recipe)
        transformed_list = []
        for item in ingred_list:
            transformed_list.append(self._transform_value(item))

        results = transformed_list[0]
        for array in transformed_list: results = np.logical_or(results, array)
        return results

    ########################## Decoding function back to ingred ##########################
    def _decodeIngred(self, array):
        array = [array]
        integer_encoded = self.onehot_encoder.inverse_transform(array)
        integer_encoded = integer_encoded.reshape(1, len(integer_encoded))
        print(integer_encoded)
        ingred = self.label_encoder.inverse_transform(integer_encoded.ravel())

        return ingred[0]


if __name__ == '__main__':
    ########################## Training and encode code #############################
    # recipeList_filename = "recipes_mapped.json"
    #
    # with open(recipeList_filename, 'r', encoding='utf-8') as f:
    #     recipeList = json.load(f)

    # encoder = OneHotEncodeIngred()

    # recipes_ingred_list_vec = []
    # prep_time_list = []
    # rating_list = []
    # cuisine_list = []
    # counter = 1
    # for recipe in recipeList:
    #     print("Working on recipe #" + str(counter))
    #     results = encoder._encodeRecipe(recipe)
    #     recipes_ingred_list_vec.append(results.astype(np.int))
    #
    #     prep_time_list.append(encoder._getPrepTime(recipe))
    #     rating_list.append(encoder._getRating(recipe))
    #     cuisine_list.append(encoder._getCuisine(recipe))
    #     counter = counter + 1
    #
    # recipes_encoded_df = pd.DataFrame(recipes_ingred_list_vec)
    # recipes_encoded_df["prep time"] = prep_time_list
    # recipes_encoded_df["rating"] = rating_list
    # recipes_encoded_df["cuisine"] = cuisine_list
    # print(recipes_encoded_df.shape)
    # recipes_encoded_df.to_csv("recipes_mapped_encoded.csv")


    ################################## Decode code ##################################
    encoder = OneHotEncodeIngred("label_encoder.pkl", "onehot_encoder.pkl")

    ingred_list = pd.read_csv("recipes_output.csv", index_col = 0)
    print(ingred_list.iloc[3].values)
    print(encoder._decodeIngred(ingred_list.iloc[3].values))
