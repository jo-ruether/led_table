import snake
from input import Input
from time import sleep
import time
from threading import Thread
import queue
import RPi.GPIO as GPIO
from collections import defaultdict
from snake import Garden
from pong_single import Pong
from telegram_bot import TelegramBot

# from telegram.ext import Updater, InlineQueryHandler, CommandHandler
# from telegram import InlineKeyboardButton


def application(input_q):
    # start() function returns if the game is over
    # Then return from the application so that the thread can terminate 
    #garden = Garden(input_q)
    #garden.start()
    pong = Pong(input_q)
    pong.start()
    return False

def inputs(input_q, b_pins=[7, 24]):
    """ Processes inputs by pushing them to the shared input_q 
    """
    # Save the last time that each button was pressed for debouncing
    last_pressed = {}
    # Initialize all buttons provided in the list of pins
    for pin in b_pins:
        last_pressed[pin] = time.time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin,GPIO.RISING)

    # Constantly check for Pressed buttons
    while True:
        if GPIO.input(b_pins[0]):
            if debounce(b_pins[0], last_pressed):
                input_q.put_nowait('right')
                print('right')
        elif GPIO.input(b_pins[1]):
            if debounce(b_pins[1], last_pressed):
                input_q.put_nowait('left')
                print('left')
        sleep(0.05)

def debounce(pin, last_pressed):
    """ Provides button debouncing
    """
    # Checks the last time that button has been pressed
    last_time = last_pressed[pin]
    # If time difference is reasonable, we assume that it is valid bress of a button
    if abs(time.time()-last_time) > 0.2:
        last_pressed[pin] = time.time()
        return True
    # If time difference is too small, the button is just bouncing
    else:
        return False
        
def telegram_inputs(input_q):
    bot = TelegramBot(input_q)
    bot.run()
    
input_q = queue.Queue(maxsize=3)
input_q.put('Running')

input_thread = Thread(target=inputs, args=(input_q,))
input_thread.setDaemon(True)
input_thread.start()

telegram_thread = Thread(target=telegram_inputs, args=(input_q,))
telegram_thread.setDaemon(True)
telegram_thread.start()

app_thread = Thread(target=application, args=(input_q,))
app_thread.setDaemon(True)
app_thread.start()

app_thread.join()

print("Done")

input_thread.join()
