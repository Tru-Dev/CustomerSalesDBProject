from typing import Callable, Optional
import tkinter as tk

from . import config
from .db_classes import session

class UIHost():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.frame = Welcome(self, self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.filemenu.add_command(label="Customers", underline=0)
        self.filemenu.add_command(label="Products", underline=0)
        self.filemenu.add_command(label="Sales", underline=0)
        self.filemenu.add_command(label="Welcome", underline=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", underline=0, command=self.root.destroy)
        self.menu.add_cascade(label="File", menu=self.filemenu, underline=0)
        self.root.minsize(400, 300)
        self.root.geometry("640x480")
        self.root.mainloop()

    def switchFrameCallback(self, frameClass: type[tk.Frame]) -> Callable[[], None]:
        pass

class Welcome(tk.Frame):
    def __init__(self, host: UIHost, master: Optional[tk.Tk]=None):
        super().__init__(master)
        self.master = master
        self.master.title(config.config.windowtitle.format("Welcome"))
        self.pack(fill=tk.BOTH, expand=True)
        # self.create_widgets()

    # def create_widgets(self):
        # self.


