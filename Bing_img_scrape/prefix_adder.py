import os, argparse, pathlib

######################################################
############### ARGUMENT PARSER ######################
######################################################
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
                help='Directory Path of the Image Folder')
ap.add_argument("-p", "--prefix", required=True,
                help='Prefix to be added to filename')
ap.add_argument("-r", "--rename", type=int, default = 1, required=False,
                help='Prefix to be added to filename')


args = vars(ap.parse_args())


######################################################
##################### VARIABLES ######################
######################################################
DIR_PATH = args['directory']
PREFIX = args['prefix']
TO_RENAME = args['rename']

######################################################
################### PREFIX EDITOR ####################
######################################################
os.chdir(DIR_PATH)
print(f"Directory Selected: {os.getcwd()}")

file_list = os.listdir()
print(f"Number of Images in file: {len(file_list)}")

print (TO_RENAME)

if TO_RENAME == 1:
	count = 1
	for index, filename in  enumerate(os.listdir('.')):
		suffix = pathlib.Path(filename).suffix
		os.rename(filename, PREFIX + '_' + str(count) + suffix)
		count = count + 1
	print(f"Files renamed with prefix, {PREFIX} ")

else:
	for index, filename in  enumerate(os.listdir('.')):  #listdir('.') = current directory
		os.rename(filename, PREFIX + filename)
	print(f"Prefix, {PREFIX}, added to filename ")