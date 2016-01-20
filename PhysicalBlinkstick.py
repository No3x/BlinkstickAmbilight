__author__ = 'No3x'
import math
import time

from blinkstick import blinkstick

from Ambilight import Ambilight
from Prompt import Prompt

NUMLED = 4
BORDER = 50


class Blinkstick2812(blinkstick.BlinkStickPro):
    def __init__(self, ambilight=None, r_led_count=None, max_rgb_value=None, delay=None):
        self.ambilight = ambilight
        blinkstick.BlinkStickPro.__init__(self, r_led_count=r_led_count, max_rgb_value=max_rgb_value, delay=delay)

    def insureWSMode(self):
        mode = self.bstick.get_mode()
        if mode is not 2:
            if Prompt().prompt.query_yes_no("Should I set the proper mode for you now? (Mode 2 : WS2812)", "no"):
                print "Set mode to 2"
                self.bstick.set_mode(2)
                print "Please reconnect your BlinkStick"
            else:
                raise ValueError(
                        'BlinkStick is not in proper mode (see https://www.blinkstick.com/help/tutorials/blinkstick-pro-modes). Exit')

    def __round(self, colors):
        roundedColors = []
        for k, v in colors:
            (R, G, B) = v
            R = math.floor(R)
            G = math.floor(G)
            B = math.floor(B)
            v = (R, G, B)
            roundedColors.append(v)
        return roundedColors

    def run(self):
        print "Running.."
        try:
            while 1:
                self.send_data_all()
                self.ambilight.run()
                # colors = collections.OrderedDict()
                # colors[0] = (161, 174, 188)
                # colors[1] = (161, 174, 188)
                # colors[2] = (161, 174, 188)
                # colors[3] = (161, 174, 188)
                colors = ambilight.currentColors
                for k, v in colors.items():
                    (R, G, B) = v
                    R = int(R)
                    G = int(G)
                    B = int(B)
                    self.set_color(0, k - 1, R, G, B)
                time.sleep(0.02)
        except KeyboardInterrupt:
            self.off()
            return


ambilight = Ambilight(NUMLED, BORDER)
blinkstick2812 = Blinkstick2812(ambilight=ambilight, r_led_count=NUMLED, max_rgb_value=255, delay=0.002)
if blinkstick2812.connect():
    blinkstick2812.insureWSMode()
    blinkstick2812.run()
else:
    print "No BlinkSticks found"
