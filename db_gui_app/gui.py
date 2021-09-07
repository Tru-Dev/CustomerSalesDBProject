from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from . import config, db_classes as db

class UIHost():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#eee")
        self.style.configure("TLabel", background="#eee")
        self.style.configure("Danger.TButton", foreground="lightgray")
        self.style.configure("Danger.TButton", background="#e00")
        self.style.map("Danger.TButton",
            foreground=[("active", "white")],
            background=[("active", "red")]
        )
        self.frame = Welcome(self, self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.filemenu.add_command(
            label="Customers", underline=0, command=self.switch_frame_callback(CustomersView)
        )
        self.filemenu.add_command(
            label="Products", underline=0, command=self.switch_frame_callback(ProductsView)
        )
        self.filemenu.add_command(
            label="Sales", underline=0, command=self.switch_frame_callback(SalesView)
        )
        self.filemenu.add_command(
            label="Welcome", underline=0, command=self.switch_frame_callback(Welcome)
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", underline=0, command=self.root.destroy)
        self.menu.add_cascade(label="File", menu=self.filemenu, underline=0)
        self.root.minsize(400, 300)
        self.root.geometry("640x480")
        self.root.mainloop()

    def switch_frame_callback(self, frameClass: type[tk.Frame]) -> Callable[[], None]:
        def callback_func():
            self.frame.destroy()
            self.frame = frameClass(self, self.root)
        return callback_func

class Welcome(ttk.Frame):
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
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=1, row=1, sticky="N")
        self.main_label = ttk.Label(
            self.main_frame, text="Customer Sales DB", font=("Segoe UI", 15), padding=(5,10)
        )
        self.main_label.grid(column=0, row=0)
        self.customers_btn = ttk.Button(
            self.main_frame, text="Customers", command=self.host.switch_frame_callback(CustomersView)
        )
        self.customers_btn.grid(column=0, row=1, sticky="NEW")
        self.products_btn = ttk.Button(
            self.main_frame, text="Products", command=self.host.switch_frame_callback(ProductsView)
        )
        self.products_btn.grid(column=0, row=2, sticky="NEW")
        self.sales_btn = ttk.Button(
            self.main_frame, text="Sales", command=self.host.switch_frame_callback(SalesView)
        )
        self.sales_btn.grid(column=0, row=3, sticky="NEW")
        self.exit_btn = ttk.Button(
            self.main_frame, text="Exit", command=self.master.destroy, style="Danger.TButton"
        )
        self.exit_btn.grid(column=0, row=4, sticky="NEW")

class SearchWidget(ttk.Frame):
    def __init__(self, master: "TableView"):
        super().__init__(master)
        self.master: "TableView" = master
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)
        self.queryvar = tk.StringVar(self)
        self.searchbox = ttk.Entry(self, textvariable=self.queryvar)
        self.searchbox.grid(column=0, row=0, sticky="NESW")
        self.searchbox.bind("<Return>", lambda event: self.search_callback())
        self.submitbtn = ttk.Button(self, text="Search", command=self.search_callback)
        self.submitbtn.grid(column=1, row=0, sticky="NESW")
        self.label = ttk.Label(self, text="Column to Search:")
        self.label.grid(column=2, row=0, sticky="NESW")
        self.colvar = tk.StringVar(self)
        self.colselect = ttk.Combobox(
            self, values=[s.replace("_", " ").title() for s in self.master.cols],
            textvariable=self.colvar
        )
        self.colselect.current(1)
        self.colselect.grid(column=3, row=0, sticky="NESW")
    
    def search_callback(self):
        self.master.search_table(self.queryvar.get(), self.master.cols[self.colselect.current()])

class BaseForm(tk.Frame):
    pass

class TableView(tk.Frame):
    """
    Base class for the data views for each table in the database.
    DO NOT INSTANTIATE DIRECTLY!!!
    """
    db_class = None
    form = None

    def __init__(self, host: UIHost, master: Optional[tk.Tk]=None):
        super().__init__(master)
        self.master = master
        self.host = host
        self.master.title(config.config.windowtitle.format(self.db_class.__name__ + "s"))
        self.pack(fill=tk.BOTH, expand=True)
        self.cols: list[str] = self.db_class.__table__.c.keys()
        self.create_widgets()

    def create_widgets(self):
        self.search = SearchWidget(self)
        self.search.pack(fill=tk.X, padx=20, pady=(20, 5))

    def search_table(self, query: str, column: str):
        print(f"q: {query}\tc: {column}")

class CustomersView(TableView):
    db_class = db.Customer

class ProductsView(TableView):
    db_class = db.Product

class SalesView(TableView):
    db_class = db.Sale
