__author__ = 'Christian'
import pyscreeze
import Tkinter
from PIL import Image, ImageDraw

root = Tkinter.Tk()


class Ambilight:
    def __init__(self):
        self.NUMLED = 60
        self.BORDER = 50
        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()

    def run(self):
        top, right, bottom, left = self.makeImages()
        # self.doMath(top)
        #self.save(top)
        self.concat(top, right, bottom, left)
        self.drawBalkens()

    def makeImages(self):
        # start_x, start_y, breite, hoehe
        top = pyscreeze.screenshot(region=(0, 0, self.WIDTH, self.BORDER), imageFilename='top.png')
        right = pyscreeze.screenshot(region=(self.WIDTH - self.BORDER, 0, self.BORDER, self.HEIGHT),
                                     imageFilename='right.png')
        bottom = pyscreeze.screenshot(region=(0, self.HEIGHT - self.BORDER, self.WIDTH, self.BORDER),
                                      imageFilename='bottom.png')
        left = pyscreeze.screenshot(region=(0, 0, self.BORDER, self.HEIGHT), imageFilename='left.png')
        return top, right, bottom, left


    def doMath(self, im):
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        del draw

    def save(self, im):
        # write
        im.save('top_after.png', "PNG")

    def concat(self, top, right, bottom, left):
        right = right.rotate(90)
        bottom = bottom.rotate(-180)
        left = left.rotate(-90)
        # Image.new("RGB", (width, height) )
        # top.size[0] = width, top.size[1] = height
        blank_image = Image.new("RGB", (top.size[0] + right.size[0] + bottom.size[0] + left.size[0], top.size[1]))
        # Image.paste(im, ( x, y) )
        blank_image.paste(top, (0, 0))
        blank_image.paste(right, (top.size[0], 0))
        blank_image.paste(bottom, (top.size[0] + right.size[0], 0))
        blank_image.paste(left, (top.size[0] + right.size[0] + bottom.size[0], 0))
        print top.size[0] + right.size[0] + bottom.size[0]
        blank_image.save('all.png')

    def drawBalkens(self):
        im = Image.open('all.png')
        draw = ImageDraw.Draw(im)
        width, height = im.size
        div = width / self.NUMLED
        iteratedPixels = 0
        for pixel in list(range(0, width)):
            iteratedPixels = iteratedPixels + 1
            if iteratedPixels % div == 0:
                draw.line((iteratedPixels, 0, iteratedPixels, height), fill=128, width=3)

        del draw
        im.save('all.png')


Ambilight().run()
