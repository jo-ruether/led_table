from threading import Thread
import json

from table.TelegramBot import TelegramBot
from table.games.Menu import Menu
from table.Postman import Postman
from table.ConfigHandler import ConfigHandler

from table.UsbInput import listen_to_usb_input

try:
    from table.OutputTable import OutputTable
except (ImportError, NotImplementedError):
    from table.OutputSim import OutputSim

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(process)d-%(levelname)s-%(message)s')


def application(postman, output, config_handler):
    # start() function returns if the game is over
    # Then return from the application so that the thread can terminate 
    menu = Menu(postman, output, config_handler)
    menu.start()

    output.emptyMatrix()


def telegram(postman, config_handler):
    bot = TelegramBot(postman, config_handler)
    bot.run()

# def inputs(input_q, b_pins=[7, 24]):
#     """ Processes inputs by pushing them to the shared input_q
#     """
#     # Save the last time that each button was pressed for debouncing
#     last_pressed = {}
#     # Initialize all buttons provided in the list of pins
#     for pin in b_pins:
#         last_pressed[pin] = time.time()
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#         GPIO.add_event_detect(pin, GPIO.RISING)
#
#     # Constantly check for Pressed buttons
#     while True:
#         if GPIO.input(b_pins[0]):
#             if debounce(b_pins[0], last_pressed):
#                 input_q.put_nowait(CMD.RIGHT)
#                 print(CMD.RIGHT)
#         elif GPIO.input(b_pins[1]):
#             if debounce(b_pins[1], last_pressed):
#                 input_q.put_nowait(CMD.LEFT)
#                 print(CMD.LEFT)
#         sleep(0.05)
#
#
# def debounce(pin, last_pressed):
#     """ Provides button debouncing
#     """
#     # Checks the last time that button has been pressed
#     last_time = last_pressed[pin]
#     # If time difference is reasonable, we assume that it is valid bress of a button
#     if abs(time.time() - last_time) > 0.2:
#         last_pressed[pin] = time.time()
#         return True
#     # If time difference is too small, the button is just bouncing
#     else:
#         return False


config_handler = ConfigHandler("config.json")

# Create output for matrix rendering
if config_handler.get_value("General", "table_present"):
    try:
        output = OutputTable()
    except:
        print("Unable to create table output")
        output = OutputSim()
else:
    output = OutputSim()

# Create postman for thread communication
postman = Postman()

usb_controller_thread = Thread(target=listen_to_usb_input, args=(postman, config_handler))
usb_controller_thread.start()

telegram_thread = Thread(target=telegram, args=(postman, config_handler), daemon=True)
telegram_thread.start()

app_thread = Thread(target=application, args=(postman, output, config_handler))
app_thread.start()

app_thread.join()

print("Done")
