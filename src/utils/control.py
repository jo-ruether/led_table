import RPi.GPIO as GPIO


class Control():
    def __init__(self, useButtons = False, buttonPins = []):
        self.useButtons = useButtons
        self.buttonPins = buttonPins
        if (self.useButtons):
            for pin in self.buttonPins:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.add_event_detect(pin,GPIO.RISING,callback=self.button_callback)

    def __del__(self):
        GPIO.cleanup()

    def button_callback(self,channel):
        print("Button",channel,"was pushed!")
