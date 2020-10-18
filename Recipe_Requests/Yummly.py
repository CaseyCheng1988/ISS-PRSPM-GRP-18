# req_recipe scrapes links from website's search function and scraps out recipe details from recipe websites
# Yummly seem to have a max of 500 recipes per search

import requests,concurrent.futures,bs4,re,time,os,sys,copy

dir_main = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(dir_main, "ProjectModel_Ingredients"))

import MapIngred
import OneHotEncodeIngred as OHEIngred
import IngrePredict

start=time.perf_counter()
recipeList = []

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
        self.MODEL_PATH = os.path.join(dir_main, "ProjectModel_Ingredients", "codefull.hdf5")

        self.mapIng = MapIngred.MapIngred()
        self.encoder = OHEIngred.OneHotEncodeIngred(label_encoder = self.LABEL_ENCODER, onehot_encoder = self.ONEHOT_ENCODER)
        self.predictor = IngrePredict.IngrePredict(model_path = self.MODEL_PATH)


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

        recipeList.append(recipe)

    ############################## THIS SECTION IS FOR METHODS TO RETRIEVE INFOMATION FROM RETRIEVED LIST ###################################################
    # Gets the recipes based on the URLs found
    def _getRecipeList(self, numSearch):

        recipeURLs = self._getRecipeURLs(numSearch)[1:]
        #####multithreading from recipeURLs list#####################
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._getRecipe, recipeURLs)

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

    # Checks whether ingredient exists in recipe and addtional ingredient list
    def _checkDuplicateIngred(self, recipe, ingred):
        # print([d["Ingredient"] for d in recipe["Ingredients"]])
        if ingred in [d["Ingredient"] for d in recipe["Ingredients"]]: return True
        return False

    # Combines the additional ingredients into the recipe with dummy amount and unit
    def _combineAddIngred(self, recipe):
        for item in self.recommendedIngred:
            ingred_temp = {}
            ingred_temp["Ingredient"] = item
            ingred_temp["Amount"] = ""
            ingred_temp["Unit"] = ""
            recipe["Ingredients"].append(ingred_temp)
        return recipe["Ingredients"]

    # Runs prediction model to predict the additional ingredient to recommend
    def _recommendIngred(self):
        recipeList = copy.deepcopy(self.top10Recipes)
        recipeName = self.selectedRecipeName

        for recipe in recipeList:
            if recipe["Name"] == recipeName:

                print("Mapping ingredients into broader categories for prediction...")
                recipe["Ingredients"] = self.mapIng._mapRecipeIngred(recipe)
                recipe["Ingredients"] = self._combineAddIngred(recipe)

                print("Converting ingredient list to one hot encoded vector...")
                recipeIngred_encode = self.encoder._encodeRecipe(recipe)

                print("Prediction ongoing...")
                predicted_class = self.predictor._predict_inputs(inputs = recipeIngred_encode)[0]

                print("Mapping prediction to ingredient class...")
                recommendIngred = self.encoder._decodeIngred(predicted_class)

                print("Predicted ingredient: " + recommendIngred)

                if self._checkDuplicateIngred(recipe, recommendIngred):
                    print("Ingredient already present. Will not add to list")
                else:
                    self.recommendedIngred.append(recommendIngred)
                break

    # Extract and form text of ingredients and instructions link based on input recipe name
    # Includes the running of the prediction function to generate the additional ingredient
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

                self.selectedRecipeName = recipeName
                return text
        return "Unable to find recipe name."

    # Returns the recommended additional ingredient to be added
    def _getRecommendedIngred(self):
        return self.recommendedIngred


if __name__ == '__main__':
    ingredients = ["Banana","Chicken",'Potato']
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

    for item in yum.top10RecipesName:
        print(item)
    finish=time.perf_counter()
    chosenRecipe = input("Please choose recipe from above list: ")
    print(yum._getRecipeText(chosenRecipe))
    yum._recommendIngred()
    print(yum.recommendedIngred)
    yum._recommendIngred()
    print(yum.recommendedIngred)
    print(f'Finished in {round(finish-start,2)}second(s)')
