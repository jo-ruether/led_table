import RPi.GPIO as GPIO
import queue

class Input:
    def __init__(self, button_pins=[24, 26]):
    # Input queue stores pin_number of pressed buttons
        self.input_queue = queue.Queue(maxsize=2)
        for pin in button_pins:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin,GPIO.RISING)
            if GPIO.event_detected(pin):
                self.input_queue(pin)