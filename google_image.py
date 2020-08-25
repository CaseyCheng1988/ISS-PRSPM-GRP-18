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

def imageDownload(X,Y,a):
    pyperclip.copy('NA')
    time.sleep(2)
    pg.click(x=X, y=Y,button='right')
    time.sleep(2)
    
    z=pg.locateOnScreen('save_image.png',confidence=0.8,region=(a,779,238,175))
    z=pg.locateOnScreen('save_image.png',confidence=0.8,region=(a,779,238,175))
    if z!=None:#detect whether save as image pop out came out
        Nkey(5,'up')
        time.sleep(1)
        pg.hotkey('enter')
        
    else:
        pg.hotkey('esc')
 
    time.sleep(4)
    if pg.locateOnScreen(('download.png'),confidence=0.8,region=(11,875,1583,130))!=None:# do download if tally the download.png
        pg.hotkey('enter')
    else: 
        pg.hotkey('esc')

def pulldown():#pull down the page initially
    i=0
    while i<300:
       pg.doubleClick(1906,1010)
       i+=1
       
    count=0   
    while count<70: 
        pg.doubleClick(1906,1010)
        if pg.locateOnScreen('show more results.png',confidence=0.8)!=None:
            pg.click(922,803)
        count+=1

    count1=0
    while count1<150:
       pg.doubleClick(1906,1010)
       count1+=1
    
    count2=0
    while count2<100:
        pg.doubleClick(1906,1010)
        if pg.locateOnScreen('end.png',confidence=0.8)!=None:
            break
        count2+=1
    n=int(i+count+count1+count2)
    return n

def pullup(n):#pull up to go back the top page
    i=0
    while i<n:
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
        
    imageDownload(228,555,247)
    imageDownload(562,555,581)
    imageDownload(978,555,997)
    imageDownload(1333,555,1352)
    imageDownload(1711,555,1495)
    
def google(Object,line):#browser start all the way until table 
    browser.get('https://www.google.com/imghp?hl=EN')
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Object)
    browser.implicitly_wait(1)
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    browser.implicitly_wait(10)

    n=pulldown()
    pullup(n)
    i=0
    while i<line:
        DownloadLine(i,Object)
        i+=1
    
google('chicken meat',400)# pls input here. 
#Object/Chicken Meat is the object is to google search
#100/line in above means the number of lines needed to download. 
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line
