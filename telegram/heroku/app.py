# req_recipe scrapes links from website's search function and scraps out recipe details from recipe websites
# Yummly seem to have a max of 500 recipes per search

import requests
import bs4
import re

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
        self.top10Recipes = self._getRecipeList(10)
        self.top10RecipeURLs = self._getRecipeURLList(self.top10Recipes)
        self.top10RecipesName = self._getRecipeNameList(self.top10Recipes)

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
        return recipe_links


    ############################## THIS SECTION IS FOR RETRIEVING RECIPE DETAILS FROM RECIPE URLS ###################################################
    # Simple scrapping function to full out text from certain tag and class search in bs4
    def _getHTMLText(self, soup, tag, tagClass):
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

        return recipe

    ############################## THIS SECTION IS FOR METHODS TO RETRIEVE INFOMATION FROM RETRIEVED LIST ###################################################
    # Gets the recipes based on the URLs found
    def _getRecipeList(self, numSearch):
        recipeList = []
        recipeURLs = self._getRecipeURLs(numSearch)[1:]
        i = 1
        for link in recipeURLs:
            print("Extracting recipe from Link " + str(i) + " out of " + str(len(recipeURLs)))
            recipeList.append(self._getRecipe(link))
            i = i + 1
        return recipeList

    def _getRecipeNameList(self, recipeList):
        namelist = []
        for recipe in recipeList: namelist.append(recipe["Name"])
        return namelist

    def _getRecipeURLList(self, recipeList):
        URLlist = []
        for recipe in recipeList: URLlist.append(recipe["Link"])
        return URLlist

    def _getIngredient(self, item):
        ingredient = item["Ingredient"]
        amount = item["Amount"]
        unit = item["Unit"]
        if unit == "":
            if amount == "":
                return ingredient
            else:
                return amount + " " + ingredient
        else:
            return amount + " " + unit + " of " + ingredient

    # Extract and form text of ingredients and instructions link based on input recipe name
    def _getRecipeText(self, recipeName, recipeList = []):
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
                return text
        return "Unable to find recipe name."


def main(ingredients):
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
    #yum = Yummly(ingredients)
    return yum._getRecipeText(chosenRecipe)
   
import numpy as np

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


class Prediction_Model:

	CONST = {'IMG_HEIGHT' : 256,
	         'IMG_WIDTH'  : 256}

	CLASS_LABELS = {0 : 'Apple',
	                1 : 'Avocado',
	                2 : 'Banana',
	                3 : 'BeanSprout',
	                4 : 'Broccoli',
	                5 : 'Chicken',
	                6 : 'GreenBean',
	                7 : 'Potato',
	                8 : 'Salmon',
	                9 : 'Tomato'}

	learning_rate = 0.0005
	optmz       = optimizers.RMSprop(lr=learning_rate)
	num_classes = 10

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
	    predout     = Prediction_Model.CLASS_LABELS[int(np.argmax(predicts, axis=1))]
	    
	    return predout



def model():
	import os, pathlib
	folderpath = os.path.abspath(os.getcwd())
	model_folderpath = os.path.join(folderpath, 'model')
	prediction_folderpath = os.path.join(folderpath)

	modelname = 'Food_Classification_Gen10'                                           #Model Name to be loaded
	model_path = os.path.join(model_folderpath, modelname+'.hdf5')                     #Model Path to be loaded
	print(f"Model Path is: {model_path}")

	image_path = os.path.join(prediction_folderpath, 'telegram_image.jpg')           #Image Path to be predicted
	print(f"Image Path is: {image_path}")



	#Step 1: Initalise Prediction_Model Class with model_path
	Pred_Model = Prediction_Model(model_path)
    
	#Step 2: predict_image by passing in image_path of the image
    
	return Pred_Model.predict_image(image_path)
     
	#print(prediction)
    
 # -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:08:50 2020
@author: user
"""
# webhook_remover is needed to delete outside webhook from conflicting
#with the current connection, webhook conflict will occur every 15-30minutes
#so i have wrote a library called webhook_remover and used threading
# to delete the webhook every 10 second, threading module is needed
# so that it can run concurrently with the code

from io import BytesIO
#from Prediction_Model import model
from telegram.ext import Updater,MessageHandler,Filters




TOKEN='1239312494:AAGXEt22xKY9pF3DEyHrfG4nUGBsS4CXoHk'

tele_ingredients = []
yummly=[]
userOption=[]

def YummlyToString(yummly):
    i=len(yummly)-1
    prev_y=''
    while i>-1:
        y=str(i+1)+'. '+yummly[i]+'\n'+prev_y
        prev_y=y
        i-=1
    return 'Yummly suggestions:\n'+y

def Yummlymessage(yummly,update):
    try:
        if len(yummly)>0:
            replies=int(update.message.text)
            if replies>0:
                RecipeName=yummly[replies-1]
                return RecipeName
    except Exception:
        pass


def message(update,context):
    global yummly,yum,y

    #below is the detect the integer from user, so that to match the recipe name
    if Yummlymessage(yummly,update)!=None:
        userOption.append(Yummlymessage(yummly,update))
        update.message.reply_text(userOption)
        print(userOption)
        update.message.reply_text('Above is the user option\n'+
            'If decided to pick this recipe, pls reply "chosen yummly" to extract the details.\n'+
                                  'If got typo or want to clear user option, pls reply "clear user option"')
    print(update.message.text)

    #Type 'to yummly' in telegram danielthx account
    #and it will activate yummly function
    if update.message.text.upper().find('TO YUMMLY')>-1:
        update.message.reply_text('transfering to yummly')
        #ingredients=tele_ingredients.copy()
        ingredients = list(filter(None, tele_ingredients))
        print(ingredients)
        #main target for yummly function
        #ingredients list/array to input to yummly main function
        #from yummly, it should output standard strings
        yummly,yum = main(ingredients)
        try:
            y=YummlyToString(yummly)
            print(y)
        
            update.message.reply_text(y+'\n'+
                                  'Pls confirm which recipe to pick?'
                                  +'\n'+
                                  'For eg, if want recipe 1, pls reply just "1".')
        except Exception:
            y="don't have such combination/recipe"
            print(y)
            update.message.reply_text(y)

        tele_ingredients.clear()
        ingredients.clear()
        userOption.clear()

    if update.message.text.upper().find('CHOSEN YUMMLY')>-1:
        i=0
        while i<len(userOption):
            details=getRecipe(yum,userOption[i])
            print(details)
            update.message.reply_text(details)
            i+=1

    if update.message.text.upper().find('SHOW YUMMLY')>-1:
        print(y)
        update.message.reply_text(y)

    if update.message.text.upper().find('SHOW USER OPTION')>-1:
        print(userOption)
        update.message.reply_text(userOption)

    if update.message.text.upper().find('CLEAR USER OPTION')>-1:
        print('userOption list cleared')
        update.message.reply_text('userOption list cleared')
        userOption.clear()

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
    try:
        print('download in progress')
        update.message.reply_text('download in progress')
        obj=context.bot.getFile(file_id=update.message.photo[-1].file_id)
        f =  BytesIO(obj.download_as_bytearray())
        write_bytesio_to_file('telegram_image.jpg', f)
        update.message.reply_text('file has been downloaded')
        print('file has been downloaded')
        google_label=model()
        print(google_label)
        update.message.reply_text(google_label+
                                  " is added into into ingredients list.\n"+
                                  "If want to add in more ingredient , pls upload the photo.\n"
                                  "If ingredients enough, pls reply 'to yummly' once it is confirmed.")
        tele_ingredients.append(google_label)

    except Exception as e:
        print(str(e))
        receive_image(update,context)

def telegramBot(TOKEN):
    updater=Updater(token=TOKEN,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,message))
    dp.add_handler(MessageHandler(Filters.photo,receive_image))
    updater.start_polling()
    updater.idle()

telegramBot(TOKEN)

