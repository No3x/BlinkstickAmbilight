__author__ = 'No3x'

import Tkinter

import pyscreeze
from PIL import Image

import ctypes
user32 = ctypes.windll.user32


def memoize(f):
    def wrapped(*args, **kwargs):
        if hasattr(wrapped, '_cached_val'):
            return wrapped._cached_val
        result = f(*args, **kwargs)
        wrapped._cached_val = result
        return result
    return wrapped

class ImageUtils:
    def __init__(self):
        self.WIDTH = self.getScreenSize()[0]
        self.HEIGHT = self.getScreenSize()[1]

    @memoize
    def getScreenSize(self):
        size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return size

    def makeImagesOfCorners(self, border):
        if 0 >= border:
            raise ValueError('Border is too small.')

        # start_x, start_y, breite, hoehe
        top = pyscreeze.screenshot(region=(0, 0, self.WIDTH, border))
        right = pyscreeze.screenshot(region=(self.WIDTH - border, 0, border, self.HEIGHT))
        bottom = pyscreeze.screenshot(region=(0, self.HEIGHT - border, self.WIDTH, border))
        left = pyscreeze.screenshot(region=(0, 0, border, self.HEIGHT))

        # Loop over ImageCrop to make Images
        out = []
        for i, image in enumerate((top, right, bottom, left)):
            image_copy = Image.new(image.mode, image.size)
            image_copy.putdata(list(image.getdata()))
            out.append((image_copy))
        return out

    def concat(self, images):
        if 1 >= len(images):
            raise ValueError('Pass more than one images to concat')

        width_total = sum(int(v.size[0]) for v in images)
        concat_image = Image.new("RGB", (width_total, images[0].size[1]))
        # Image.paste(im, ( x, y) )
        width_processed = 0
        for image in images:
            concat_image.paste(image, (width_processed, 0))
            width_processed += image.size[0]
        return concat_image

    def concatStripe(self, images):
        return self.concat(
                [(image.rotate(90, expand=True) if image.height > image.width else image) for image in images])

    def splitImageIntoChunks(self, image, count):
        chunks = []
        i = 0
        chunks_done = 0
        width, height = image.size
        div = width / count
        while (i <= width - 1 * div):
            # left, upper, right, and lower pixel
            left = i
            right = left + div;
            if (count == chunks_done - 1):
                right = width
            upper = 0
            chunk = image.crop(box=(left, upper, right, height))
            chunks.append(chunk)
            chunks_done = chunks_done + 1
            i = i + div
        assert chunks_done == count
        return chunks
