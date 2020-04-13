from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

import logging

TOKEN = '873643803:AAH-u1t5m0hc_EvKeCzi7zPYbjQneDUPkIM'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot():
    def __init__(self, input_q):
        self.input_q = input_q

    def start(self, update, context):
        update.message.reply_text('Hallo')
        reply_keyboard = [['action'], ['left', 'right']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)  
            
    def button(self, update, context):
        command = update.message.text
        self.input_q.put_nowait(command)    
        update.message.reply_text(text="Selected option: {}".format(command))

    def help(self, update, context):
        update.message.reply_text("Use /start to test this bot.")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(TOKEN, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', self.start, pass_args=True))
#        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.button))
        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        updater.dispatcher.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()