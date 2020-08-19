# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:43:20 2020

@author: user
"""
import time 
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
browser=webdriver.Chrome('C://Users//user//OneDrive - National University of Singapore//IS5002//projects//chromedriver',options=options)
pg.FAILSAFE=True

def Nkey(N,key):
    i=0
    while i<N:
        pg.hotkey(key)
        i+=1

def imageDownload(X,Y,URL,Object):
    time.sleep(2)
    pg.click(x=X, y=Y,button='right')
    Nkey(7,'down')#move down 7times to download image
    time.sleep(1)
    pg.hotkey('enter')#enter to execute download
    time.sleep(1)
    pg.hotkey('ctrl','c')
    
    time.sleep(1)
    if len(pyperclip.paste())>40:#from the copied string, check whether is it more than 40characters
        pg.hotkey('esc')
        time.sleep(1)
        pg.hotkey('ctrl','l')
        time.sleep(1)
        pg.hotkey('ctrl','c')#copy the browser link
        if pyperclip.paste()!=URL:#check if browser link not the same with URL then close it
            pg.hotkey('ctrl','w')
    else:
        pyperclip.copy(Object)
        time.sleep(1)
        pg.hotkey('ctrl','v')#rename the file with respective object and line location
        time.sleep(1)
        pg.hotkey('enter')

def DownloadLine(i,URL,Object):
    time.sleep(2)
    Object=Object+str(i)#line location and various points in column
    if i!=0:
        Nkey(2,'down')
    imageDownload(228,555,URL,Object+'a')
    imageDownload(562,555,URL,Object+'b')
    imageDownload(978,555,URL,Object+'c')
    imageDownload(1333,555,URL,Object+'d')
    imageDownload(1711,555,URL,Object+'e')
    
def google(Object,line):#browser start all the way until table 
    browser.get('https://www.google.com/imghp?hl=EN')
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Object)
    browser.implicitly_wait(1)
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    browser.implicitly_wait(10)
    pg.hotkey('ctrl','l')
    time.sleep(1)
    pg.hotkey('ctrl','c')
    time.sleep(1)
    URL=pyperclip.paste()
    i=0
    while i<line:
        DownloadLine(i,URL,Object)
        i+=1
    
google('Chicken Meat',100)# pls input here. 
#Object/Chicken Meat is the object is to google search
#100/line in above means the number of lines needed to download. 
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line