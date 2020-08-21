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
browser=webdriver.Chrome('C:\\Users\\tanda\\Documents\\python testing\\chromedriver',options=options)  
pg.FAILSAFE=True

def Nkey(N,key):
    i=0
    while i<N:
        pg.hotkey(key)
        i+=1

def imageDownload(X,Y,Object):
    pyperclip.copy('NA')
    time.sleep(2)
    pg.click(x=X, y=Y,button='right')
    
    time.sleep(1)
    Nkey(3,'up')
    time.sleep(1)
    pg.hotkey('enter')#enter to execute download
    time.sleep(3)
    pg.hotkey('ctrl','c')
    time.sleep(2)
    pg.hotkey('esc')
    time.sleep(1)
    
    
    if len(pyperclip.paste())>100:
        pg.click(x=X, y=Y,button='right')
        Nkey(5,'up')#move down 7times to download image
        time.sleep(1)
        pg.hotkey('enter')#enter to execute download
        time.sleep(2)
        pg.hotkey('ctrl','c')
        time.sleep(1)
        pyperclip.copy(Object+'.jpg')
        time.sleep(2)
        pg.hotkey('ctrl','v')#rename the file with respective object and line location
        time.sleep(1)
        pg.hotkey('enter')
        
    elif pyperclip.paste().find('search')>-1:
        time.sleep(1)
        pg.hotkey('enter')
        time.sleep(5)
        pulldown2()
        pullup()

def pulldown():#pull down the page initially
    i=0
    while i<200:
       pg.doubleClick(1906,1010) 
       i+=1

def pulldown2():#pull down the page once enter a new link
    i=0
    while i<200:
       pg.doubleClick(1906,937) 
       i+=1

def pullup():#pull up to go back the top page
    i=0
    while i<200:
       pg.doubleClick(1906,178) 
       i+=1

def DownloadLine(i,Object):
    time.sleep(2)
    Object=Object+str(i)#line location and various points in column
    if i!=0:
        pg.hotkey('esc')
        time.sleep(1)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.click(1906,178)
        pg.doubleClick(1906,937)
        
    #    time.sleep(1)
     #   Nkey(2,'down')
    imageDownload(228,555,Object+'a')
    imageDownload(562,555,Object+'b')
    imageDownload(978,555,Object+'c')
    imageDownload(1333,555,Object+'d')
    imageDownload(1711,555,Object+'e')
    
def google(Object,line):#browser start all the way until table 
    browser.get('https://www.google.com/imghp?hl=EN')
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Object)
    browser.implicitly_wait(1)
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    browser.implicitly_wait(10)

    pulldown()
    pullup()
    i=0
    while i<line:
        DownloadLine(i,Object)
        i+=1
    
google('chicken meat',400)# pls input here. 
#Object/Chicken Meat is the object is to google search
#100/line in above means the number of lines needed to download. 
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line
