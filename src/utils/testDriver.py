from output import Output
#from control import Control
import time
import random
import neopixel
testOutput = Output()

#testInput = Control(useButtons = True,buttonPins = [18])


while(True):
    x = random.randint(0,11)
    y = random.randint(0,11)

    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)


    testOutput.setValueRGB(x,y,(r,g,b))
    time.sleep(0.1)
    
