from BlinkstickAmbilight.PhysicalBlinkstick import Blinkstick2812
from BlinkstickAmbilight.Ambilight import Ambilight
from BlinkstickAmbilight.BlinkstickMock import BlinkstickMock

__author__ = 'No3x'

ambilight = Ambilight(60, 50)
#blinkstick = VirtualBlinkStick()
blinkstick = BlinkstickMock()

if blinkstick.connect():
    while True:
        try:
            ambilight.run()
            colors = ambilight.currentColors.items()
            blinkstick.setCurrentColors(colors)
            blinkstick.run();
        except KeyboardInterrupt:
            print 'Interrupted'
else:
    print "No BlinkSticks found"
