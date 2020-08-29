1.please pip install telegram
2. The bot name is called danielthx2bot, so you can try it out in telegram once python script was start up
3. Main focus should be on receive_image function, because it is an interrupt based system.
4. This receive_image function can only work when the photos are attached to file not send like normal photos, after it is sent from user to danielthx2bot, 
the photo will be autodownloaded into the same folder which contains telegram_photo.py
5.update.message.reply_text('string') will be the main mechanism of replying the user after he/she sent the photo 