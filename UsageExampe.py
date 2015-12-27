from Ambilight import Ambilight
from VirtualBlinkstick import VirtualBlinkStick
import math
import time

ambilight = Ambilight(60, 50)
blinkstick = VirtualBlinkStick()
blinkstick.connect()

while True:
    try:
        ambilight.run()
        colors = ambilight.currentColors.items()
        blinkstick.setCurrentColors( colors )
        blinkstick.run();
    except KeyboardInterrupt:
        print 'Interrupted'

