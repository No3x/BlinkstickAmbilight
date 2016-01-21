from BlinkstickAmbilight.Ambilight import Ambilight
from BlinkstickAmbilight.VirtualBlinkstick import VirtualBlinkStick

__author__ = 'No3x'

ambilight = Ambilight(60, 50)
blinkstick = VirtualBlinkStick()
blinkstick.connect()

while True:
    try:
        ambilight.run()
        colors = ambilight.currentColors.items()
        blinkstick.setCurrentColors(colors)
        blinkstick.run();
    except KeyboardInterrupt:
        print 'Interrupted'
