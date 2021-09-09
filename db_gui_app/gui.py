from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from sqlalchemy import inspect
import tkintertable as tktb

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
        self.root.minsize(640, 480)
        self.root.geometry("800x600")
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

# Obsoleted by tkintertable filtering
# class SearchWidget(ttk.Frame):
#     def __init__(self, master: "TableView"):
#         super().__init__(master)
#         self.master: "TableView" = master
#         self.columnconfigure(0, weight=2)
#         self.columnconfigure(1, weight=0)
#         self.columnconfigure(2, weight=0)
#         self.columnconfigure(3, weight=0)
#         self.queryvar = tk.StringVar(self)
#         self.searchbox = ttk.Entry(self, textvariable=self.queryvar)
#         self.searchbox.grid(column=0, row=0, sticky="NESW")
#         self.searchbox.bind("<Return>", lambda event: self.search_callback())
#         self.submitbtn = ttk.Button(self, text="Search", command=self.search_callback)
#         self.submitbtn.grid(column=1, row=0, sticky="NESW")
#         self.label = ttk.Label(self, text="Column to Search:")
#         self.label.grid(column=2, row=0, sticky="NESW")
#         self.colvar = tk.StringVar(self)
#         self.colselect = ttk.Combobox(
#             self, values=self.master.humanized_cols,
#             textvariable=self.colvar
#         )
#         self.colselect.current(1)
#         self.colselect.grid(column=3, row=0, sticky="NESW")
    
#     def search_callback(self):
#         self.master.search_table(self.queryvar.get(), self.master.cols[self.colselect.current()])

class TableWidget(tktb.TableCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dirtyrows = []
        self.deleted_ids = []

    def deleteRow(self, e=None):
        """Deletes a row, and adds its ID to deleted_ids."""

        if len(self.multiplerowlist)>1:
            n = tk.messagebox.askyesno("Delete",
                                      "Delete Selected Records?",
                                      parent=self.parentframe)
            if n:
                rows = self.multiplerowlist
                for row in rows:
                    id = self.model.getRecordAtRow(row).get("Id", "")
                    if id != "":
                        self.deleted_ids.append(int(id))
                    if row in self.dirtyrows:
                        self.dirtyrows.remove(row)
                        for i in range(len(self.dirtyrows)):
                            if self.dirtyrows[i] > row:
                                self.dirtyrows[i] -= 1
                self.model.deleteRows(rows)
                self.clearSelected()
                self.setSelectedRow(0)
                self.redrawTable()
        else:
            n = tk.messagebox.askyesno("Delete",
                                      "Delete This Record?",
                                      parent=self.parentframe)
            if n:
                row = self.getSelectedRow()
                id = self.model.getRecordAtRow(row).get("Id", "")
                if id != "":
                    self.deleted_ids.append(int(id))
                if row in self.dirtyrows:
                    self.dirtyrows.remove(row)
                    for i in range(len(self.dirtyrows)):
                        if self.dirtyrows[i] > row:
                            self.dirtyrows[i] -= 1
                self.model.deleteRow(row)
                self.setSelectedRow(max(row - 1, 0))
                self.clearSelected()
                self.redrawTable()
        # print(self.dirtyrows)
        print(self.deleted_ids)

    def drawCellEntry(self, row, col, text=None):
        """
        When the user single/double clicks on a text/number cell, bring up entry window.
        Overridden to add ID read-only check and append edited rows to dirtyrows.
        """

        if getattr(self, "cellentry", None):
            self.cellentry.destroy()
        if self.read_only == True:
            return
        # ID column is read-only
        if self.model.getColumnLabel(col) == "Id":
            return
        #absrow = self.get_AbsoluteRow(row)
        h=self.rowheight
        model=self.getModel()
        cellvalue = self.model.getCellRecord(row, col)
        if tktb.Formula.isFormula(cellvalue):
            return
        else:
            text = self.model.getValueAt(row, col)
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        w=x2-x1
        #Draw an entry window
        txtvar = tk.StringVar()
        txtvar.set(text)
        initial = txtvar.get()
        def callback(e):
            value = txtvar.get()
            if value == '=':
                #do a dialog that gets the formula into a text area
                #then they can click on the cells they want
                #when done the user presses ok and its entered into the cell
                self.cellentry.destroy()
                #its all done here..
                self.formula_Dialog(row, col)
                return

            coltype = self.model.getColumnType(col)
            if coltype == 'number':
                sta = self.checkDataEntry(e)
                if sta == 1:
                    model.setValueAt(value,row,col)
            elif coltype == 'text':
                model.setValueAt(value,row,col)

            color = self.model.getColorAt(row,col,'fg')
            self.drawText(row, col, value, color, align=self.align)
            if e.keysym=='Return':
                self.delete('entry')
                #self.drawRect(row, col)
                #self.gotonextCell(e)

        self.cellentry=tk.Entry(self.parentframe,width=20,
                        textvariable=txtvar,
                        #bg=self.entrybackgr,
                        #relief=FLAT,
                        takefocus=1,
                        font=self.thefont)
        self.cellentry.icursor(tk.END)
        self.cellentry.bind('<Return>', callback)
        self.cellentry.bind('<KeyRelease>', callback)
        def edit_end_cb(e=None):
            if initial == txtvar.get():
                return
            if row not in self.dirtyrows:
                self.dirtyrows.append(row)
                # print(self.dirtyrows)
            self.cellentry.unbind("<Return>")
            self.cellentry.unbind("<KeyRelease>")
            self.cellentry.unbind("<FocusOut>")
        self.cellentry.bind("<FocusOut>", edit_end_cb)
        self.cellentry.bind("<Destroy>", edit_end_cb)
        self.cellentry.focus_set()
        self.entrywin=self.create_window(x1+self.inset,y1+self.inset,
                                width=w-self.inset*2,height=h-self.inset*2,
                                window=self.cellentry,anchor='nw',
                                tag='entry')

class TableView(ttk.Frame):
    """
    Base class for the data views for each table in the database.
    DO NOT INSTANTIATE DIRECTLY!!!
    """
    db_class = None

    def __init__(self, host: UIHost, master: Optional[tk.Tk]=None):
        super().__init__(master)
        self.master = master
        self.host = host
        self.master.title(config.config.windowtitle.format(self.db_class.__name__ + "s"))
        self.pack(fill=tk.BOTH, expand=True)
        self.cols: list[str] = self.db_class.__table__.c.keys()
        self.humanized_cols = [s.replace("_", " ").title() for s in self.cols]
        self.create_widgets()

    def create_widgets(self):
        # self.search = SearchWidget(self)
        # self.search.pack(fill=tk.X, padx=10, pady=(15, 5))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.table_data = tktb.TableModel()
        self.init_data()
        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(column=0, row=0, columnspan=4, sticky="NESW", padx=5, pady=5)
        self.table = TableWidget(
            self.table_frame, self.table_data,
            rowheaderwidth=0, cellwidth=100, thefont=("sans-serif", 10)
        )
        self.table.show()
        self.table.resizeColumn(0, 30)
        self.commit_btn = ttk.Button(self, text="Commit Changes", command=self.commit_changes)
        self.commit_btn.grid(column=0, row=1, sticky="NESW", padx=4, pady=2)
        self.refresh_btn = ttk.Button(self, text="Refresh Table", command=self.refresh)
        self.refresh_btn.grid(column=1, row=1, sticky="NESW", padx=4, pady=2)
        self.addrow_btn = ttk.Button(self, text="Add Row", command=self.table.addRow)
        self.addrow_btn.grid(column=2, row=1, sticky="NESW", padx=4, pady=2)
        self.delrow_btn = ttk.Button(
            self, text="Delete Row(s)", command=self.table.deleteRow, style="Danger.TButton"
        )
        self.delrow_btn.grid(column=3, row=1, sticky="NESW", padx=4, pady=2)
        self.welcome_btn = ttk.Button(
            self, text="Back to Welcome", command=self.host.switch_frame_callback(Welcome)
        )
        self.welcome_btn.grid(column=0, row=2, columnspan=2, sticky="NESW", padx=4, pady=2)
        self.exit_btn = ttk.Button(
            self, text="Exit Application", command=self.master.destroy, style="Danger.TButton"
        )
        self.exit_btn.grid(column=2, row=2, columnspan=2, sticky="NESW", padx=4, pady=2)

    def init_data(self):
        self.table_data.data = {}
        data = {
            i: {
                c.key.replace("_", " ").title(): str(getattr(o, c.key))
                for c in inspect(o).mapper.column_attrs
            }
            for i, o in enumerate(db.session.query(self.db_class).all())
        }
        data[len(data)] = {c: "" for c in self.humanized_cols} # Empty Row
        self.table_data.importDict(data)

    def commit_changes(self):
        n = tk.messagebox.askyesno(
            "Commit", "Commit to DB? This will enact all changes, including deletions.",
            parent=self
        )
        if n:
            for id in self.table.deleted_ids:
                obj = db.session.query(self.db_class).get(id)
                db.session.delete(obj)
            for row in self.table.dirtyrows:
                rec = self.table_data.getRecordAtRow(row)
                if rec.get("Id", "") == "":
                    db_row_dict = {}
                    for k in self.humanized_cols:
                        if k == "Id":
                            continue
                        if rec.get(k, "") == "":
                            tk.messagebox.showerror(
                                "Commit Error",
                                "Error occured when committing: Empty fields are not allowed."
                            )
                            db.session.rollback()
                            return
                        else:
                            db_row_dict[k.lower().replace(" ", "_")] = rec[k]
                    db_row = self.db_class(**db_row_dict)
                    db.session.add(db_row)
                else:
                    update_dict = {}
                    for k in self.humanized_cols:
                        if k == "Id":
                            continue
                        if rec.get(k, "") == "":
                            tk.messagebox.showerror(
                                "Commit Error",
                                "Error occured when committing: Empty fields are not allowed."
                            )
                            db.session.rollback()
                            return
                        else:
                            update_dict[k.lower().replace(" ", "_")] = rec[k]
                    db.session.query(self.db_class).filter_by(id=int(rec["Id"])).update(update_dict)
            db.session.commit()
            self.init_data()
            self.table.redraw()
            self.table.dirtyrows = []
            self.table.deleted_ids = []


    def refresh(self):
        n = tk.messagebox.askyesno(
            "Refresh", "Refresh from DB? This will revert all uncommitted changes.",
            parent=self
        )
        if n:
            self.init_data()
            self.table.redraw()
            self.table.dirtyrows = []
            self.table.deleted_ids = []

class CustomersView(TableView):
    db_class = db.Customer

class ProductsView(TableView):
    db_class = db.Product

class SalesView(TableView):
    db_class = db.Sale
