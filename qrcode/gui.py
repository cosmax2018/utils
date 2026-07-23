#
# gui.py
#
# Interfaccia grafica QRGenerator Professional
#
# Copyright 2026
#

import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


from PIL import ImageTk


from qrengine import QREngine
from clipboard import ClipboardManager
from printer import QRPrinter
from history import History
from database import InventoryDatabase
from settings import Settings
from label import LabelGenerator
from theme import ThemeManager
from validators import Validator



class QRGeneratorApp(tk.Tk):


    ############################################################

    def __init__(self):

        super().__init__()


        self.title(

            "QR Generator Professional"

        )


        self.geometry("700x850")

        self.minsize(
            650,
            750
        )


        ##################################################
        # moduli
        ##################################################

        self.qr = QREngine()

        self.clipboard = ClipboardManager()

        self.printer = QRPrinter()

        self.history = History()

        self.database = InventoryDatabase()

        self.settings = Settings()

        self.label = LabelGenerator()

        self.theme = ThemeManager()

        self.validator = Validator()



        self.current_image = None

        self.tk_image = None



        self.create_gui()



    ############################################################

    def create_gui(self):


        ##################################################
        # menu
        ##################################################


        menu = tk.Menu(self)


        file_menu = tk.Menu(

            menu,

            tearoff=0

        )


        file_menu.add_command(

            label="Esci",

            command=self.destroy

        )


        menu.add_cascade(

            label="File",

            menu=file_menu

        )



        settings_menu = tk.Menu(

            menu,

            tearoff=0

        )


        settings_menu.add_command(

            label="Tema chiaro/scuro",

            command=self.toggle_theme

        )


        menu.add_cascade(

            label="Impostazioni",

            menu=settings_menu

        )



        self.config(

            menu=menu

        )



        ##################################################
        # notebook
        ##################################################


        self.tabs = ttk.Notebook(

            self

        )


        self.tabs.pack(

            fill="both",

            expand=True

        )



        ##################################################
        # tab QR
        ##################################################


        self.tab_qr = ttk.Frame(

            self.tabs

        )


        self.tabs.add(

            self.tab_qr,

            text="QR Code"

        )



        self.create_qr_tab()



        ##################################################
        # tab inventario
        ##################################################


        self.tab_inventory = ttk.Frame(

            self.tabs

        )


        self.tabs.add(

            self.tab_inventory,

            text="Inventario"

        )
        
        self.create_inventory_tab()


        ##################################################
        # tab cronologia
        ##################################################


        self.tab_history = ttk.Frame(

            self.tabs

        )


        self.tabs.add(

            self.tab_history,

            text="Cronologia"

        )
        
        self.create_history_tab()


        ##################################################
        # tab report
        ##################################################


        self.tab_report = ttk.Frame(

            self.tabs

        )


        self.tabs.add(

            self.tab_report,

            text="Report"

        )

        self.create_report_tab()

    ############################################################

    def create_qr_tab(self):


        main_frame = ttk.Frame(

            self.tab_qr

        )


        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



        ##################################################
        # BOX DATI
        ##################################################


        ttk.Label(

            main_frame,

            text="Dati da codificare"

        ).pack()



        self.text_data = tk.Text(

            main_frame,

            height=8,

            width=55

        )


        self.text_data.pack(

            pady=10

        )



        ##################################################
        # ANTEPRIMA QR
        ##################################################


        ttk.Label(

            main_frame,

            text="Anteprima QR Code"

        ).pack(

            pady=(10,5)

        )



        self.qr_preview = ttk.Label(

            main_frame

        )


        self.qr_preview.pack(

            pady=10

        )

        ##################################################
        # ETICHETTA DESCRITTIVA QR
        ##################################################

        self.qr_label = ttk.Label(

            main_frame,

            text="",

            justify="center",

            font=(

                "Arial",

                12,

                "bold"

            )

        )


        self.qr_label.pack(

            pady=5

        )

        ##################################################
        # TOOLBAR
        ##################################################


        toolbar = ttk.Frame(

            main_frame

        )


        toolbar.pack(

            pady=15

        )



        self.btn_create = ttk.Button(

            toolbar,

            text="▶ Crea QR",

            command=self.create_qr,

            width=12

        )


        self.btn_create.pack(

            side="left",

            padx=3

        )



        self.btn_save = ttk.Button(

            toolbar,

            text="💾 Salva",

            command=self.save_png,

            width=12

        )


        self.btn_save.pack(

            side="left",

            padx=3

        )



        self.btn_print = ttk.Button(

            toolbar,

            text="🖨 Stampa",

            command=self.print_qr,

            width=12

        )


        self.btn_print.pack(

            side="left",

            padx=3

        )



        self.btn_copy = ttk.Button(

            toolbar,

            text="📋 Copia",

            command=self.copy_qr,

            width=12

        )


        self.btn_copy.pack(

            side="left",

            padx=3

        )



        self.btn_close = ttk.Button(

            toolbar,

            text="✖ Chiudi",

            command=self.destroy,

            width=12

        )


        self.btn_close.pack(

            side="left",

            padx=3

        )
    
    ############################################################
    #
    # CREAZIONE QR CODE
    #
    ############################################################


    def create_qr(self):


        text = self.text_data.get(

            "1.0",

            tk.END

        ).strip()



        if not text:


            messagebox.showwarning(

                "Attenzione",

                "Inserire un testo da codificare"

            )


            return



        ##################################################
        # validazione
        ##################################################


        if not self.validator.validate_qr_text(text):


            messagebox.showerror(

                "Errore",

                "\n".join(

                    self.validator.get_errors()

                )

            )


            return



        ##################################################
        # genera QR
        ##################################################


        self.current_image = self.qr.create(

            text

        )


        ##################################################
        # mostra anteprima
        ##################################################


        preview = self.qr.resize(
            280
        )


        self.tk_image = ImageTk.PhotoImage(

            preview

        )


        self.qr_preview.configure(

            image=self.tk_image

        )


        ##################################################
        # testo descrittivo sotto QR
        ##################################################

        lines = text.split("\n")


        preview_text = "\n".join(

            lines[:4]

        )


        self.qr_label.configure(

            text=preview_text

        )

        ##################################################
        # salva cronologia
        ##################################################


        self.history.add(

            title="QR manuale",

            content=text

        )



    ############################################################
    #
    # SALVA PNG
    #
    ############################################################


    def save_png(self):


        if self.current_image is None:


            messagebox.showwarning(

                "Attenzione",

                "Creare prima il QR"

            )


            return



        filename = filedialog.asksaveasfilename(

            defaultextension=".png",

            filetypes=[

                (

                    "Immagine PNG",

                    "*.png"

                )

            ]

        )



        if filename:


            self.qr.save_png(

                filename

            )


            messagebox.showinfo(

                "Salvataggio",

                "QR salvato correttamente"

            )



    ############################################################
    #
    # COPIA CLIPBOARD
    #
    ############################################################


    def copy_qr(self):


        if self.current_image is None:


            messagebox.showwarning(

                "Attenzione",

                "Nessun QR disponibile"

            )


            return



        self.clipboard.copy_image(

            self.current_image

        )



        messagebox.showinfo(

            "Clipboard",

            "QR copiato negli appunti"

        )



    ############################################################
    #
    # STAMPA
    #
    ############################################################


    def print_qr(self):


        if self.current_image is None:


            messagebox.showwarning(

                "Attenzione",

                "Nessun QR disponibile"

            )


            return



        self.printer.print_image(

            self.current_image

        )



    ############################################################
    #
    # CAMBIO TEMA
    #
    ############################################################


    def toggle_theme(self):


        self.theme.toggle()


        self.theme.apply_tkinter(

            self

        )
        
    ############################################################
    #
    # TAB INVENTARIO
    #
    ############################################################


    def create_inventory_tab(self):


        top = ttk.Frame(
            self.tab_inventory
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )


        self.search_asset = tk.Entry(
            top
        )

        self.search_asset.pack(
            side="left",
            fill="x",
            expand=True
        )


        ttk.Button(

            top,

            text="Cerca",

            command=self.search_inventory

        ).pack(
            side="left",
            padx=5
        )



        columns=(

            "id",

            "brand",

            "model",

            "serial",

            "user"

        )



        self.inventory_table = ttk.Treeview(

            self.tab_inventory,

            columns=columns,

            show="headings"

        )



        for c in columns:

            self.inventory_table.heading(

                c,

                text=c.upper()

            )



        self.inventory_table.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )



        self.inventory_table.bind(

            "<Double-1>",

            self.load_asset_qr

        )


        self.refresh_inventory()

    def refresh_inventory(self):


        for item in self.inventory_table.get_children():

            self.inventory_table.delete(item)



        assets = self.database.get_all()



        for a in assets:


            self.inventory_table.insert(

                "",

                tk.END,

                values=(

                    a[0],

                    a[3],

                    a[4],

                    a[5],

                    a[7]

                )

            )

    def search_inventory(self):


        text = self.search_asset.get()



        for item in self.inventory_table.get_children():

            self.inventory_table.delete(item)



        assets = self.database.search(

            text

        )



        for a in assets:


            self.inventory_table.insert(

                "",

                tk.END,

                values=(

                    a[0],

                    a[3],

                    a[4],

                    a[5],

                    a[7]

                )

            )

    def load_asset_qr(self,event):


        selected = self.inventory_table.selection()


        if not selected:

            return



        values = self.inventory_table.item(

            selected[0]

        )["values"]



        asset_id = values[0]



        asset = self.database.get_asset(

            asset_id

        )



        text = f"""

MARCA: {asset[3]}

MODELLO: {asset[4]}

SERIALE: {asset[5]}

UTENTE: {asset[7]}

REPARTO: {asset[8]}

"""



        self.text_data.delete(

            "1.0",

            tk.END

        )


        self.text_data.insert(

            tk.END,

            text

        )


        self.tabs.select(

            self.tab_qr

        )


        self.create_qr()

    ############################################################
    #
    # TAB HISTORY
    #
    ############################################################


    def create_history_tab(self):


        columns=(

            "id",

            "date",

            "title",

            "content"

        )



        self.history_table = ttk.Treeview(

            self.tab_history,

            columns=columns,

            show="headings"

        )



        for c in columns:

            self.history_table.heading(

                c,

                text=c.upper()

            )


        self.history_table.pack(

            fill="both",

            expand=True

        )


        self.refresh_history()

    def refresh_history(self):


        for item in self.history_table.get_children():

            self.history_table.delete(item)



        rows = self.history.get_last(100)



        for r in rows:


            self.history_table.insert(

                "",

                tk.END,

                values=(

                    r[0],

                    r[1],

                    r[2],

                    r[3][:40]

                )

            )

    ############################################################
    #
    # REPORT
    #
    ############################################################


    def create_report_tab(self):


        ttk.Button(

            self.tab_report,

            text="Genera Report PDF Inventario",

            command=self.generate_report

        ).pack(

            pady=50

        )

    def generate_report(self):


        from reports import InventoryReport



        filename = filedialog.asksaveasfilename(

            defaultextension=".pdf",

            filetypes=[

                (
                    "PDF",

                    "*.pdf"

                )

            ]

        )



        if filename:


            report = InventoryReport()



            report.create_pdf(

                self.database.get_all(),

                filename

            )



            messagebox.showinfo(

                "Report",

                "Report creato"

            )

            