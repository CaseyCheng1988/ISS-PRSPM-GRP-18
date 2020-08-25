# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:43:20 2020
@author: user
"""
import time 
import datetime  
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

def imageDownload(X,Y,a,Object):
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
    pyperclip.copy(Object)
    time.sleep(4)
    if pg.locateOnScreen(('download.png'),confidence=0.8,region=(11,875,1583,130))!=None:# do download if tally the download.png
        pg.hotkey('ctrl','v')
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
    while count1<120:
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
    if i!=0:
        pg.hotkey('esc')
        time.sleep(1)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.click(1906,937)
        
    imageDownload(228,555,247,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'a.jpg')
    imageDownload(562,555,581,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'b.jpg')
    imageDownload(978,555,997,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'c.jpg')
    imageDownload(1333,555,1352,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'d.jpg')
    imageDownload(1711,555,1495,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'e.jpg')
    
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
        z1=pg.locateOnScreen('end.png',confidence=0.8)
        z1=pg.locateOnScreen('end.png',confidence=0.8)
        if z1!=None:
            break
        else:
            DownloadLine(i,Object)

        i+=1
    
google('raw chicken meat',400)# pls input here. 
finish=time.perf_counter()
print(f'Finished in {round(finish-start,2)}second(s)')
#Object/Chicken Meat is the object is to google search
#400/line in above means the number of lines needed to download. 
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line. However, it will be limited to google image end page, usually max is 400images
