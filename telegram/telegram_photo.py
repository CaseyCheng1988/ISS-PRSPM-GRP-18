 """
Created on Sun Aug 23 13:08:50 2020
@author: user
"""
import time
# webhook_remover is needed to delete outside webhook from conflicting
#with the current connection, webhook conflict will occur every 15-30minutes
#so i have wrote a library called webhook_remover and used threading
# to delete the webhook every 10 second, threading module is needed
# so that it can run concurrently with the code
from webhook_remover import webhook_remover
from req_recipe import main # import Jie Shen's req_recipe.py main function
from telegram.ext import Updater,MessageHandler,Filters
import os,pyperclip,threading
import pyautogui as pg
start=time.perf_counter()
from selenium import webdriver
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
TOKEN='1117701604:AAFffyfiR5PyIZHCtTxDiSPwe87YuO8S3x4'
chromedriverPath='C://Users//user//OneDrive - National University of Singapore//IS5002//projects//chromedriver'
#folderpath of the python_telegram_photo
folderpath=r'C:\Users\user\OneDrive - National University of Singapore\IS5002\projects'
A=['STEAK','BEEF','SALMON','CHICKEN','BROCCOLI','CABBAGE','CARROT'
   ,'CELERY','CORN','CUCUMBER','BRINJAL','EGGPLANT','GREEN BEAN'
   ,'BELL PEPPER','OLIVE','ONION','POTATO','SPINACH','TOMATO'
   ,'APPLE','AVOCADO','BANANA','LEMON','BREAD','CHEESE'
   ,'MUSHROOM','EGG'
   ]
a=['steak','steak','salmon','chicken','broccoli','cabbage','carrot'
   ,'celery','corn','cucumber','eggplant','eggplant','green bean'
   ,'green pepper','olive','onion','potato','spinach','tomato'
   ,'apple','avocado','banana','lemon','bread','cheese'
   ,'mushroom','egg'
   ]
tele_ingredients = []

def file():
    folder=os.listdir(folderpath)
    i=0
    FILE=[]
    #print(folder)
    while i<len(folder):
        if folder[i].find('file_')>-1 and folder[i].find('jpg') >-1:
            file=int(folder[i].replace('file_','').replace('.jpg',''))
            FILE.append(file)
        i+=1
    filepath=folderpath+'/file_'+str(max(FILE))
    filepath=filepath.replace('/','\,').replace(',','')
    
    #main target of the model function is here
    #google_reverse function is a temporary substitute to the model
    #input to it is the newly downloaded image filepath from telegram
    #output is the 25 different category of label/short strings like 'potato' etc
    google_label=google_reverse(filepath)
    
    try:
        os.remove(filepath+'.jpg')
        print(filepath+' deleted')
    except Exception:
        print(filepath+' cannot be deleted because the file no longer exist')
    return google_label


def ingredientsFilter(google_label):
    i=0
    while i<len(A):
        if google_label.upper().find(A[i])>-1:
            return a[i]
        i+=1  

def google_reverse(filepath):
    driver = webdriver.Chrome(chromedriverPath,options=options)
    driver.implicitly_wait(10)
    site = 'https://www.google.com/imghp?hl=EN'
    driver.get(site)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[3]/div[2]/span").click()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/a").click()
    except Exception:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/a").click()
        #/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/a
        except Exception:
            driver.close()
    driver.implicitly_wait(10)

    pg.hotkey('tab')
    pg.hotkey('tab')
    pg.hotkey('enter')
    pyperclip.copy(filepath)
    time.sleep(4)
    pg.hotkey('ctrl','v')
    pg.hotkey('enter')
    pg.hotkey('esc')
    
    try:
        text= driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a").text
    except Exception:
        try:
            text= driver.find_element_by_xpath("/html/body/div[7]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a").text
        except Exception:
            try:
                text = driver.find_element_by_id("topstuff").text
            except Exception:
                driver.close()
    driver.close()
    return text
    
def message(update,context):
    print(update.message.text)
    #Type 'to yummly' in telegram danielthx account
    #and it will activate yummly function
    if update.message.text.upper().find('TO YUMMLY')>-1:
        update.message.reply_text('transfering to yummly')
        ingredients = list(filter(None, tele_ingredients)) 
        print(ingredients)
        
        #main target for yummly function
        #ingredients list/array to input to yummly main function
        #from yummly, it should output standard strings
        yummly=main(ingredients)
        print(yummly)
        update.message.reply_text(yummly)
        
        tele_ingredients.clear()
        ingredients.clear()

def receive_image(update,context):
    try:
        print('download in progress')
        update.message.reply_text('download in progress')
        obj=context.bot.getFile(file_id=update.message.photo[-1].file_id)
        obj.download()
        update.message.reply_text('file has been downloaded')
        print('file has been downloaded')
        google_label=file()
     #   print(google_label)
        google_label=ingredientsFilter(google_label)
        print(google_label)
        update.message.reply_text(google_label)
        tele_ingredients.append(google_label)
 
    except Exception as e:
        print(str(e))
        receive_image(update,context)

def telegramBot(TOKEN):
    updater=Updater(token=TOKEN,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,message))
    dp.add_handler(MessageHandler(Filters.photo,receive_image))
    updater.start_polling()
    updater.idle()

threading.Thread(target=webhook_remover,args=[TOKEN]).start()
telegramBot(TOKEN)
