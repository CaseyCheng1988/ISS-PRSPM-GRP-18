import random
import os, csv

###############################################################
################### DIRECTORIES AND PATHS #####################
###############################################################
CURRENT_DIR = os.path.abspath(os.path.dirname('__file__'))
ROOT_DIR = os.path.abspath(os.path.dirname(CURRENT_DIR))
RECIPE_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'Recipe_Requests'))
ING_CODE_PATH = os.path.abspath(os.path.join(RECIPE_DIR, 'ingred_decode.csv'))
ING_DATA_PATH = os.path.abspath(os.path.join(RECIPE_DIR, 'recipes_encoded.csv' ))

###############################################################
#################### INGREDIENTS CODE DICTIONARY ##############
###############################################################
with open(ING_CODE_PATH, mode='r') as code_file:
    reader = csv.reader(code_file)
    ING_CODE_DICT = {int(row[0]) : row[1] for row in reader}

TOTAL_ING = len(ING_CODE_DICT)

###############################################################
####### GENERATE RANDOM LIST OF INGREDIENTS ###################
###############################################################
def generate_ingredients():
    # generate a random total of ingredients
    rand_total = random.randint(1, TOTAL_ING)

    # generate a random list of ingredients
    rand_code = random.sample(range(0, TOTAL_ING-1), rand_total)
    print(rand_code)
    rand_ing = [ING_CODE_DICT[i] for i in rand_code]

    return rand_ing

if __name__=='__main__':
    print(generate_ingredients())
