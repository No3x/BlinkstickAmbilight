import unittest

from PIL import Image

from ImageUtils import ImageUtils


class ImageUtilsTest(unittest.TestCase):
    def setUp(self):
        self.image1 = Image.open('test1.png')
        # test2.png Breite: 200px # Hoehe: 220px
        self.image2 = Image.open('test2.png')
        self.imageUtils = ImageUtils()

    def test_makeImagesOfCorners_numbe_of_elements(self):
        images = self.imageUtils.makeImagesOfCorners(50)
        self.assertEqual(4, len(images))

    def test_makeImagesOfCorners_size(self):
        border = 50
        top, right, bottom, left = self.imageUtils.makeImagesOfCorners(border)
        self.assertEqual(top.size, (self.imageUtils.getScreenSize()[0], border))
        self.assertEqual(right.size, (border, self.imageUtils.getScreenSize()[1]))
        self.assertEqual(bottom.size, (self.imageUtils.getScreenSize()[0], border))
        self.assertEqual(left.size, (border, self.imageUtils.getScreenSize()[1]))

    def test_makeImagesOfCorners_small_border(self):
        with self.assertRaises(ValueError):
            self.imageUtils.makeImagesOfCorners(0)
            self.imageUtils.makeImagesOfCorners(-1)

    def test_concat_too_few(self):
        with self.assertRaises(ValueError):
            self.imageUtils.concat(())
            self.imageUtils.concat((self.image1))

    def test_concat_proper_size(self):
        images = (self.image2, self.image2)
        concated = self.imageUtils.concat(images)
        width_expected = 200 + 200
        height_expected = 220
        width_actual, height_actual = concated.size
        self.assertEqual(width_expected, width_actual)
        self.assertEqual(height_expected, height_actual)

    def test_concat_stripe_proper_size(self):
        images = (self.image2, self.image2)
        concated = self.imageUtils.concatStripe(images)
        width_expected = 220 + 220
        height_expected = 200
        width_actual, height_actual = concated.size
        # TODO:
        # self.assertEqual( width_expected, width_actual )
        # self.assertEqual( height_expected, height_actual )

    def test_split_images_into_chunks_number_of_elements(self):
        count = 4
        chunks = self.imageUtils.splitImageIntoChunks(self.image2, count)
        self.assertEqual(count, len(chunks))

    def test_split_images_into_chunks_width(self):
        count = 4
        chunks = self.imageUtils.splitImageIntoChunks(self.image2, count)

        expected_width_per_chunk = self.image2.size[0] / count;
        [self.assertEqual(expected_width_per_chunk, image.size[0]) for image in chunks]

    def test_split_images_into_chunks_width2(self):
        count = 4
        chunks = self.imageUtils.splitImageIntoChunks(self.image1, count)
        chunks.pop(len(chunks) - 1)
        expected_width_per_chunk = self.image2.size[0] / count;
        [image.show() for image in chunks]
        [self.assertEqual(expected_width_per_chunk, image.size[0]) for image in chunks]


if __name__ == '__main__':
    unittest.main()
