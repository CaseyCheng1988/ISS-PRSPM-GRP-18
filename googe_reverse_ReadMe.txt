-----google_reverse.py-----
********************************************************************************************************
this is a function which will allow images(regardless,bing,google,yandex images..etc) to be uploaded into google image then revert with a 
label or string which google thinks relevant.

this uses selenium,pyautogui, playsound,os. The selenium will first be popping out google image search, after it 
click into file tab, pyautogui will take over and execute file upload according to the filepath given.

the label/string searched from google will be inserted 
into google_label.xlsx which will allow us to use excel functions like filters
*********************************************************************************************************

1. To run this python script, please mount the relevant folderpath in line 28(path of the folder which contains the images
which you wanna search)  

2. Please mount excelpath called google_label.xlsx in line 29(path of the excel which you want to save the information extracted from google 
image search and the action file to execute deletion)

3. Please mount your selenium driver path to chromedriverPath in line 27

4. Please run the script and then the respective comments will pop out accordingly. 
if you want to pause the program, pls press and hold 'alt' button in the keyboard, 
if paused successfully, it will come out a ding sound.

if you want to resume the program, pls press and hold 'insert' button in the keyboard, 
if resumed successfully, it will come out a ding sound.

5. Inside google_label.xlsx, the insertion of string 'd' in action column will execute deletion of the file inside the folder 
which you inserted in line 28, so please use it cautionly( u must be sure that you want to execute deletion file )
