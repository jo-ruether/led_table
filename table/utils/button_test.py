import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        if GPIO.input(12):
            print("Port is high")
        else:
            print("Port is low") 
        sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()

