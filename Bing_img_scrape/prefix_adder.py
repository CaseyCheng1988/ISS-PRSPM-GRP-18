import os, argparse

######################################################
############### ARGUMENT PARSER ######################
######################################################
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
                help='Directory Path of the Image Folder')
ap.add_argument("-p", "--prefix", required=True,
                help='Prefix to be added to filename')
args = vars(ap.parse_args())


######################################################
##################### VARIABLES ######################
######################################################
DIR_PATH = args['directory']
PREFIX = args['prefix']

######################################################
################### PREFIX EDITOR ####################
######################################################
os.chdir(DIR_PATH)
print(f"Directory Selected: {os.getcwd()}")

file_list = os.listdir()
print(f"Number of Images in file: {len(file_list)}")

for index, filename in  enumerate(os.listdir('.')):  #listdir('.') = current directory
	os.rename(filename, PREFIX+filename)