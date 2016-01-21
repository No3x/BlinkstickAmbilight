__author__ = 'No3x'

import collections

from PIL import ImageStat

from BlinkstickAmbilight.ImageUtils import ImageUtils


class Ambilight:
    def __init__(self, led_num, border):
        self.NUMLED = led_num
        self.BORDER = border
        self.imageUtils = ImageUtils()
        self.currentColors = collections.OrderedDict()
        self.current_image_all = None

    def run(self):
        self.current_image_all = self.imageUtils.concatStripe(self.imageUtils.makeImagesOfCorners(self.BORDER))
        self.currentColors = self.__calcColors()

    def __save(self, im, name):
        im.save(name, "PNG")

    def __calcColors(self):
        currentColors = collections.OrderedDict()
        for i, chunk in enumerate(self.imageUtils.splitImageIntoChunks(self.current_image_all, self.NUMLED), 0):
            currentColors[i] = ImageStat.Stat(chunk)._getmean()
        return currentColors
