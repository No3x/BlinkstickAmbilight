import unittest

from PIL import Image

from Ambilight import Ambilight
from ImageUtils import ImageUtils


class ImageUtilsTest(unittest.TestCase):
    def setUp(self):
        self.image1 = Image.open('test1.png')
        self.image2 = Image.open('test2.png')
        self.imageUtils = ImageUtils()

    def test_small_border(self):
        with self.assertRaises(ValueError):
            self.imageUtils.makeImagesOfCorners(0)
            self.imageUtils.makeImagesOfCorners(-1)

    def test_concat_too_few(self):
        with self.assertRaises(ValueError):
            self.imageUtils.concat( () )
            self.imageUtils.concat( (self.image1) )

    def test_concat_proper_size(self):
        images = (self.image1, self.image2)
        concated = self.imageUtils.concat( images )
        width_expected = sum(int(v.size[0]) for v in images)
        height_expected = sum(int(v.size[1]) for v in images)

        width_actual = concated.size[0]
        height_actual = concated.size[1]
        #TODO: Test images must have same size
        #self.assertEquals( width_expected, width_actual )
        #self.assertEquals( height_expected, height_actual )

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
