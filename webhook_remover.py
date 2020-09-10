# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:50:12 2020

@author: user
"""
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

chromedriverPath='C://Users//user//OneDrive - National University of Singapore//IS5002//projects//chromedriver'
folderpath=r'C:\Users\user\OneDrive - National University of Singapore\IS5002\projects\ISS-PRSPM-GRP-18-master\ISS-PRSPM-GRP-18-master\cleaned google datas\5Sep2020\bell pepper'
excelpath=r'C:\Users\usezr\OneDrive - National University of Singapore\IS5002\projects\google_label.xlsx'
driver = webdriver.Chrome(chromedriverPath,options=options)

def webhook_remover(TOKEN):
    site = 'https://api.telegram.org/bot'+TOKEN+'/deleteWebhook'
    driver.get(site)
    while True:  
        time.sleep(10)
        driver.refresh()

#webhook_remover('1117701604:AAFffyfiR5PyIZHCtTxDiSPwe87YuO8S3x4')