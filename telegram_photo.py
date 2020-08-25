# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:08:50 2020

@author: user
"""
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters

def start(update,context):
    update.message.reply_text('Hi,welcome')
    
def message(update,context):
    print(update.message.text)
    if update.message.text.upper().find('LOVE')>-1:
        update.message.reply_text('love you too')
    elif update.message.text.upper().find('THANK')>-1:
        update.message.reply_text('you are welcome')
    elif update.message.text.upper().find('HOW ARE YOU')>-1:
        update.message.reply_text('i am fine')
    else:
        update.message.reply_text('are you here')  
    
def receive_image(update,context):
    try:
        print('download in progress')
        update.message.reply_text('download in progress')
        obj=context.bot.getFile(file_id=update.message.document.file_id)
        obj.download()
        update.message.reply_text('file has been downloaded')
        print('file has been downloaded')
    except Exception as e:
        print(str(e))
    
def main():
    updater=Updater(token='1351428540:AAHHYbP6MSUCc47LjKUqkw71IyRKhkUaQ6o',use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(MessageHandler(Filters.text,message))
    dp.add_handler(MessageHandler(Filters.document.jpg,receive_image))
    updater.start_polling()
    updater.idle()

def command_handling_fn(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id,text='testing')

main()