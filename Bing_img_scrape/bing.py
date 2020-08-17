import requests, time, os, argparse
from datetime import datetime
from requests import exceptions
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import numpy as np

######################################################
############### ARGUMENT PARSER ######################
######################################################
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--key", required=True,
                help='API keys of Image Search API')
ap.add_argument("-q", "--query", required=True,
               help='search term for Bing Image API')
ap.add_argument("-t", "--total", type=int, required=True,
                help='total image to get')
ap.add_argument("-r", "--response", type=int, default=150,
               help="number of images per request")
ap.add_argument("-i", "--index", type=int, default=1,
               help='starting index of image')
args = vars(ap.parse_args())

######################################################
##################### VARIABLES ######################
######################################################

SUBSCRIPTION_KEY = args['key']
SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
SEARCH_TERM = args['query'] # specify search term here
IMG_PER_RESPONSE = args['response'] # number of images to return in one response, maximum 150
TOTAL_IMG = args['total'] # total number of images required
ITERATION = int(np.ceil(TOTAL_IMG/IMG_PER_RESPONSE)) # number of iterations
START_INDEX = args['index']
EXCEPTIONS = set([IOError, FileNotFoundError,
                 exceptions.RequestException, exceptions.HTTPError,
                 exceptions.ConnectionError, exceptions.Timeout])
CURRENT_TIME = datetime.now()

######################################################
########## REQUEST HEADER AND PARAMETERS #############
######################################################

headers = {"Ocp-Apim-Subscription-Key" : SUBSCRIPTION_KEY,}

params = {"q" : SEARCH_TERM,
         "count" : IMG_PER_RESPONSE,
          "safeSearch" : "strict",
          "imageType" : "photo",
          "license" : "share",
         }

######################################################
##################### FILE PATHS #####################
######################################################
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
IMG_DIR = os.path.join(BASE_DIR, SEARCH_TERM)
LOG_FILE = os.path.join(BASE_DIR, SEARCH_TERM + '.txt')

# create image directory if not exists
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# open log file, or create and open if not exists
log_file = open(LOG_FILE, 'w+')

######################################################
#################### LOGGING INFO ####################
######################################################
log_file.write("[INFO] Search term: {}\n".format(SEARCH_TERM))
log_file.write("[INFO] Search time: {}\n".format(CURRENT_TIME.strftime("%d/%m/%Y %a %I:%M:%S %p")))
log_file.write("[INFO] Start index: {}\n".format(START_INDEX))

######################################################
#################### MAKE REQUESTS ###################
######################################################
all_img_urls=[]
for iter in range(ITERATION):
    print("Starting request iteration: {}".format(iter))

    # set offset for request
    params['offset'] = iter * IMG_PER_RESPONSE

    # get API response
    response = requests.get(SEARCH_URL,
                           headers = headers,
                           params = params)

    # raise exceptions for bad request
    try:
        response.raise_for_status()
        print("Search request successful..")
        log_file.write("[INFO] Search successful at iteration {}.\n".format(iter))
    except Exception as e:
        if type(e) in EXCEPTIONS:
            print("Search request failed with {} at iteration {}.".format(str(e), iter))
            log_file.write("[ERROR] Search failed with {} at iteration {}.\n".format(str(e), iter))
            continue

    # get response as json object
    search_results = response.json()

    # get all urls from current request
    img_urls = [img['thumbnailUrl'] for img in search_results['value']]

    # add all current urls to the final list of urls
    all_img_urls += img_urls

    time.sleep(1) # pause 1 s

print("End of requests.")

########################################################
####################### SAVE IMAGES ####################
########################################################
index = START_INDEX
for url in all_img_urls:
    try:
        print("Fetching image from {} ...".format(url))
        log_file.write("[INFO] Fetching image from {}\n".format(url))
        # get response from image url
        response = requests.get(url, timeout=30)

        # get image from response
        img = Image.open(BytesIO(response.content))

        # set image path
        img_name = str(index) + '.jpg'
        img_path = os.path.join(IMG_DIR, img_name)

        # save image
        img.save(img_path)
        print("Saving image as {}".format(img_path))
        log_file.write("[INFO] Saving image at {}\n".format(img_path))

        index += 1

    except Exception as e:
        if type(e) in EXCEPTIONS:
            print("Error {} while fetching image: {}\n".format(str(e), url))
            print("Skipping image...")
            log_file.write("[ERROR] Fetching image {} failed with {}\n".format(url, str(e)))
            continue

log_file.write("[INFO] Total images saved: {}".format(index-START_INDEX))
log_file.close()
