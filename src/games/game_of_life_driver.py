import game_of_life as gol
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
    print("Button was pushed")
    w = gol.World()
    w.start()

GPIO.add_event_detect(24,GPIO.RISING,callback=button_callback)
# except KeyboardInterrupt:
#    GPIO.cleanup()
message = input("Press enter to quit\n\n")
GPIO.cleanup()
