######################################
#MapIngred
######################################
# Map ingredients from specific names to categories that was manually labelled
import pandas as pd
import json,gc
requestSuggestion=[]
Suggestion=[]
z=[]
class MapIngred:

    def __init__(self):
        self.ingredMap_filename = "ingred_decode_label.xlsx"
        self._getIngredMap()
        gc.collect()

    # Function to get the ingedient map and load into the class
    def _getIngredMap(self):
        self.map = pd.read_excel(self.ingredMap_filename, index_col=0)
        gc.collect()
        # print(self.map)

    # Does the actual mapping of ingredient based on category in "General Category" column
    def _mapIngredient(self, ingredient):
        try:
            label = self.map.loc[self.map["Ingredients"] == ingredient, "General Category"].iloc[0]
        except:
            label = ""
        gc.collect()
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
        gc.collect()
        return temp_ingred

# req_recipe scrapes links from website's search function and scraps out recipe details from recipe websites
# Yummly seem to have a max of 500 recipes per search
#####################################################
#OneHotEncode
###################################################
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
        gc.collect()



    ################## Generic Functions to Extract Info from Recipes ###################
    def _getIngreds(self, recipe):
        gc.collect()
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
        gc.collect()
        return prep_time

    def _getRating(self, recipe):
        return recipe["Rating"]

    def _getCuisine(self, recipe):
        return recipe["Cuisine"]


    ################## Functions to Generate Map for One Hot Encoding ###################
    def _loadTrainData(self):
        with open(self.recipesTrain_filename, 'r', encoding='utf-8') as f:
            self.recipesTrain = json.load(f)
            gc.collect()

    def _extractInfo(self):
        for recipe in self.recipesTrain:
            ingred_list = self._getIngreds(recipe)
            for ingred in ingred_list:
                if ingred == None: print(recipe["Name"])
                self.ingredients.add(ingred)
        gc.collect()

        self.ingredients = list(self.ingredients)

        # print(len(self.ingredients))
        # print(self.ingredients[0:10])
        self.ingredients.sort()
        # print(len(self.ingredients))
        # print(self.ingredients[0:10])

    def _saveIngredDecode(self):
        ingred_df = pd.DataFrame(self.ingredients)
        ingred_df.to_csv("ingred_decode.csv")
        gc.collect()

    def _oneHotEncodeTrain(self):
        values = np.array(self.ingredients)
        self.label_encoder = LabelEncoder()
        gc.collect()

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
        gc.collect()
        self._saveIngredDecode()

    ################## Functions to One Hot encode recipes ###############################
    def _transform_value(self, s):
        l = np.array([s])
        integer_encoded = self.label_encoder.transform(l)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        onehot_encoded = self.onehot_encoder.transform(integer_encoded)
        gc.collect()
        return onehot_encoded[0]

    def _encodeRecipe(self, recipe):
        ingred_list = self._getIngreds(recipe)
        print(ingred_list)
        transformed_list = []
        for item in ingred_list:
            transformed_list.append(self._transform_value(item))

        results = transformed_list[0]
        for array in transformed_list: results = np.logical_or(results, array)
        gc.collect()
        return results

    ########################## Decoding function back to ingred ##########################
    def _decodeIngred(self, array):
        array = [array]
        integer_encoded = self.onehot_encoder.inverse_transform(array)
        integer_encoded = integer_encoded.reshape(1, len(integer_encoded))
        print(integer_encoded)
        ingred = self.label_encoder.inverse_transform(integer_encoded.ravel())
        gc.collect()
        return ingred[0]

#############################################
#IngrePredict
#########################################
from tensorflow.keras.models import load_model
import numpy as np

class IngrePredict:
    def __init__(self, model_path=None, inputs=None):
        if model_path is not None:
            self.model_path = model_path
        else:
            self.model_path = None

        if inputs is not None:
            self.inputs = self._correct_inputs_dim(inputs)
            self.num_classes = self.inputs.shape[1]
        else:
            self.inputs = None
            self.num_classes = None
        gc.collect()

    def _correct_inputs_dim(self, inputs):
        # make sure inputs array is 2-dimensional:
        if inputs.ndim == 1:
            inputs = np.reshape(inputs, (1, -1))
        elif (inputs.ndim < 1) or (inputs.ndim > 2):
            raise Exception('Inputs array must be either one or two-dimensional array.')
        gc.collect()
        return inputs

    def _set_modelpath(self, model_path):
        gc.collect()
        self.model_path = model_path

    def _set_inputs(self, inputs):
        self.inputs = self._correct_inputs_dim(inputs)
        self.num_classes = self.inputs.shape[1]
        gc.collect()

    def _check_num_classes(self, model, inputs):
        if model.input.shape.as_list()[1] == inputs.shape[1]:
            return True
        else:
            return False
        gc.collect()

    def _one_hot_encode(self, predicted_class):
        row = len(predicted_class)
        one_hot_prediction = np.zeros((row, self.num_classes), dtype=np.int8)
        for i in range(len(predicted_class)):
            one_hot_prediction[i, predicted_class[i]] = 1
        gc.collect()
        return one_hot_prediction


    def _predict_inputs(self, model_path=None, inputs=None):
        if model_path is not None:
            print('I am here 1')
            self._set_modelpath(self, model_path)

        if inputs is not None:
            print('I am here 2')
            self._set_inputs(inputs)

        if self.inputs is None:
            raise Exception("Inputs array is missing for prediction.")

        if self.model_path is None:
            raise Exception("Model is missing for prediction.")

        model = load_model(self.model_path)
        if not (self._check_num_classes(model, self.inputs)):
            raise Exception("Total classes of inputs array does not tally with model input dimension.")

        predict_probability = model.predict(self.inputs)
        predict_class = np.argmax(predict_probability, axis=1)
        gc.collect()
        return self._one_hot_encode(predict_class)



# req_recipe scrapes links from website's search function and scraps out recipe details from recipe websites
# Yummly seem to have a max of 500 recipes per search

import requests,bs4,re,time,os,sys,copy

dir_main = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(dir_main, "ProjectModel_Ingredients"))

#import MapIngred
#import OneHotEncodeIngred as OHEIngred
#import IngrePredict

start=time.perf_counter()
recipeList = []
folderpath = os.path.abspath(os.getcwd())
model_folderpath = os.path.join(folderpath, 'ProjectModel_Ingredients')
modelname = 'codefull'
class Yummly:

    # Yummly class by default will initiate a top 10 relevant search and pull from Yummly
    # This information can be called from top10Recipes list
    def __init__(self, ingredients, cuisine=""):
        self.top10RecipeURLs = []
        self.top10RecipesName = []
        self.ingredients = [item.lower() for item in ingredients]
        self.cuisine = cuisine
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }
        self.top10Recipes = self._getRecipeList(10)[:10]
        self.top10RecipeURLs = self._getRecipeURLList(self.top10Recipes)
        self.top10RecipesName = self._getRecipeNameList(self.top10Recipes)

        self.selectedRecipeName = ""
        self.recommendedIngred = []

        self.LABEL_ENCODER = "label_encoder.pkl"
        self.ONEHOT_ENCODER = "onehot_encoder.pkl"
        self.MODEL_PATH = os.path.join(model_folderpath, modelname+'.hdf5')

        self.mapIng = MapIngred()
        self.encoder = OneHotEncodeIngred(label_encoder = self.LABEL_ENCODER, onehot_encoder = self.ONEHOT_ENCODER)
        self.predictor = IngrePredict(model_path = self.MODEL_PATH)


    ############################## THIS SECTION IS FOR RETRIEVING RECIPE URLS FROM SEARCH ###################################################
    # This function is to generate the scraping URL based on the input ingredients and returning to the request function to scrap information
    def _scrapeURL(self, start, maxResult, URLOption):
        url_prefix_Yum = r'https://mapi.yummly.com/mapi/v18/content/search?solr.seo_boost=new'
        if URLOption == 0:
            url_postfix_Yum = f'&ignore-taste-pref%3F=true&start={start}&maxResult={maxResult}&fetchUserCollections=false&allowedContent=single_recipe&allowedContent=suggested_search&allowedContent=related_search&allowedContent=article&allowedContent=video&allowedContent=generic_cta&exp_sspop_enable=true&guided-search=true&solr.view_type=search_internal'
        else:
            url_postfix_Yum = f'&ignore-taste-pref%3F=true&start={start}&maxResult={maxResult}&fetchUserCollections=false&allowedContent=single_recipe&allowedContent=suggested_search&allowedContent=related_search&allowedContent=article&allowedContent=video&allowedContent=generic_cta&guided-search=true&solr.view_type=search_internal'
        url_main_ingre_Yum = r'&q='
        url_add_ingre_Yum = r'&allowedIngredient='
        url_cuisine_Yum = r'&allowedCuisine=cuisine%5Ecuisine-'
        num_ingre = len(self.ingredients)
        num_cuisine = len(self.cuisine)
        if num_ingre == 0:
            print("No ingredients found")
        else:
            url = url_prefix_Yum
            for i in range(1, num_ingre):
                url = url + url_add_ingre_Yum + self.ingredients[i]
            if num_cuisine != 0: url = url + url_cuisine_Yum + self.cuisine
            url = url + url_main_ingre_Yum + self.ingredients[0] + url_postfix_Yum
        #gc.collect()
        return url

    # Actual function to scrap recipe urls from Yummly
    # Links are generated based from _scrapeURL function
    # Number of recipes can be searched in multiples of 10
    def _getRecipeURLs(self, num_recipes):
        check = 0
        recipe_cnt = 0
        recipe_links = []
        maxResult = 10
        i = 2
        URLOption = 0
        while len(recipe_links) < num_recipes:
            if check == 2 and URLOption == 0:
                URLOption = 1
                check = 0
            url = self._scrapeURL(i, maxResult, URLOption)
            print(url)
            reqs = requests.get(url, self.headers)
            print(reqs)
            if reqs.status_code == 200:
                soup = bs4.BeautifulSoup(reqs.content, features="lxml")
                for link in re.findall('(?<=")(https:\/\/www.yummly.com/recipe.*?)(?=")', str(soup)):
                    recipe_links.append(link)
                i = i + maxResult
            else:
                url = self._scrapeURL(i, int(maxResult/2), URLOption)
                print(url)
                reqs = requests.get(url, self.headers)
                print(reqs)
                if reqs.status_code == 200:
                    soup = bs4.BeautifulSoup(reqs.content, features="lxml")
                    for link in re.findall('(?<=")(https:\/\/www.yummly.com/recipe.*?)(?=")', str(soup)): recipe_links.append(link)
                    recipe_links = list(dict.fromkeys(recipe_links))
                print("Error in site request")
                break
            recipe_links = list(dict.fromkeys(recipe_links))

            if recipe_cnt == len(recipe_links):
                check = check + 1
                if check == 3:
                    print("No increase in new recipes, exiting loop...")
                    break
            else:
                check = 0
            recipe_cnt = len(recipe_links)
            print(recipe_cnt)
        gc.collect()
        return recipe_links

    ############################## THIS SECTION IS FOR RETRIEVING RECIPE DETAILS FROM RECIPE URLS ###################################################
    # Simple scrapping function to full out text from certain tag and class search in bs4
    def _getHTMLText(self, soup, tag, tagClass):
        #gc.collect()
        try:
            return soup.find(tag, class_=tagClass).get_text().replace(u'\xa0', "").rstrip()
        except:
            return ""

    # Search for the buttom in Yummly to find link to recipe instructions
    def _getInstructions(self, url, soup):
        try:
            html = soup.find_all("a", class_="read-dir-btn btn-primary wrapper recipe-summary-full-directions p1-text")
            for line in html:
                instructions = line.get("href")
            if instructions == "#directions": instructions = url + instructions
        except:
            instructions = ""
        #gc.collect()
        return instructions

    # Search for review stars and capture rating of recipe
    def _getRating(self, soup):
        try:
            rating_html = soup.find("a", class_="recipe-details-rating p2-text primary-orange")
            full_star = rating_html.find_all("span", class_="icon full-star y-icon")
            rating = len(full_star)
            if len(rating_html.find_all("span", class_="icon half-star y-icon")) != 0: rating = rating + 0.5
        except:
            rating = ""
        #gc.collect()
        return rating


    # Gets a list of information about the recipe from Yummly
    # Using bs4 to scrap through the source code for specific terms and HTML tags
    # This part is catered only to Yummly
    def _getRecipe(self, url):
        reqs = requests.get(url, self.headers)
        print(reqs)
        soup = bs4.BeautifulSoup(reqs.content, features="html.parser")
        recipe = {}
        recipe["Name"] = self._getHTMLText(soup, "h1", "recipe-title font-bold h2-text primary-dark")
        recipe["CookingTime"] = {}
        recipe["Ingredients"] = []
        recipe["CookingTime"]["Value"] = self._getHTMLText(soup.find("div", class_="recipe-summary-item unit h2-text"), "span", "value font-light h2-text")
        recipe["CookingTime"]["Unit"] = self._getHTMLText(soup.find("div", class_="recipe-summary-item unit h2-text"), "span", "unit font-normal p3-text")

        for tag in soup.find_all("div", class_="add-ingredient show-add"):
            ingredient = {
                "Ingredient": self._getHTMLText(tag, "span", "ingredient"),
                "Amount": self._getHTMLText(tag, "span", "amount"),
                "Unit": self._getHTMLText(tag, "span", "unit")
            }
            recipe["Ingredients"].append(ingredient)

        recipe["Instructions"] = self._getInstructions(url, soup)
        recipe["Rating"] = self._getRating(soup)
        recipe["Cuisine"] = self.cuisine
        recipe["Link"] = url
        #gc.collect()
        return recipe

    # Gets the recipes based on the URLs found
    def _getRecipeList(self, numSearch):
        recipeList = []
        recipeURLs = self._getRecipeURLs(numSearch)[1:]
        i = 1
        for link in recipeURLs:
            print("Extracting recipe from Link " + str(i) + " out of " + str(len(recipeURLs)))
            recipeList.append(self._getRecipe(link))
            i = i + 1
        gc.collect()
        return recipeList

    def _getRecipeNameList(self, recipeList):
        namelist = []
        for recipe in recipeList: namelist.append(recipe["Name"])
        #gc.collect()
        return namelist

    def _getRecipeURLList(self, recipeList):
        URLlist = []
        for recipe in recipeList: URLlist.append(recipe["Link"])
        #gc.collect()
        return URLlist

    def _getIngredient(self, item):
        ingredient = item["Ingredient"]
        amount = item["Amount"]
        unit = item["Unit"]
        #gc.collect()
        if unit == "":
            if amount == "":
                return ingredient
            else:
                return amount + " " + ingredient
        else:
            return amount + " " + unit + " of " + ingredient

    # Checks whether ingredient exists in recipe and addtional ingredient list
    def _checkDuplicateIngred(self, recipe, ingred):
        gc.collect()
        # print([d["Ingredient"] for d in recipe["Ingredients"]])
        if ingred in [d["Ingredient"] for d in recipe["Ingredients"]]: return True
        return False

    # Combines the additional ingredients into the recipe with dummy amount and unit
    def _combineAddIngred(self, recipe):
        self.recommendedIngred.extend(requestSuggestion)
        for item in self.recommendedIngred:
            ingred_temp = {}
            ingred_temp["Ingredient"] = item
            ingred_temp["Amount"] = ""
            ingred_temp["Unit"] = ""
            recipe["Ingredients"].append(ingred_temp)
        gc.collect()
        return recipe["Ingredients"]

    # Runs prediction model to predict the additional ingredient to recommend
    def _recommendIngred(self):
        recipeList = copy.deepcopy(self.top10Recipes)
        recipeName = self.selectedRecipeName
        warning=''
        for recipe in recipeList:
            if recipe["Name"] == recipeName:

                print("Mapping ingredients into broader categories for prediction...")
                recipe["Ingredients"] = self.mapIng._mapRecipeIngred(recipe)
                recipe["Ingredients"] = self._combineAddIngred(recipe)

                print("Converting ingredient list to one hot encoded vector...")
                try:
                    recipeIngred_encode = self.encoder._encodeRecipe(recipe)
                except Exception:
                    junk=requestSuggestion[0]
                    self.recommendedIngred.remove(junk)
                    return junk+' cannot be encoded, thus it will be remove from the list'

                print("Prediction ongoing...")
                predicted_class = self.predictor._predict_inputs(inputs = recipeIngred_encode)[0]

                print("Mapping prediction to ingredient class...")
                recommendIngred = self.encoder._decodeIngred(predicted_class)

                print("Predicted ingredient: " + recommendIngred)

                if self._checkDuplicateIngred(recipe, recommendIngred):
                    warning ='The ingredients model is predicting '+recommendIngred+" but it is already present. So will not add to list"+". If you want to add ingredients manually, pls type like for eg,'extend banana'"
                else:
                    self.recommendedIngred.append(recommendIngred)
                gc.collect()
                return warning

    # Extract and form text of ingredients and instructions link based on input recipe name
    # Includes the running of the prediction function to generate the additional ingredient
    def _getRecipeText(self, recipeName, recipeList = []):
        gc.collect()
        if len(recipeList) == 0: recipeList = self.top10Recipes
        text = ""
        for recipe in recipeList:
            if recipe["Name"] == recipeName:
                text = text + "Name: " + recipeName
                text = text + "\nIngredients:"
                num = 1
                for item in recipe["Ingredients"]:
                    text = text + "\n" + str(num) + ". " + self._getIngredient(item)
                    num = num + 1
                text = text + "\nCooking Instructions: " + recipe["Link"]

                self.selectedRecipeName = recipeName
                return text
        return "Unable to find recipe name."

    # Returns the recommended additional ingredient to be added
    def _getRecommendedIngred(self):
        return self.recommendedIngred


def main(ingredients):
    gc.collect()
    recipeList.clear()
    #gc.enable()
    gc.collect()
    #ingredients = ["beef"]
    # cuisine = ""
    # cuisine = "american"

    yum = Yummly(ingredients)
    # recipes = yum._getRecipeList(500)
    recipes = yum.top10Recipes
    # print(yum.top10RecipesName)

    # recipe_filenm = ingredients[0]
    # for i in range(1, len(ingredients)):
    #     recipe_filenm = recipe_filenm + "_" + ingredients[i]
    # if not os.path.exists("recipes"): os.makedirs("recipes")
    # recipe_filenm = "recipes/" + recipe_filenm + '_recipes.json'
    # with open(recipe_filenm, 'w', encoding='utf-8') as f:
    #     json.dump(recipes, f, ensure_ascii=False, indent=4)
    print("Number of URLs found from Yummly: " + str(len(recipes)))
    return yum.top10RecipesName,yum


def getRecipe(yum,chosenRecipe):
    gc.collect()
    details=yum._getRecipeText(chosenRecipe)
    Suggestion,warning=getRecommend(yum)
    return details,Suggestion,warning

def getRecommend(yum):
    gc.collect()
    warning=yum._recommendIngred()
    return yum.recommendedIngred,warning

###########################################################
#MODEL FUNCTION
###########################################################

import numpy as np
import gc
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras import optimizers
from tensorflow.keras import regularizers
#gc.enable()
gc.collect()

class Prediction_Model:

	CONST = {'IMG_HEIGHT' : 256,
	         'IMG_WIDTH'  : 256,
	         'THRESHOLD'  : 0.5,
			 "NONE" 	  : 'None'}

	CLASS_LABELS = 	{0 : 'Apple',
					 1 : 'Avocado',
					 2 : 'Banana',
					 3 : 'BeanSprout',
					 4 : 'Beef',
					 5 : 'Bread',
					 6 : 'Broccoli',
					 7 : 'Cabbage',
					 8 : 'Carrot',
					 9 : 'Celery',
					 10: 'Cheese',
					 11: 'Chicken',
					 12: 'Corn',
					 13: 'Cucumber',
					 14: 'Egg',
					 15: 'Eggplant',
					 16: 'GreenBean',
					 17: 'Lemon',
					 18: 'Mushroom',
					 19: 'Olive',
					 20: 'Onion',
					 21: 'Potato',
					 22: 'Salmon',
					 23: 'Spinach',
					 24: 'Tomato'}


	learning_rate = 0.0005
	optmz       = optimizers.RMSprop(lr=learning_rate)
	num_classes = 25

	def __init__(self, model_path):
		Prediction_Model.pred_model = Prediction_Model.createModel()
		Prediction_Model.model_path = model_path

	def createModel():

	    xin = Input(shape=(256,256,3))
	    x = Rescaling(1./255) (xin)

	    x = Conv2D(64,(3,3),activation=None, padding='same')(x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(32,(3,3),activation=None, padding='same')(x)
	    x = BatchNormalization() (x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(32,(3,3),activation=None, padding='same')(x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(64,(3,3),activation=None, padding='same', kernel_regularizer=regularizers.l2(0.001))(x)
	    x = BatchNormalization() (x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(128,(3,3),activation=None, padding='same', kernel_regularizer=regularizers.l2(0.001))(x)
	    x = BatchNormalization() (x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Flatten() (x)
	    x = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)) (x)
	    x = Dropout(0.5) (x)
	    x = Dense(Prediction_Model.num_classes, activation='softmax') (x)


	    pred_model = Model(inputs=xin,outputs=x)
	    pred_model.compile(loss='categorical_crossentropy',
	                  optimizer=Prediction_Model.optmz,
	                  metrics=['categorical_accuracy'])

	    return pred_model


	def predict_image(self, image_path):

	    PIL_img = load_img(
	        image_path,
	        color_mode = 'rgb',
	        target_size = (Prediction_Model.CONST['IMG_HEIGHT'], Prediction_Model.CONST['IMG_WIDTH']))

	    ARR_img = img_to_array(PIL_img)
	    ARR_img = np.expand_dims(ARR_img, axis=0)

	    Prediction_Model.pred_model.load_weights(Prediction_Model.model_path)
	    Prediction_Model.pred_model.compile(loss='categorical_crossentropy',
	        optimizer=Prediction_Model.optmz,
	        metrics=['categorical_accuracy'])


	    predicts    = Prediction_Model.pred_model.predict(ARR_img)
	    #print (predicts)
	    print (max(predicts[0]))
	    if max(predicts[0]) >= Prediction_Model.CONST['THRESHOLD']:
	    	predout = Prediction_Model.CLASS_LABELS[int(np.argmax(predicts, axis=1))]
	    else:
	    	predout = Prediction_Model.CONST['NONE']
	    return predout



def model():
	import os, pathlib

	folderpath = os.path.abspath(os.getcwd())
	model_folderpath = os.path.join(folderpath, 'model')
	prediction_folderpath = os.path.join(folderpath)

	modelname = 'Food_Classification_Gen25'                                           #Model Name to be loaded
	model_path = os.path.join(model_folderpath, modelname+'.hdf5')                     #Model Path to be loaded
	print(f"Model Path is: {model_path}")

	image_path = os.path.join(prediction_folderpath, 'telegram_image.jpg')           #Image Path to be predicted
	print(f"Image Path is: {image_path}")



	#Step 1: Initalise Prediction_Model Class with model_path
	Pred_Model = Prediction_Model(model_path)

	#Step 2: predict_image by passing in image_path of the image

	return Pred_Model.predict_image(image_path)



###########################################################
#TELEGRAM FUNCTION
###########################################################

from io import BytesIO
import gc
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters, InlineQueryHandler, CallbackQueryHandler
#from telegram.ext import Updater,MessageHandler,Filters
from telegram.ext.dispatcher import run_async
import time,threading,multiprocessing
#from webhook_remover import webhook_remover
TOKEN='1209854585:AAHC9A4awhi0lqjYnI7r_qkEyctq_p2xyAQ'
ingredients=[]
yummly=[]

def YummlyToString(yummly,string):
    i=len(yummly)-1
    prev_y=''
    while i>-1:
        y=str(i+1)+'. '+yummly[i]+'\n'+prev_y
        prev_y=y
        i-=1
        y=('Yummly suggestions for '+string+':\n'+
            y+'\n'+'Pls confirm which recipe to pick?'
            +'\n'+'For eg, if want recipe 1, pls reply just "1".')
    gc.collect()
    return y

def IngredientsToString(ingredients):
    i=len(ingredients)-1
    prev_y=''
    while i>-1:
        y=str(i+1)+'. '+ingredients[i]+'\n'+prev_y
        prev_y=y
        i-=1
        y=("ingredients list:\n"+
            y+"\nIn case this ingredient is wrong, pls type the command along with the respective ingredients list number."+
            "\n\n*Like for eg,if ingredients number 1 is wrong, just type 'del 1' to delete number 1 ingredient"+
            "\n*Like for eg, if ingredients number 1 is wrong want to swap it with banana, just type 'edit 1,banana' to swap the respective ingredients"+
            "\n*If manual input is needed, like for eg; want to add in banana, just press 'add banana' "
            +"\n\n***If ingredients list is correct and enough, pls reply 'done' once it is confirmed."+
            '\n***If ingredients list is not enough, pls continue to upload the photos'
           )
    gc.collect()
    return y

def SuggestionToString(Suggestion):
    if len(Suggestion) == 0:
        return ''
    i=len(Suggestion)-1
    prev_sugstring=''
    sugstring=''
    while i>-1:
        sugstring='\n-'+Suggestion[i]+prev_sugstring
        i-=1
        prev_sugstring=sugstring
    return 'CookWhatAh recommends adding the following ingredients to spice things up:'+sugstring

def Yummlymessage(yummly,update):
    try:
        if len(yummly)>0:
            replies=int(update.message.text)
            if replies>0:
                RecipeName=yummly[replies-1]
                return RecipeName
    except Exception:
        pass

def yummlyTransfer(ingredients,update):
        #main target for yummly function
        #ingredients list/array to input to yummly main function
        #from yummly, it should output standard strings
        yummly,yum = main(ingredients)
        string=convert_list_to_string(ingredients,',')
        print(yummly)
        if yummly!=[] and yummly[0]!='':
                print(yummly)
                y=YummlyToString(yummly,string)
                print(y)
                update.message.reply_text(y)
                ingredients.clear()

        elif yummly==[] or yummly[0]=='':
            update.message.reply_text("don't have such combination/recipe for "+string)
            remove_ingredients=ingredients[len(ingredients)-1]

            update.message.reply_text('due to invalid combination,'+remove_ingredients+' is removed.')
            ingredients.remove(remove_ingredients)
            y,yummly,yum=yummlyTransfer(ingredients,update)

        del string

        return y,yummly,yum

def delete(i,ingredient_num):
    if len(ingredients)!=0:
        try:
            i+=1
            return ingredients[ingredient_num-i]
        except Exception:
            delete(i,ingredient_num)
    elif y.find('Yummly suggestions')==-1:
        return "ingredient is not added in , pls send ingredients photo here"

def message(update,context):
    #gc.enable()
    gc.collect()
    global yummly,yum,y,ingredients,manual,suggestion,RecipeName,sug_string,z,x

    if update.message.text.upper().find('EXTEND')>-1 and len(z)>0:
        #print(getRecommend(yum))

        update.message.reply_text('Pls wait ah!, we will suggest more to you shortly')
        user=update.message.text.lower().replace('extend','')
        try:
            if user[0]==' ':
                user=user[1:]
        except Exception:
            pass
        if user!='':
            print(user)
            requestSuggestion.append(user)
        manual_ingred=convert_list_to_string(requestSuggestion,',')
        if manual_ingred!='':
                print('you have added '+manual_ingred)
                update.message.reply_text('you have added '+manual_ingred)
        Suggestion,warning=getRecommend(yum)
        suggestion=SuggestionToString(Suggestion)

        print(suggestion)
        if suggestion != '': update.message.reply_text(suggestion)
        if warning!='':
                update.message.reply_text(warning)
        requestSuggestion.clear()



    elif update.message.text.upper().find('EXTEND')>-1 and len(z)==0:
        update.message.reply_text('what to extend ah! invalid command')

    #below is the detect the integer from user, so that to match the recipe name
    if Yummlymessage(yummly,update)!=None:
        if z==[]:
            z.append('1')
        update.message.reply_text('retrieving recipe!Please wait ah')
        RecipeName=Yummlymessage(yummly,update)
        details,Suggestion,warning=getRecipe(yum,RecipeName)
        print(details)
        sugestion=SuggestionToString(Suggestion)
        print(sugestion)
        update.message.reply_text(details)
        if warning != '':
            update.message.reply_text(warning)
        else:
            update.message.reply_text(sugestion)
        #update.message.reply_text('we suggest you add '+suggestion+' to make it more tasty.')

    if update.message.text.upper().find('DEL')>-1:
        z.clear()
        ingredient_num=int(update.message.text.upper().replace('DEL',''))
        print(ingredient_num)
        temp=delete(0,ingredient_num)
        print(temp)
        update.message.reply_text(temp+' is removed')
        ingredients.remove(temp)
        print(ingredients)
        try:
            ingredients_string=IngredientsToString(ingredients)
            print(ingredients_string)
            update.message.reply_text(ingredients_string)
        except Exception:
            pass
        del ingredient_num,temp

    if update.message.text.upper().find('EDIT')>-1:
            z.clear()
            manual=str(update.message.text)
            first=manual.split(',')[0]
            second=manual.split(',')[1]
            ingredient_num=int(first.upper().replace('EDIT',''))
            print(manual)

            print(ingredient_num)
            temp=delete(0,ingredient_num)
            print(temp)
            update.message.reply_text(temp+' is removed')
            ingredients.remove(temp)
            temp=second.lower().replace(' ','')
            if temp!='':
                ingredients.append(temp)
                print(ingredients)
            try:
                ingredients_string=IngredientsToString(ingredients)
                update.message.reply_text(ingredients_string)
            except Exception:
                pass
            del temp,first,second,ingredient_num

    if update.message.text.upper().find('ADD')>-1:
            z.clear()
            temp=update.message.text.upper().replace('ADD','').replace(' ','')
            if temp!='':
                ingredients.append(temp.lower())

            try:
                ingredients_string=IngredientsToString(ingredients)
                update.message.reply_text(ingredients_string)
            except Exception:
                pass
            del temp

    #Type 'to yummly' in telegram danielthx account
    #and it will activate yummly function
    if update.message.text.upper().find('DONE')>-1:
        z.clear()
        update.message.reply_text('transfering to yummly')

        try:
            if ingredients!=[]:
                y,yummly,yum=yummlyTransfer(ingredients,update)

            elif y.find('Yummly suggestions')>-1:
                temp="ingredients has been transferred to yummly, now pls type 'recipe'."
                print(temp)
                update.message.reply_text(temp)
        except Exception:
            if ingredients==[]:
                y="ingredient is not added in , pls send ingredients photo here"
                print(y)
                update.message.reply_text(y)
            else:
                pass
            del temp
    try:
        if update.message.text.upper().find('RECIPE')>-1:
            print(y)
            update.message.reply_text(y)
    except Exception:
        print('no recipe yet')
        update.message.reply_text('no recipe yet')


    if update.message.text.upper().find('HELP')>-1:
        instruction=("*reply 'recipe' is to get show all the suggested top 10 recipes from Yummly"+
              "\n*reply 'done' is to retrieve the recipes from yummly"+
              "\n*reply for eg 'edit 1,banana' will swap the ingredients item number 1 with banana"+
              "\n*reply for eg 'add banana' will just add the ingredients list with banana"+
              "\n*reply for eg 'del 1' will just delete the ingredients item number 1 in ingredients list"
              "\n*reply 'extend' is to extend the suggestion from ingredient suggestor"
              "\n*if you want to add ingredients manually in the ingredients model, pls type like for eg,'extend banana'"
              )
        print(instruction)
        update.message.reply_text(instruction)
        update.message.bot.send_photo(update.message.chat.id,open('Photo_Standard.jpg','rb'))

def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)

def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

def receive_image(update,context):
    z.clear()
    #gc.enable()
    gc.collect()
    global ingredients,string
    try:
        update.message.reply_text("wait ah, it's still downloading")
        recipeList.clear()
        obj=context.bot.getFile(file_id=update.message.photo[-1].file_id)
        f =  BytesIO(obj.download_as_bytearray())
        write_bytesio_to_file('telegram_image.jpg', f)

        label=model().lower()
        print(label)
        if label!='none':

            if label not in ingredients:
                ingredients.append(label)
            string=convert_list_to_string(ingredients,',')
            print(ingredients)


            update.message.reply_text(string+
                                  " are in ingredients list.\n"+
                                  "If want to add in more ingredient , pls upload the photo.\n"
                                  )
            ingredients_string=IngredientsToString(ingredients)
            update.message.reply_text(ingredients_string)
            del f,obj,label
        else:
            update.message.reply_text("Pls retake the photo again")
            update.message.bot.send_photo(update.message.chat.id,open('Photo_Standard.jpg','rb'))


    except Exception as e:
        print(str(e))
        receive_image(update,context)


def command_handling_fn(update,context):
    update.message.reply_text('Welcome to CookWhatAh')
    update.message.reply_text("you can start upload your photos or press 'help' to guide through this bot")
    update.message.bot.send_photo(update.message.chat.id,open('Photo_Standard.jpg','rb'))

def telegramBot(TOKEN):
    #gc.enable()
    gc.collect()
    updater=Updater(token=TOKEN,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',command_handling_fn))
    dp.add_handler(MessageHandler(Filters.text,message))
    dp.add_handler(MessageHandler(Filters.photo,receive_image))
    updater.start_polling()
    updater.idle()


telegramBot(TOKEN)
