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
        self.host = host
        self.master.title(config.config.windowtitle.format("Welcome"))
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=3)
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(column=1, row=1, sticky="N")
        self.main_label = tk.Label(
            self.main_frame, text="Customer Sales DB", font=("Segoe UI", 15), pady=10
        )
        self.main_label.grid(column=0, row=0)
        self.customers_btn = tk.Button(self.main_frame, text="Customers")
        self.customers_btn.grid(column=0, row=1, sticky="NEW")
        self.products_btn = tk.Button(self.main_frame, text="Products")
        self.products_btn.grid(column=0, row=2, sticky="NEW")
        self.sales_btn = tk.Button(self.main_frame, text="Sales")
        self.sales_btn.grid(column=0, row=3, sticky="NEW")
        self.exit_btn = tk.Button(
            self.main_frame, text="Exit", fg="white", bg="red", command=self.master.destroy
        )
        self.exit_btn.grid(column=0, row=4, sticky="NEW")
