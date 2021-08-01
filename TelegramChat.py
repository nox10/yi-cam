from telegram import *
from telegram.ext import *


class TelegramChat:

    def __init__(self, camera, dispatcher, callbackUpdate):
        self.camera = camera
        self.updateStatus = callbackUpdate
        
        self.sayCommand = f"/say {self.camera.name} "

        dispatcher.add_handler(MessageHandler(Filters.regex(f"{self.camera.name} On"), self.enableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(f"{self.camera.name} Off"), self.disableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(f"{self.camera.name} Foto"), self.getImmagine))

        dispatcher.add_handler(MessageHandler(Filters.regex(self.sayCommand), self.textToSpeech))


    def enableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(True, update, CallbackContext)


    def disableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(False, update, CallbackContext)


    def enableNotification(self, update: Update, context: CallbackContext):
        self.__setNotification(True, update, CallbackContext)
    

    def disableNotification(self, update: Update, context: CallbackContext):
        self.__setNotification(False, update, CallbackContext)


    def __setNotification(self, enabled, update: Update, context: CallbackContext):
        self.camera.setNotification(enabled)
        self.updateStatus(True)
    

    def textToSpeech(self, update: Update, context: CallbackContext):
        text = update.message.text.replace(self.sayCommand, "")
        if len(text) == 0:
            update.message.reply_text(f"err arg empty")
        else:
            update.message.reply_text(f"Saying {text}")
            self.camera.textToSpeech(text)


    def __setCamera(self, enabled, update: Update, context: CallbackContext):
        status = "On" if enabled else "Off"
        update.message.reply_text(f"Trying to set {self.camera.name} {status}...")
        if self.camera.enableCam(enabled):
            update.message.reply_text(f"{self.camera.name} is {status}")
        else:
            update.message.reply_text(f"Trying to set {self.camera.name} failed")


    def getImmagine(self, update: Update, context: CallbackContext):
        self.camera.sendImage(force = True)