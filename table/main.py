from threading import Thread
import queue

from table.TelegramBot import TelegramBot
from table.games.Menu import Menu
from table.OutputSim import OutputSim
from table.Postman import Postman


def application(postman, output):
    # start() function returns if the game is over
    # Then return from the application so that the thread can terminate 
    menu = Menu(postman, output)
    menu.start()

    output.emptyMatrix()

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
#                 input_q.put_nowait('right')
#                 print('right')
#         elif GPIO.input(b_pins[1]):
#             if debounce(b_pins[1], last_pressed):
#                 input_q.put_nowait('left')
#                 print('left')
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


def telegram(postman):
    bot = TelegramBot(postman)
    bot.run()


# Create postman for thread communication
postman = Postman(['Output', 'UserInput', 'Settings', 'UserFeedback'])

# Create output for matrix rendering
output = OutputSim()

telegram_thread = Thread(target=telegram, args=(postman,), daemon=True)
telegram_thread.start()

app_thread = Thread(target=application, args=(postman, output))
app_thread.start()

app_thread.join()

print("Done")
