# Datasets
- **recipes folder** - individual queries for recipes from Yummly
- **recipes.json** - raw dataset from Yummly before processing
- **recipes_mapped.json** - processed and categorized recipe dataset (used to extract data for modelling)
- **recipes_input.csv** - one hot encoded input for modelling
- **recipes_output.csv** - one hot encoded output for modelling

# Recipe Requests

This folder consists of codes that are used to complete 2 main tasks:
1) Parse ingredients received from user image recognition module into Yummly website to retrieve list of recipes, convert into proper data structure and pushes back to user interface

2) Based on user selected recipe, map the ingredients and one hot encode them before parsing into additional ingredient recommendation model. Predictions are decoded and push back to user interface

## Yummly Class

Yummly.py consists of the main class that runs the core of the functions after receiving the ingredients list of interest from the user interface.


## Preparing Data Set for Ingredient Recommender Neural Network
Flow to prepare the dataset used for training the neural network:
1) Scrap recipes containing the 25 ingredients from Yummly, and filtering out recipes rated 3.5 stars and above (Total 6700+ recipes -> recipes_rated.json)
    1) **yummly_db_build.py** - main query script to run in parallel with multiple filters
    2) **combine_recipes.py** - combine multiple queries into a single big recipe list
    3) **remove_dup_recipes.py** - remove duplicate recipes that were queried
    4) **extract_rated_recipes.py** - filter out recipes with 3.5 stars and above

2) OneHotEncodeIngred.py is used in training mode to generate list of unique ingredients (Total 5000 ingredients - ingred_decode_label.xlsx)

3) Manual labelling of ingredients to broad category (5000 unique ingredients -> 600 labels)
    1) MapIngred.py uses this label map (ingred_decode_label.xlsx) to map ingredients from recipes to broad labels before being parsed into the model

4) OneHotEncodeIngred.py is used again in training mode to generate Label and One Hot encoders to one hot encode inputs. Mapping is stored as "label_encoder.pkl" and "onehot_encoder.pkl". These files are used in encode/decode mode to translate ingredients
    1) This also generates the one hot encoded recipe list together with other information such as prep time, cuisine etc. (recipes_encoded_rate_cuisine.csv)

5) Finally, generate_ingred_predict_dataset.py is used to iterate through each recipe in the dataset, omitting one ingredient at a time, to generate the input (recipes_input.csv) and output (recipes_output.csv) of the training dataset to be used in the NN model.

