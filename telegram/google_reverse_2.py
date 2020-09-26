# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:08:31 2020

@author: user
"""
import os
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
options.add_argument("--disable-extensions")


def google_reverse():
    executable_path=os.path.abspath("chromedriver")
    driver = webdriver.Chrome(executable_path,options=options)
    try:
    # Open the website
        driver.get('https://images.google.com/')

    # Find cam button
        cam_button = driver.find_elements_by_xpath("//div[@aria-label=\"Search by image\" and @role=\"button\"]")[0]
        cam_button.click()

    # Find upload tab
        upload_tab = driver.find_elements_by_xpath("//*[contains(text(), 'Upload an image')]")[0]
        upload_tab.click()

    # Find image input
        upload_btn = driver.find_element_by_name('encoded_image')
        upload_btn.send_keys(os.getcwd()+"/telegram_image.jpg")

        driver.implicitly_wait(10)
        return google_reverse2(driver)
    except Exception as e:
        print(e)

    driver.quit()
    
def google_reverse2(driver):
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
    
print(google_reverse())