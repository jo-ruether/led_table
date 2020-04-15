from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

import logging

# Johannes
# TOKEN = '873643803:AAH-u1t5m0hc_EvKeCzi7zPYbjQneDUPkIM'
# Arjun
TOKEN = '1242272775:AAHdR1ImQce9f9MfnnvbBYP0s0VldNO7I-o'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot():
    def __init__(self, postman):
        self.postman = postman

    def start(self, update, context):
        update.message.reply_text('Hallo')
        reply_keyboard = [['action'], ['left', 'right']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)  
            
    def button(self, update, context):
        command = update.message.text
        self.postman.send('UserInput', command)
        update.message.reply_text(text="Selected option: {}".format(command))

    def help(self, update, context):
        update.message.reply_text("Use /start to test this bot.")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def set(self, update, context):
        """ Change configuration of games"""
        command = context.args
        if len(command) == 2:
            self.postman.send('Settings', command)
        else:
            # Bug This statement doesn't get printed!
            update.message.reply_text("Please stay to the standard format: ```/set <variable> "
                                      "<value>.```")

    def check_user_feedback(self, update):
        """ Asks postman for user feedback to be printed out"""
        post = self.postman.request('UserFeedback')
        if post:
            msg = post['message']
            update.message.reply_text(msg)

    def run(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(TOKEN, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', self.start, pass_args=True))
#        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        updater.dispatcher.add_handler(CommandHandler('set', self.set))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.button))
        updater.dispatcher.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        while True:
            self.check_user_feedback(updater)
