 # -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:08:50 2020
@author: user
"""
# webhook_remover is needed to delete outside webhook from conflicting
#with the current connection, webhook conflict will occur every 15-30minutes
#so i have wrote a library called webhook_remover and used threading
# to delete the webhook every 10 second, threading module is needed
# so that it can run concurrently with the code

from io import BytesIO
from Prediction_Model import model
from telegram.ext import Updater,MessageHandler,Filters
import os
import sys

dir_main = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(dir_main, "Recipe_Requests"))

import Yummly

TOKEN='1351428540:AAHHYbP6MSUCc47LjKUqkw71IyRKhkUaQ6o'

tele_ingredients = []
yummly=[]
userOption=[]

def YummlyToString(yummly):
    i=len(yummly)-1
    prev_y=''
    while i>-1:
        y=str(i+1)+'. '+yummly[i]+'\n'+prev_y
        prev_y=y
        i-=1
    return 'Yummly suggestions:\n'+y

def Yummlymessage(yummly,update):
    try:
        if len(yummly)>0:
            replies=int(update.message.text)
            if replies>0:
                RecipeName=yummly[replies-1]
                return RecipeName
    except Exception:
        pass


def message(update,context):
    global yummly,yum,y

    #below is the detect the integer from user, so that to match the recipe name
    if Yummlymessage(yummly,update)!=None:
        userOption.append(Yummlymessage(yummly,update))
        update.message.reply_text(userOption)
        print(userOption)
        update.message.reply_text('Above is the user option\n'+
            'If decided to pick this recipe, pls reply "chosen yummly" to extract the details.\n'+
                                  'If got typo or want to clear user option, pls reply "clear user option"')
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
        yum = Yummly.Yummly(ingredients)
        y=YummlyToString(yum.top10RecipesName)
        print(y)
        update.message.reply_text(y+'\n'+
                                  'Pls confirm which recipe to pick?'
                                  +'\n'+
                                  'For eg, if want recipe 1, pls reply just "1".')

        tele_ingredients.clear()
        ingredients.clear()
        userOption.clear()

    if update.message.text.upper().find('CHOSEN YUMMLY')>-1:
        i=0
        while i<len(userOption):
            details=yum._getRecipeText(userOption[i])
            print(details)
            update.message.reply_text(details)
            i+=1

    if update.message.text.upper().find('SHOW YUMMLY')>-1:
        print(y)
        update.message.reply_text(y)

    if update.message.text.upper().find('SHOW USER OPTION')>-1:
        print(userOption)
        update.message.reply_text(userOption)

    if update.message.text.upper().find('CLEAR USER OPTION')>-1:
        print('userOption list cleared')
        update.message.reply_text('userOption list cleared')
        userOption.clear()

def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

def receive_image(update,context):
    try:
        print('download in progress')
        update.message.reply_text('download in progress')
        obj=context.bot.getFile(file_id=update.message.photo[-1].file_id)
        f =  BytesIO(obj.download_as_bytearray())
        write_bytesio_to_file('telegram_image.jpg', f)
        update.message.reply_text('file has been downloaded')
        print('file has been downloaded')
        google_label=model()
        print(google_label)
        update.message.reply_text(google_label+
                                  " is added into into ingredients list.\n"+
                                  "If want to add in more ingredient , pls upload the photo.\n"
                                  "If ingredients enough, pls reply 'to yummly' once it is confirmed.")
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

telegramBot(TOKEN)
