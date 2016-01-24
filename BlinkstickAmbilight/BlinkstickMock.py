import collections

from BlinkstickAmbilight.ImageUtils import ImageUtils

__author__ = 'Christian'
import Tkinter as tk
import time
from PIL import Image, ImageDraw, ImageStat

NUMLED = 60
BORDER = 50

root = tk.Tk()
root.title = "Game"
root.resizable(0,0)
root.wm_attributes("-topmost", 1)
screensize = ImageUtils().getScreenSize()
root.geometry("%dx%d+0+0" % (screensize[0], screensize[1]))


canvas = tk.Canvas(root, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

class Tile:
    def __init__(self, canvas, color, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, x, y)

    def draw(self):
        self.canvas.after(50, self.draw)

class BlinkstickMock():

    currentColors = collections.OrderedDict()

    def setCurrentColors(self, currentColors):
        self.currentColors = currentColors

    def connect(self):
        print "connected"
        return True

    def run(self):
        width, height = ImageUtils().getScreenSize()
        div = width / NUMLED
        iteratedPixels = 0
        row = 1
        for k, v in self.currentColors:
            iteratedPixels = iteratedPixels + div
            (R, G, B) = v
            ct_hex = "%02x%02x%02x" % tuple(v)
            bg_colour = '#' + "".join(ct_hex)
            if( (k % 10) is 0 ):
                row = row+1
                iteratedPixels = 0
            ball = Tile(canvas, bg_colour, iteratedPixels, row*25)
            ball.draw()
            time.sleep(0.02)
            print k, v
        root.update()
