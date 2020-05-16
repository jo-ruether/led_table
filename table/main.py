from threading import Thread

from table.core.ConfigHandler import ConfigHandler
from table.core.Postman import Postman
from table.games.Menu import Menu

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(process)d-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)

# Config Handler manages access to config file (read and write)
config_handler = ConfigHandler()

# Postman manages topic-structed thread-safe communication
postman = Postman()

# Create output for matrix rendering
if config_handler.get_value("General", "table_present"):
    from table.core.output.Table import Table

    output = Table()
else:
    from table.core.output.Simulator import Simulator

    output = Simulator()

# Listen to USB controller if enabled
if config_handler.get_value("UsbInput", "enable"):
    from table.core.UsbInput import listen_to_usb_input

    usb_controller_thread = Thread(target=listen_to_usb_input, args=(postman, config_handler))
    usb_controller_thread.start()

# Start TelegramBot if enabled
if config_handler.get_value("TelegramBot", "enable"):
    from table.core.TelegramBot import TelegramBot

    bot = TelegramBot(postman, config_handler)
    telegram_thread = Thread(target=bot.run, args=(), daemon=True)
    telegram_thread.start()

# Start application thread with menu
menu = Menu(postman, output, config_handler)
app_thread = Thread(target=menu.start, args=())
app_thread.start()

# Wait for app thread to join
app_thread.join()
logger.info("All threads joined. Exiting.")
