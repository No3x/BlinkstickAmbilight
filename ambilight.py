import collections
import pyscreeze
import Tkinter
from PIL import Image, ImageDraw, ImageStat

from ImageUtils import ImageUtils

__author__ = 'Christian'

root = Tkinter.Tk()

class Ambilight:
    def __init__(self, led_num, border):
        self.NUMLED = led_num
        self.BORDER = border
        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()
        self.STRIPE_LENGTH = (2 * self.HEIGHT) + (2 * self.WIDTH)
        self.imageUtils = ImageUtils()
        self.currentColors = collections.OrderedDict()
        self.current_image_all = None

    def run(self):
        top, right, bottom, left = self.__makeImages()
        self.__concat(top, right, bottom, left)
        self.__drawBalkens()
        self.__calcColors()

    def __makeImages(self):
        return self.imageUtils.makeImagesOfCorners( self.BORDER )

    def __doMath(self, im):
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        del draw

    def __save(self, im, name):
        im.save(name, "PNG")

    def __concat(self, top, right, bottom, left):
        (top, right, bottom, left).count()
        self.current_image_all = self.imageUtils.concat( (top, right, bottom, left) )

    def __drawBalkens(self):
        draw = ImageDraw.Draw(self.current_image_all)
        width, height = self.current_image_all.size
        div = width / self.NUMLED
        iteratedPixels = 0
        for pixel in list(range(0, width)):
            iteratedPixels = iteratedPixels + 1
            if iteratedPixels % div == 0:
                draw.line((iteratedPixels, 0, iteratedPixels, height), fill=128, width=3)
        del draw

    def __improvedMedian(self, im):
        # grab width and height
        width, height = im.size

        # make a list of all pixels in the image
        pixels = im.load()
        data = []
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                data.append(cpixel)
        r = 0
        g = 0
        b = 0
        counter = 0

        # loop through all pixels
        # if alpha value is greater than 200/255, add it to the average
        # (note: could also use criteria like, if not a black pixel or not a white pixel...)
        for x in range(len(data)):
            try:
                if data[x][3] > 200:
                    r+=data[x][0]
                    g+=data[x][1]
                    b+=data[x][2]
            except:
                r+=data[x][0]
                g+=data[x][1]
                b+=data[x][2]

            counter+=1

        # compute average RGB values
        rAvg = r/counter
        gAvg = g/counter
        bAvg = b/counter

        return [rAvg, gAvg, bAvg]

    def __calcColors(self):
        i = 0
        chunks_done = 0
        width, height = self.current_image_all.size
        div = width / self.NUMLED
        while (i <= self.STRIPE_LENGTH-1*div):
            # left, upper, right, and lower pixel
            left = i
            right = left+div;
            if( self.NUMLED == chunks_done-1 ):
                right = self.STRIPE_LENGTH
            lower = self.BORDER
            upper = 0
            chunk = self.current_image_all.crop(box=(left, upper, right, lower ) )
            #hex = self.__improvedMedian(chunk)#ImageStat.Stat(chunk)._getmean()
            self.currentColors[chunks_done] = ImageStat.Stat(chunk)._getmean()
            chunks_done = chunks_done + 1
            i = i + div
        assert chunks_done == self.NUMLED