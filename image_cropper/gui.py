import tkinter as tk


class GUI(tk.Tk):
    init_title = 'Image Cropper'
    init_msg = '双击或者拖入选择图片'
    delay_ms = 3000

    def __init__(self):
        super().__init__()

        self.frame_main = tk.Frame(self)
        self.label_info = tk.Label(self.frame_main, text=self.init_msg)
        self.canvas_img = tk.Canvas(
            self.frame_main,
            # width=MAX_IMG_WIDTH, height=MAX_IMG_HEIGHT,
            # bg='pink'
        )

        self.config_gui()
        self.layout_gui()

    def raise_msg(self, msg: str):
        self.label_info.config(text=msg)
        self.label_info.after(
            self.delay_ms, lambda: self.label_info.config(text=self.init_msg)
        )

    def set_title(self, title: str | None = None):
        if title is None:
            self.title(self.init_title)
        else:
            self.title(f'{self.init_title} - {title}')

    def config_gui(self):
        self.set_title()
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.exit)
        self.bind('<Control-q>', lambda event: self.exit())

    def layout_gui(self):
        self.frame_main.pack()
        self.canvas_img.pack()
        self.label_info.pack()

    def center_gui(self):
        self.update()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(
            '+%d+%d'
            % ((screen_width - window_width) >> 1, (screen_height - window_height) >> 1)
        )

    def run(self):
        self.mainloop()

    def exit(self):
        self.destroy()

    def set_canvas_img(self, img):
        self.canvas_img.create_image(0, 0, anchor=tk.NW, image=img)
