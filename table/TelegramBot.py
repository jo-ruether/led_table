from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Bot, ReplyKeyboardMarkup

from table.Postman import Topics
from table.utils.Commands import CMD

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    REGISTER = range(1)

    def __init__(self, postman, config_handler):
        self.postman = postman
        self.config_handler = config_handler
        self.token = config_handler.get_value("TelegramBot", "token")
        self.bot = Bot(self.token)
        self.password = config_handler.get_value("TelegramBot", "password")
        self.admin_user = config_handler.get_value("TelegramBot", "admin_user")

    def start(self, update, context):
        logger.info("TelegramBot is started.")
        update.message.reply_text('Welcome to this awesome LED Table! Please enter the correct '
                                  'password to register as admin')

        return self.REGISTER

    def register(self, update, context):
        if update.message.text == self.password:
            # Correct password, now register
            self.admin_user = update.message.from_user.id
            self.config_handler.set_value("TelegramBot", "admin_user", self.admin_user)

            logger.info(f"Registered new admin: {update.message.from_user.username}")
            update.message.reply_text(f"Registration successful! From now on I only listen to "
                                      f"{update.message.from_user.first_name}.")

            self.make_controller(update)
            return ConversationHandler.END
        else:
            update.message.reply_text("Wrong password! Please try again are enter /cancel.")
            return self.REGISTER

    def cancel(self, update, context):
        logger.debug("Stopping conversation.")

        self.make_controller(update)
        return ConversationHandler.END

    def status(self, update, context):
        if not self.admin_user:
            update.message.reply_text("No one rules this table - yet.")
        else:
            update.message.reply_text(f"Admin User: {self.admin_user}")

    def button(self, update, context):
        command = update.message.text
        logger.debug(f"UserInput received: {command}")

        if command == "left":
            self.postman.send(Topics.INPUT, CMD.LEFT)
        elif command == "right":
            self.postman.send(Topics.INPUT, CMD.RIGHT)
        elif command == "action":
            self.postman.send(Topics.INPUT, CMD.X)
        else:
            self.postman.send(Topics.INPUT, command)

    def help(self, update, context):
        update.message.reply_text("Part of being a bot is about helping humans. \n\n"
                                  "Available commands:\n"
                                  "/start: Register as admin\n"
                                  "/status: Show admin user")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def set(self, update, context):
        """ Change configuration of games"""
        command = context.args
        logger.info(f"Set command received: {command}")
        if len(command) == 2:
            self.postman.send('Settings', command)
        else:
            # Bug This statement doesn't get printed!
            update.message.reply_text("Please stay to the standard format: ```/set <variable> "
                                      "<value>.```")

    def make_controller(self, update):
        reply_keyboard = [['action'], ['left', 'right']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(text='Here is your game controller', reply_markup=reply_markup)

    def check_user_feedback(self,):
        """ Asks postman for user feedback to be printed out"""
        post = self.postman.request(Topics.OUTPUT)
        if post:
            msg = post['message']
            logger.debug(f"UserFeedback received. Now printing out: {msg}")
            if self.admin_user:
                self.bot.send_message(chat_id=self.admin_user, text=msg)
            else:
                logger.warning("No user registered as admin. Drop message!")

    def run(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.token, use_context=True)

        # Conversation handler for admin registration
        admin_registration = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                self.REGISTER: [CommandHandler('cancel', self.cancel),
                                MessageHandler(Filters.text, self.register)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        updater.dispatcher.add_handler(admin_registration)

        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        updater.dispatcher.add_handler(CommandHandler('set', self.set))
        updater.dispatcher.add_handler(CommandHandler('status', self.status))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.button))
        updater.dispatcher.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        while True:
            self.check_user_feedback()
