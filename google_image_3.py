# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:08:31 2020

@author: user
"""
import concurrent.futures
import requests, time, os,datetime
from io import BytesIO
from PIL import Image
start=time.perf_counter()
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
options = Options()
#options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
#options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

excelInputPath="C:/Users/user/OneDrive - National University of Singapore/IS5002/projects/ISS-PRSPM-GRP-18-master/ISS-PRSPM-GRP-18-master/google_scrape/google_scrape_1.xlsx"
chromedriverPath='C://Users//user//OneDrive - National University of Singapore//IS5002//projects//chromedriver'

img_urls=[]
driver = webdriver.Chrome(chromedriverPath,options=options)
# create image directory if not exists
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))


#taking user input

def google(SEARCH_TERM):
    IMG_DIR = os.path.join(BASE_DIR, SEARCH_TERM)

    # open log file, or create and open if not exists

    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    site = 'https://www.google.com/search?tbm=isch&q='+SEARCH_TERM
    
    #passing site url
    driver.get(site)
    
    #the image anchor
    i=1
    while True:
        #start with first anchor
        driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div["+str(i)+"]/a[1]/div[1]/img").click()
        driver.implicitly_wait(8)
        
        try:
            #click see more
            driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[3]/div[3]/c-wiz/div/div/div/div[2]/a").click()
            break
        #to deal with google licensed photo,if don't have click see more, it will go back and proceed with the next picture
        except Exception:
            driver.back()
            driver.implicitly_wait(8)
        i+=1

    #below while loop scrolls the webpage 10 times(if available)
    i = 0
    while i<10:  
	#for scrolling page
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        try:
		#for clicking show more results button
            driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
        except Exception as e:
            pass
        i+=1

    #parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #scraping image urls with the help of image tag and class used for images
    img_tags = soup.find_all("img", class_="rg_i")

    count = 0
    for i in img_tags:
        try:
            img_urls.append(str(count)+'@@'+SEARCH_TERM+'##'+i['src'])
            count+=1
        except Exception as e:
            pass
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, img_urls)

def download_image(img_url):
    A=img_url.find('@@')
    B=img_url.find('##')
    url=img_url[B+2:]
    count = img_url[:A]
    SEARCH_TERM=img_url[A+2:B]

    IMG_DIR = os.path.join(BASE_DIR, SEARCH_TERM)
    LOG_FILE = os.path.join(BASE_DIR, SEARCH_TERM + '.txt')
    # open log file, or create and open if not exists
    log_file = open(LOG_FILE, 'w+')
    #passing image urls one by one and downloading
    response = requests.get(url, timeout=30)
        # get image from response
    img = Image.open(BytesIO(response.content))
        # set image path
    img_name = SEARCH_TERM+'_'+str(datetime.datetime.now().strftime("%y%m%d%H%M%S"))+'_'+count + '.jpg'
    img_path = os.path.join(IMG_DIR, img_name)
        # save image
    img.save(img_path)
    print("Saving image as {}".format(img_path))
    log_file.write("[INFO] Saving image at {}\n".format(img_path))
    print("Number of images downloaded = "+count+' '+SEARCH_TERM,end='\r')        
    

def excelread(wait):
    try:
        ExcelRead=pd.read_excel(excelInputPath)
        print('in progress')
    except Exception:
        if wait==0:
            print('please close google_scrap.xlsx to proceed')
        time.sleep(3)
        wait+=1
        excelread(wait)

excelread(0)
ExcelRead=pd.read_excel(excelInputPath)

excel_count=0
while excel_count<len(ExcelRead):
    SEARCH_TERM=str(ExcelRead['SEARCH_TERM'][excel_count])
    google(SEARCH_TERM)
    excel_count+=1
    
driver.close()

finish=time.perf_counter()
print(f'\nFinished in {round(finish-start,2)}second(s)')
