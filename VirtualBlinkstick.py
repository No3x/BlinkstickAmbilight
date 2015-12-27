import pyscreeze
import os
import Tkinter
import time
import collections
from PIL import Image, ImageDraw, ImageStat
from blinkstick import blinkstick

from socketIO_client import SocketIO, LoggingNamespace

import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

import pickle
import math

from PIL import Image, ImageDraw

class VirtualBlinkStick:
    def connect(self):
        return True

    def run(self):

        try:
            colors = []
            for k, v in currentColors.items():
                ( R, G, B ) = v
                R = math.floor(R);
                G = math.floor(G);
                B = math.floor(B);
                v = (R, G, B)
                colors.append( v )
                time.sleep(0.02)
                print k, v
        except KeyboardInterrupt:
            self.off()
            return
        with SocketIO('localhost', 7076, LoggingNamespace) as socketIO:
            socketIO.emit('setColors', {'colors': colors})
            socketIO.wait_for_callbacks(seconds=2)

root = Tkinter.Tk()
currentColors = collections.OrderedDict()

DEBUG = False
NUMLED = 60
BORDER = 50
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
STRIPE_LENGTH = (2 * HEIGHT) + (2 * WIDTH)


def saveImage(im, name):
    if DEBUG:
        start_time = time.time()
        im.save(name)
        elapsed_time = time.time() - start_time
        print "Saving ", name, " took ", elapsed_time


left = pyscreeze.screenshot(region=(0, 0, BORDER, HEIGHT))
left = left.rotate(-90)
saveImage(left, "border_left.jpeg")
top = pyscreeze.screenshot(region=(0, 0, WIDTH, BORDER))
saveImage(top, "border_top.jpeg")
right = pyscreeze.screenshot(region=(WIDTH - BORDER, 0, BORDER, HEIGHT))
right = right.rotate(90)
saveImage(right, "border_right.jpeg")
bottom = pyscreeze.screenshot(region=(0, HEIGHT - BORDER, WIDTH, BORDER))
bottom = bottom.rotate(180)
saveImage(bottom, "border_bottom.jpeg")
print os.path.dirname(__file__)

# blank_image = Image.new("RGB", (top.size[0] + right.size[0] + bottom.size[0] + left.size[0], top.size[1]))
all = Image.new("RGB", (STRIPE_LENGTH, BORDER))
all.paste(left, (0, 0))
all.paste(top, (HEIGHT, 0))
all.paste(right, (WIDTH + HEIGHT, 0))
all.paste(bottom, ((2 * HEIGHT) + WIDTH, 0))

draw = ImageDraw.Draw(all)
i = 0
count = 0
while (i <= STRIPE_LENGTH):

    # skip first chunk
    if i >= STRIPE_LENGTH / NUMLED:
        count = count + 1
        # draw.line((iteratedPixels, 0, iteratedPixels, height), fill=128, width=3)
        # draw.line((i, 0, i, BORDER), fill=128, width=3)
        #The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
        chunk = all.crop(box=(0, 0, STRIPE_LENGTH - i, BORDER))
        saveImage(chunk, "last_chunk.jpeg")
        currentColors[count] = ImageStat.Stat(chunk)._getmean()
        #print(i)
    i = i + STRIPE_LENGTH / NUMLED
print 'count:', count
assert count == NUMLED

del draw
saveImage(all, 'border_all.jpeg')

blinkstick2812 = VirtualBlinkStick()
if blinkstick2812.connect():
    blinkstick2812.run()
else:
    print "No BlinkSticks found"
