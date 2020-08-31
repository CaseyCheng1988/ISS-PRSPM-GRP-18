# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:43:20 2020
@author: user
"""
import time
import datetime
import sys
start=time.perf_counter()
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.chrome.options import Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
options = Options()
options.add_argument('start-maximized') #
browser=webdriver.Chrome('C://Users//profx//Documents//GitHub//ISS-PRSPM-GRP-18//chromedriver',options=options)
pg.FAILSAFE=True

####################################################################################################
############## THIS AREA NEEDS TO BE CUSTOMIZE ACCORDING TO YOUR SCREEN ############################
####################################################################################################

# REFER TO Coordinates_Explanation.jpg for visual explanation

ANCHOR_IMG_X_Y = (150,400)          # Location of anchor img
SPONSORED_OFFSET_Y = 350            # If there is a layer of sponsored links, offset in Y direction from anchor img

# Boundaries for your search screen
LEFT_BOUNDARY = 20
RIGHT_BOUNDARY = 1880
TOP_BOUNDARY = 115
BOTTOM_BOUNDARY = 990

# Number of points to click and save
# This is roughly the number of images that fits in a search screen
GRID_X = 7
GRID_Y = 4

# Calculating the offset between 2 click points based on number of points in the screen
IMAGE_OFFSET = (round((RIGHT_BOUNDARY-LEFT_BOUNDARY)/GRID_X), round((BOTTOM_BOUNDARY-TOP_BOUNDARY)/GRID_Y))

# Setting the offset from the edges
LEFT_OFFSET = LEFT_BOUNDARY+IMAGE_OFFSET[0]/2
TOP_OFFSET = TOP_BOUNDARY+IMAGE_OFFSET[1]/2

# Point on screen to scroll down
SCROLL_DOWN_X_Y = (1910, 973)

# Offset in case first point does not land on a savable image
SAVE_IMG_OFFSET = -50

# This the the size of the save image box when you right click an image
# This is used to set a bounding area to search for "save_image.jpg" to quicken the locateOnScreen process
SAVE_IMG_SIZE = (291, 306)

####################################################################################################
####################################################################################################
####################################################################################################

NUM_IMG = 0

def Nkey(N,key):
    i=0
    while i<N:
        pg.hotkey(key)
        i+=1

def imageDownload(X, Y, Object, tries = 0):
    global NUM_IMG
    pg.click(X, Y, button='right')
    for i in range(1, 10):
        z=pg.locateCenterOnScreen('save_image.jpg',confidence=0.8, region = (max(0, int(X) - SAVE_IMG_SIZE[0]), max(0, int(Y) - SAVE_IMG_SIZE[1]), SAVE_IMG_SIZE[0]*2, SAVE_IMG_SIZE[1]*2))
        if z != None: break
        time.sleep(0.1)

    if z == None:
        pg.hotkey('esc')
        if tries == 0:
            tries = tries + 1
            imageDownload(X, Y + SAVE_IMG_OFFSET, Object, tries)
    else:
        Nkey(5,'up')
        time.sleep(0.5)
        pg.hotkey('enter')
        pyperclip.copy(Object)
        for i in range(1, 40):
            z=pg.locateCenterOnScreen('download.jpg',confidence=0.8)
            if z != None: break
            time.sleep(0.1)
        if z != None:# do download if tally the download.png
            pg.hotkey('ctrl','v')
            pg.hotkey('enter')
            time.sleep(0.5)
            NUM_IMG = NUM_IMG + 1
        else:
            pg.hotkey('esc')


def findRelatedImg():
    time.sleep(1)
    z = pg.locateCenterOnScreen("sponsored.jpg", confidence=0.8)
    if z != None:
        pg.click(ANCHOR_IMG_X_Y[0], ANCHOR_IMG_X_Y[1]+SPONSORED_OFFSET_Y)
    else:
        pg.click(ANCHOR_IMG_X_Y[0], ANCHOR_IMG_X_Y[1])
    time.sleep(2)
    z = pg.locateCenterOnScreen("see_more.jpg", confidence=0.8)
    if z == None:
        pg.click(ANCHOR_IMG_X_Y[0]+IMAGE_OFFSET[0], ANCHOR_IMG_X_Y[1])
        time.sleep(2)
        z = pg.locateCenterOnScreen("see_more.jpg", confidence=0.8)
        if z == None:
            print("Unable to search for related image. Stopping script")
            sys.exit()
    pg.click(z[0], z[1])

def google(Object,line):#browser start all the way until table
    global NUM_IMG
    NUM_IMG = 0

    browser.get('https://www.google.com/imghp?hl=EN')
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Object)
    browser.implicitly_wait(1)
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    browser.implicitly_wait(10)

    findRelatedImg()

    while NUM_IMG < line:
        X = LEFT_OFFSET
        Y = TOP_OFFSET
        while Y < BOTTOM_BOUNDARY:
            while X < RIGHT_BOUNDARY:
                imageDownload(X, Y, Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S")))
                X = X + IMAGE_OFFSET[0]
            Y = Y + IMAGE_OFFSET[1]
            X = LEFT_OFFSET

        z = pg.locateCenterOnScreen('end.jpg', confidence=0.8)
        if z != None:
            print("Completed scraping for " + Object)
            break

        z = pg.locateCenterOnScreen('show more results.jpg', confidence=0.8)
        if z != None:
            pg.click(z[0], z[1])

        time.sleep(1)
        pg.click(SCROLL_DOWN_X_Y[0], SCROLL_DOWN_X_Y[1])

    print("Downloaded " + str(NUM_IMG) + " images for " + Object)



google('fresh garlic',300)
# google('cheese slice',400)
finish=time.perf_counter()
print(f'Finished in {round(finish-start,2)}second(s)')
#Object/Chicken Meat is the object is to google search
#100/line in above means the number of lines needed to download.
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line
