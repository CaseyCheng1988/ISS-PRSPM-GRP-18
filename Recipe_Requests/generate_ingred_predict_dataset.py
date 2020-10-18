import pandas as pd
import json

def generatePermuation(list):
    input = []
    output = []
    input_row = []
    total_ingred = len(list)
    output_row = [0] * total_ingred

    for i in range(total_ingred):
        if list[i] == 1:
            input_row = []
            for item in list: input_row.append(item)
            output_row = [0] * total_ingred
            input_row[i] = 0
            output_row[i] = 1
            input.append(input_row)
            output.append(output_row)

    return input, output

recipe_filename = "recipes_mapped_encoded.csv"
input_filename = "recipes_input.csv"
output_filename = "recipes_output.csv"

recipes = pd.read_csv(recipe_filename, index_col = 0)
recipes = recipes.drop("prep time", axis = 1)
recipes = recipes.drop("rating", axis = 1)
recipes = recipes.drop("cuisine", axis = 1)

header = list(recipes.columns.values)

input_final = []
output_final = []
input_final_df = pd.DataFrame(columns = header)
output_final_df = pd.DataFrame(columns = header)

print(recipes.head())

for i in range(recipes.shape[0]):
    print("Generating dataset for recipe #" + str(i))
    input, output = generatePermuation(recipes[i:i+1].values.tolist()[0])
    for item in input: input_final.append(item)
    for item in output: output_final.append(item)

input_final_df = pd.DataFrame(input_final, columns = header)
output_final_df = pd.DataFrame(output_final, columns = header)

print(input_final_df.head())
print(input_final_df.shape)
print(output_final_df.head())
print(output_final_df.shape)

input_final_df.to_csv(input_filename)
output_final_df.to_csv(output_filename)
