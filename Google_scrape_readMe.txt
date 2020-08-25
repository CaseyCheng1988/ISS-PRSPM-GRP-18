1. Python Selenium Module,pyautogui, pyperclip,OpenCV is needed for this to work
2. Please paste the appropriate path of your selenium chromedriver in line 19
3. Please download google_scrape.zip for its PNG images because the program needs it to detect the background in google image and pls mount it at the same folder with google_image.py
4. Please make sure the download pop out in google chrome is maximized so that the program can execute download command
5. Selenium is only used in the initial stage of the code then pyautogui will take over.
6. When browser starts, it will execute pulldown and pullup action so that maximum amount of photo will be captured in the browser. if you don't want pulldown and pullup, pls comment them out. It will still work, just that you will need to do manual pulldown and pullup or accepting minimal images in the browser
7.Pyautogui will do a image check on your pop out and right click and download the images.
8.The clicking action will be click at 5 different postion, point a,b,c,d&e.
9.After point e, it will scroll down the page and the cycle will loop again until it detected the end of page then only it will break the loop
