# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:50:12 2020

@author: user
"""
import time 
start=time.perf_counter()
import pyautogui as pg
from playsound import playsound
import  time, os,pyperclip,keyboard,xlsxwriter
start=time.perf_counter()
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
options = Options()
#options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

chromedriverPath='C://Users//user//OneDrive - National University of Singapore//IS5002//projects//chromedriver'
folderpath=r'C:\Users\user\OneDrive - National University of Singapore\IS5002\projects\ISS-PRSPM-GRP-18-master\ISS-PRSPM-GRP-18-master\cleaned google datas\5Sep2020\bell pepper'
excelpath=r'C:\Users\user\OneDrive - National University of Singapore\IS5002\projects\google_label.xlsx'

def Ding():
    playsound('C:/Users/user/OneDrive - National University of Singapore/IS5002/projects/google_scrape_file/google_scrape/Ding-sound-effect.mp3')

def Pause(pause):
    if keyboard.is_pressed('alt'):
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
        
def google_reverse(filepath,driver):
    Pause(0)
    driver.implicitly_wait(10)
    Pause(0)
    site = 'https://www.google.com/imghp?hl=EN'
    driver.get(site)
    Pause(0)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[3]/div[2]/span").click()
    driver.implicitly_wait(10)
    Pause(0)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/a").click()
    driver.implicitly_wait(10)
    Pause(0)

    Pause(0)
    pg.hotkey('tab')
    Pause(0)
    pg.hotkey('tab')
    Pause(0)
    pg.hotkey('enter')
    Pause(0)
    filepath=filepath.replace('/','\,').replace(',','')
    Pause(0)
    pyperclip.copy(filepath)
    Pause(0)
    time.sleep(1)
    Pause(0)
    pg.hotkey('ctrl','v')
    pg.hotkey('enter')
    Pause(0)
    
    try:
        text= driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a").text
    except Exception:
        try:
            text= driver.find_element_by_xpath("/html/body/div[7]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a").text
        except Exception:
            text = driver.find_element_by_id("topstuff").text
    return text

def rec_google(path,driver):
    try:
        return google_reverse(path,driver)
    except Exception:
        rec_google(path,driver)

def excelwrite(wait,excel):
    try:
        if excel:
            outWorkbook2.close()
    except Exception:
        if wait==0:
            print('please close google_label.xlsx to save the current result')
        time.sleep(3)
        wait+=1
        excelwrite(wait)

def excelStarter(outSheet):
    outSheet.write(0, 0,'filename')
    outSheet.write(0, 1,'google_label')
    outSheet.write(0, 9,'action')
    
def main():
    driver = webdriver.Chrome(chromedriverPath,options=options)
    folder=os.listdir(folderpath)
    i=0
    while i<len(folder):
        Pause(0)
        path=folderpath+'/'+folder[i]
        Pause(0)
        google_label=rec_google(path,driver)
        print(google_label)
        print(str(i)+'\n')
        if google_label!=None:
            outSheet.write(i+1, 0,folder[i])
            outSheet.write(i+1, 1,google_label)
            i+=1
    driver.close()

def excelread(wait):
    try:
        ExcelRead=pd.read_excel(excelpath)
        print('in progress')
    except Exception:
        if wait==0:
            print('please close google_label.xlsx to proceed')
        time.sleep(3)
        wait+=1
        excelread(wait)

def excelaction():
    excel_count=0
    while excel_count<len(ExcelRead):
        action=str(ExcelRead['action'][excel_count])
        if action=='d':
            filename=str(ExcelRead['filename'][excel_count])
            filepath=folderpath+'/'+filename
            filepath=filepath.replace('/','\,').replace(',','')
            try:
                os.remove(filepath)
            except Exception:
                print(filename+' cannot be deleted because the file no longer exist')
            
        excel_count+=1

outWorkbook2=xlsxwriter.Workbook("google_label.xlsx")
outSheet=outWorkbook2.add_worksheet()
excelStarter(outSheet)

N=input('do you want to start a google_reverse search\n(ans:y or n)\n')
if N=='y':
    main()

excelwrite(0,N=='y')

x=input('pls check the google_label.xlsx and decide whether to delete\n(ans:y or n)\n')
excelread(0)
ExcelRead=pd.read_excel(excelpath)
if x=='y':
    excelaction()


finish=time.perf_counter()
print(f'Finished in {round(finish-start,2)}second(s)')


