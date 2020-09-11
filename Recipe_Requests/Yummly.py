# req_recipe scrapes links from website's search function and scraps out recipe details from recipe websites
# Yummly seem to have a max of 500 recipes per search

import requests
import bs4
import re
import time
import json

class Yummly:

    def __init__(self, ingredients):
        self.top10RecipeURLs = []
        self.top10Recipes = []
        self.ingredients = ingredients
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }

        self.top10RecipeURLs = self._getRecipeURLs(10)[1:]
        self._getTop10Recipe()

    def _scrapeURL(self, start, maxResult):
        url_prefix_Yum = r'https://mapi.yummly.com/mapi/v18/content/search?solr.seo_boost=new'
        url_postfix_Yum = f'&ignore-taste-pref%3F=true&start={start}&maxResult={maxResult}&fetchUserCollections=false&allowedContent=single_recipe&allowedContent=suggested_search&allowedContent=related_search&allowedContent=article&allowedContent=video&allowedContent=generic_cta&exp_sspop_enable=true&guided-search=true&solr.view_type=search_internal'
        url_main_ingre_Yum = r'&q='
        url_add_ingre_Yum = r'&allowedIngredient='
        num_ingre = len(self.ingredients)
        if num_ingre == 0:
            print("No ingredients found")
        else:
            url = url_prefix_Yum
            for i in range(1, num_ingre):
                url = url + url_add_ingre_Yum + self.ingredients[i]
            url = url + url_main_ingre_Yum + self.ingredients[0] + url_postfix_Yum

        return url

    def _getRecipeURLs(self, num_recipes):
        recipe_links = []
        maxResult = 10
        i = 2
        while i < num_recipes:
            url = self._scrapeURL(i, maxResult)
            print(url)
            reqs = requests.get(url, self.headers)
            print(reqs)
            if reqs.status_code == 200:
                soup = bs4.BeautifulSoup(reqs.content, features="lxml")
                for link in re.findall('(?<=")(https:\/\/www.yummly.com/recipe.*?)(?=")', str(soup)): recipe_links.append(link)
                i = i + maxResult
            else:
                url = self._scrapeURL(i, int(maxResult/2))
                print(url)
                reqs = requests.get(url, headers)
                print(reqs)
                if reqs.status_code == 200:
                    soup = bs4.BeautifulSoup(reqs.content, features="lxml")
                    for link in re.findall('(?<=")(https:\/\/www.yummly.com/recipe.*?)(?=")', str(soup)): recipe_links.append(link)
                print("Error in site request")
                break

        recipe_links = list(dict.fromkeys(recipe_links))

        return recipe_links

    def _getHTMLText(self, soup, tag, tagClass):
        try:
            return soup.find(tag, class_=tagClass).get_text().replace(u'\xa0', "").rstrip()
        except:
            return ""

    def _getInstructions(self, url, soup):
        try:
            html = soup.find_all("a", class_="read-dir-btn btn-primary wrapper recipe-summary-full-directions p1-text")
            for line in html:
                instructions = line.get("href")
            if instructions == "#directions": instructions = url + instructions
        except:
            instructions = ""
        return instructions

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

        recipe["Link"] = url

        return recipe

    def _getTop10Recipe(self):
        for link in self.top10RecipeURLs:
            self.top10Recipes.append(self._getRecipe(link))

if __name__ == '__main__':
    ingredients = ["beef", "orange", "garlic"]
    yum = Yummly(ingredients)

    recipe_filenm = ingredients[0]
    for i in range(1, len(ingredients)):
        recipe_filenm = recipe_filenm + "_" + ingredients[i]
    recipe_filenm = recipe_filenm + '_recipes.json'
    with open(recipe_filenm, 'w', encoding='utf-8') as f:
        json.dump(yum.top10Recipes, f, ensure_ascii=False, indent=4)
    print("Number of URLs found from Yummly: " + str(len(yum.top10RecipeURLs)))
