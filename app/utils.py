"""
Image processing program
"""
import os

from PIL import Image, ImageTk, UnidentifiedImageError

from .constants import *

__all__ = [
    'ImageUtil',
    'UnidentifiedImageError'
]


class ImageUtil:
    def __init__(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError(file)
        # elif not os.path.splitext(file)[1] in EXTENSION_NAME:
        #     raise UnidentifiedImageError

        # 此处让它报错吧，否则会创建新对象，后边出现更严重的错误
        self.image = Image.open(file)
        self.file = file
        if (extn := os.path.splitext(file)[1]) != '':
            self.ext = extn
            self.extn = [(extn[1:].upper(), extn), ('*', '.*')]
        else:
            self.ext = ''
            self.extn = [('*', '.*')]

        self.new_size, self.ratio, self.image_auto_scale = self.auto_scale()

    def auto_scale(self):
        width, height = self.image.size
        if (w_h := width / height) >= RATIO_SCREEN_W_H:
            new_width = MAX_IMG_WIDTH
            new_height = new_width / w_h
            return (new_width, new_height), width / new_width, self.image.resize(
                (round(new_width), round(new_height)))
        else:
            new_height = MAX_IMG_HEIGHT
            new_width = new_height * w_h
            return (new_width, new_height), height / new_height, self.image.resize(
                (round(new_width), round(new_height)))

    def img_for_tk(self):
        return ImageTk.PhotoImage(self.image_auto_scale)

    def crop_img(self, x_b_e, y_b_e):
        x_b, x_e = sorted(x_b_e)
        y_b, y_e = sorted(y_b_e)
        size = (x_b * self.ratio, y_b * self.ratio, x_e * self.ratio, y_e * self.ratio)
        return self.image.crop(size)
