"""
The application
"""
import os
from tkinter import filedialog

try:
    import windnd
except ImportError:
    windnd = None

from .constants import DIALOG_EXT_OPT
from .gui import GUI
from .utils import ImageUtil


class Application(GUI):

    def __init__(self):
        super().__init__()

        if windnd is not None:
            windnd.hook_dropfiles(self, func=self.drag_img, force_unicode=True)

        self.config_gui()

        self.left_mouse_down_x = 0
        self.left_mouse_down_y = 0
        self.left_mouse_up_x = 0
        self.left_mouse_up_y = 0
        self.moving_mouse_x = None
        self.moving_mouse_y = None
        self.sole_rectangle = None

        self.image = None
        self.image_tk = None

    def config_gui(self):
        super().config_gui()

        self.canvas_img.bind('<Button-1>', self.left_mouse_down)  # 鼠标左键按下
        self.canvas_img.bind('<ButtonRelease-1>', self.left_mouse_up)  # 鼠标左键释放
        self.canvas_img.bind('<Button-2>', self.right_mouse_down)  # 鼠标右键按下
        self.canvas_img.bind('<ButtonRelease-2>', self.right_mouse_up)  # 鼠标右键释放
        self.canvas_img.bind('<B1-Motion>', self.moving_mouse)  # 鼠标左键按下并移动
        self.bind('<Control-o>', lambda event: self.open_img())
        self.bind('<Double-Button-1>', lambda event: self.open_img())
        self.bind('<Control-s>', lambda event: self.convert())

    def left_mouse_down(self, event):
        # 鼠标左键按下
        self.left_mouse_down_x = event.x
        self.left_mouse_down_y = event.y

    def left_mouse_up(self, event):
        self.left_mouse_up_x = event.x
        self.left_mouse_up_y = event.y

    def drag_img(self, files):
        for file in files:
            if os.path.isfile(file):
                self._open_img(file)
                break

    def open_img(self):
        img_path = filedialog.askopenfilename(filetypes=DIALOG_EXT_OPT)
        if img_path == '':  # if close the dialog window
            self.raise_msg('Cancel to open.')
            return
        self._open_img(img_path)

    def _open_img(self, img_path):
        try:
            self.image = ImageUtil(img_path)
        except Exception as e:
            self.raise_msg(f'[ERROR] {e}')
            print(e)
            return
        self.set_title(img_path.replace('/', os.sep))
        self.canvas_img.config(width=self.image.new_size[0], height=self.image.new_size[1])
        self.image_tk = self.image.img_for_tk()  # must be global variable
        self.set_canvas_img(self.image_tk)
        self.canvas_img.delete(self.sole_rectangle)

        self.center_gui()

    def convert(self):
        if self.image is None:
            self.raise_msg('No image got.')
            return
        save_path = filedialog.asksaveasfilename(filetypes=self.image.extn)
        if save_path == '':  # if close the dialog window
            self.raise_msg('Cancel to save.')
            return
        self.image.crop_img(
            [self.left_mouse_down_x, self.left_mouse_up_x],
            [self.left_mouse_down_y, self.left_mouse_up_y]
        ).save(save_path + self.image.ext)

    def moving_mouse(self, event):
        # 鼠标左键按下并移动
        # print(event.x, event.y)
        self.moving_mouse_x = event.x
        self.moving_mouse_y = event.y

        # if self.sole_rectangle is not None:
        self.canvas_img.delete(self.sole_rectangle)  # 删除前一个矩形框
        self.sole_rectangle = self.canvas_img.create_rectangle(  # 创建新的矩形框
            self.left_mouse_down_x,
            self.left_mouse_down_y,
            self.moving_mouse_x,
            self.moving_mouse_y,
            outline='red'  # 矩形框颜色
        )

    def right_mouse_down(self, event):
        # 鼠标右键按下
        pass

    def right_mouse_up(self, event):
        # 鼠标右键释放
        pass
