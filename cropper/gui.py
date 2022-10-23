"""
The main GUI program
"""

import tkinter as tk
from tkinter import filedialog

from cropper.constants import *

__all__ = [
    'GUI',
    'ask_open_path',
    'ask_save_path'
]


def ask_open_path():
    return filedialog.askopenfilename(filetypes=DIALOG_EXT_OPT)


def ask_save_path(filetypes):
    return filedialog.asksaveasfilename(filetypes=filetypes)


class GUI(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        # self.geometry('%dx%d' % (MAX_IMG_WIDTH, MAX_IMG_HEIGHT))
        self.resizable(False, False)

        self.frame_main = tk.Frame(self)
        self.canvas_img = tk.Canvas(self.frame_main,
                                    # width=MAX_IMG_WIDTH, height=MAX_IMG_HEIGHT,
                                    # bg='pink'
                                    )

    def set_ui(self):
        self.frame_main.pack()
        self.canvas_img.pack()

        self.center_ui()

    def center_ui(self):
        self.update()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry('+%d+%d' % (
            (screen_width - window_width) >> 1,
            (screen_height - window_height) >> 1
        ))

    def run(self):
        self.mainloop()

    def set_canvas_img(self, img):
        self.canvas_img.create_image(0, 0, anchor=tk.NW, image=img)
