import collections

__author__ = 'Christian'
import pyscreeze
import Tkinter
from PIL import Image, ImageDraw, ImageStat

root = Tkinter.Tk()

class Ambilight:
    def __init__(self, led_num, border):
        self.NUMLED = led_num
        self.BORDER = border
        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()
        self.STRIPE_LENGTH = (2 * self.HEIGHT) + (2 * self.WIDTH)
        self.currentColors = collections.OrderedDict()
        self.current_image_all = None

    def run(self):
        top, right, bottom, left = self.__makeImages()
        # self.__save(right, "right_debug.png")
        self.__concat(top, right, bottom, left)
        # self.__drawBalkens()
        self.__calcColors()

    def __makeImages(self):
        # start_x, start_y, breite, hoehe
        top = pyscreeze.screenshot(region=(0, 0, self.WIDTH, self.BORDER))
        right = pyscreeze.screenshot(region=(self.WIDTH - self.BORDER, 0, self.BORDER, self.HEIGHT))
        bottom = pyscreeze.screenshot(region=(0, self.HEIGHT - self.BORDER, self.WIDTH, self.BORDER))
        left = pyscreeze.screenshot(region=(0, 0, self.BORDER, self.HEIGHT))
        return top, right, bottom, left


    def __doMath(self, im):
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        del draw

    def __save(self, im, name):
        im.save(name, "PNG")

    def __concat(self, top, right, bottom, left):
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
        # print top.size[0] + right.size[0] + bottom.size[0]
        self.current_image_all = blank_image

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
        count = 0
        width, height = self.current_image_all.size
        div = width / self.NUMLED
        while (i <= self.STRIPE_LENGTH):
            # skip first chunk
            if i >= self.STRIPE_LENGTH / self.NUMLED:
                count = count + 1
                chunk = self.current_image_all.crop(box=(count*div, 0, self.STRIPE_LENGTH - (self.NUMLED-count)*div, self.BORDER))
                #hex = self.__improvedMedian(chunk)#ImageStat.Stat(chunk)._getmean()
                self.currentColors[count] = ImageStat.Stat(chunk)._getmean()
            i = i + self.STRIPE_LENGTH / self.NUMLED
        assert count == self.NUMLED