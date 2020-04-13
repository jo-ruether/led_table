from threading import Thread
import queue

from table.telegram_bot import TelegramBot
from table.games.Menu import Menu
from table.utils.output import Output


def application(input_q, output):
    # start() function returns if the game is over
    # Then return from the application so that the thread can terminate 
    menu = Menu(input_q, output)
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


def telegram_inputs(input_q):
    bot = TelegramBot(input_q)
    bot.run()


# Create output class to pass to all threads
output = Output()

input_q = queue.Queue(maxsize=3)
input_q.put('Running')

# This is for hardware switches only
#input_thread = Thread(target=inputs, args=(input_q,), daemon=True)
#input_thread.start()

telegram_thread = Thread(target=telegram_inputs, args=(input_q,), daemon=True)
telegram_thread.start()

app_thread = Thread(target=application, args=(input_q, output))
app_thread.start()

app_thread.join()

print("Done")
