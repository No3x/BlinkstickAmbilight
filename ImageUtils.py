import collections
import pyscreeze
import Tkinter
from PIL import Image, ImageDraw, ImageStat

root = Tkinter.Tk()

class ImageUtils:

    def __init__(self):
        root = Tkinter.Tk()
        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()

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
        for i, image in enumerate( (top, right, bottom, left) ):
            image_copy = Image.new(image.mode, image.size)
            image_copy.putdata(list(image.getdata()))
            out.append( (image_copy) )
        return out[0], out[1], out[2], out[3]

    def concat(self, images):
            if 1 >= len(images):
                raise ValueError('Pass more than one images to concat')

            rotated_images = [(image.rotate(90, expand=True) if image.height > image.width else image) for image in images]
            width_total = sum(int(v.size[0]) for v in rotated_images)
            concat_image = Image.new("RGB", (width_total, min(images[0].size)))
            # Image.paste(im, ( x, y) )
            width_processed = 0
            for image in rotated_images:
                concat_image.paste( image, ( width_processed, 0) )
                width_processed += image.size[0]
            return concat_image

