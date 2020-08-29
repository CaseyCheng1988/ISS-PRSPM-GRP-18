# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:43:20 2020
@author: user
"""
import time 
from playsound import playsound
import keyboard
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

def Ding():
    playsound('C:/Users/user/OneDrive - National University of Singapore/IS5002/projects/google_scrape_file/google_scrape/Ding-sound-effect.mp3')

def Pause(pause):
    if keyboard.is_pressed('esc'):
            pause=1
    i=0
    while pause:
        if i==0:
            Ding()
            print('paused')
        if keyboard.is_pressed('insert'):
            Ding()
            print('resumed')
            pause=0
        i+=1

def PauseImage(pause,X,Y,a,Object):
    if keyboard.is_pressed('esc'):
            pause=1
    i=0
    while pause:
        if i==0:
            Ding()
            print('paused')
        if keyboard.is_pressed('insert'):
            Ding()
            print('resumed')
            imageDownload(X,Y,a,Object)
            pause=0
        i+=1
    

def Nkey(N,key):
    i=0
    while i<N:
        pg.hotkey(key)
        i+=1

def imageDownload(X,Y,a,Object):
    PauseImage(0,X,Y,a,Object)
    time.sleep(2)
    PauseImage(0,X,Y,a,Object)
    pg.click(x=X, y=Y,button='right')
    PauseImage(0,X,Y,a,Object)
    time.sleep(2)
    PauseImage(0,X,Y,a,Object)
    z=pg.locateOnScreen('save_image.png',confidence=0.8,region=(a,779,238,175))
    z=pg.locateOnScreen('save_image.png',confidence=0.8,region=(a,779,238,175))
    PauseImage(0,X,Y,a,Object)
    if z!=None:#detect whether save as image pop out came out
        Nkey(5,'up')
        time.sleep(1)
        pg.hotkey('enter')
        
    else:
        pg.hotkey('esc')
    PauseImage(0,X,Y,a,Object)
    pyperclip.copy(Object)
    PauseImage(0,X,Y,a,Object)
    time.sleep(4)
    if pg.locateOnScreen(('download.png'),confidence=0.8,region=(11,875,1583,130))!=None:# do download if tally the download.png
        pg.hotkey('ctrl','v')
        pg.hotkey('enter')
    else: 
        pg.hotkey('esc')

def pulldown():#pull down the page initially
    pg.click(1893,983)
    time.sleep(1)
    i=0
    while i<300:
       Pause(0)
       pg.doubleClick(1906,1010)
       i+=1
       
    count=0   
    while count<70:
        Pause(0)
        pg.doubleClick(1906,1010)
        if pg.locateOnScreen('show more results.png',confidence=0.8)!=None:
            pg.click(922,803)
        count+=1

    count1=0
    while count1<120:
       Pause(0)
       pg.doubleClick(1906,1010)
       count1+=1
    
    count2=0
    while count2<100:
        Pause(0)
        pg.doubleClick(1906,1010)
        if pg.locateOnScreen('end.png',confidence=0.8)!=None:
            break
        count2+=1
    n=int(i+count+count1+count2)
    return n

def pullup(n):#pull up to go back the top page
    i=0
    while i<n:
       Pause(0)
       pg.doubleClick(1906,178) 
       i+=1

def DownloadLine(i,Object):
    Pause(0)
    if i!=0:
        pg.hotkey('esc')
        time.sleep(1)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.doubleClick(1906,937)
        pg.click(1906,937)
    Pause(0)
    imageDownload(228,555,247,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'a.jpg')
    Pause(0)
    imageDownload(562,555,581,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'b.jpg')
    Pause(0)
    imageDownload(978,555,997,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'c.jpg')
    Pause(0)
    imageDownload(1333,555,1352,Object+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+str(i)+'d.jpg')
    Pause(0)
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

        
# pls input here.
google('raw Celery',400)
google('UNCOOKED Celery',400)
google('vegetable Celery',400)
google('green Celery',400)

 
finish=time.perf_counter()
print(f'Finished in {round(finish-start,2)}second(s)')
#Object/Chicken Meat is the object is to google search
#100/line in above means the number of lines needed to download. 
#For example if 1000 images were to be downloaded, then 200lines has to be inputted in line
