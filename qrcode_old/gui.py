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
from load_dialog import LoadDialog


class QRGeneratorApp(tk.Tk):

    ############################################################
    # COSTRUTTORE
    ############################################################

    def __init__(self):

        super().__init__()

        self.title(
            "QR Generator Professional"
        )

        self.geometry(
            "510x660"
        )

        self.minsize(
            510,
            660
        )


        ##################################################
        # MODULI
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


        ##################################################
        # VARIABILI STATO
        ##################################################

        self.current_image = None

        self.current_label_id = None

        self.tk_image = None


        ##################################################
        # DIMENSIONE TESTO ETICHETTA
        ##################################################

        self.label_font_size = tk.IntVar(
            value=14
        )

        self.label_font_size.trace_add(
            "write",
            self.update_label_font
        )


        ##################################################
        # CREA INTERFACCIA
        ##################################################

        self.create_gui()



    ############################################################
    #
    # CREAZIONE GUI PRINCIPALE
    #
    ############################################################

    def create_gui(self):


        ##################################################
        # MENU
        ##################################################

        menu = tk.Menu(
            self
        )


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
        # NOTEBOOK
        ##################################################

        self.tabs = ttk.Notebook(
            self
        )


        self.tabs.pack(
            fill="both",
            expand=True
        )



        ##################################################
        # TAB QR
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
        # TAB INVENTARIO
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
        # TAB CRONOLOGIA
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
        # TAB REPORT
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
    #
    # TAB QR CODE
    #
    ############################################################

    def create_qr_tab(self):


        ##################################################
        # FRAME PRINCIPALE
        ##################################################

        main_frame = ttk.Frame(
            self.tab_qr
        )


        main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        main_frame.rowconfigure(
            0,
            weight=0
        )

        main_frame.rowconfigure(
            1,
            weight=1
        )

        main_frame.rowconfigure(
            2,
            weight=0
        )


        main_frame.columnconfigure(
            0,
            weight=1
        )



        ##################################################
        # FRAME DATI
        ##################################################

        input_frame = ttk.LabelFrame(
            main_frame,
            text="Dati QR Code"
        )


        input_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )


        input_frame.columnconfigure(
            1,
            weight=1
        )



        ##################################################
        # TESTO QR
        ##################################################

        ttk.Label(
            input_frame,
            text="Dati da codificare:"
        ).grid(
            row=0,
            column=0,
            sticky="nw",
            padx=5,
            pady=5
        )


        self.text_data = tk.Text(
            input_frame,
            height=5,
            width=40,
            wrap="word"
        )


        self.text_data.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )



        ##################################################
        # SERIAL NUMBER
        ##################################################

        ttk.Label(
            input_frame,
            text="Serial Number:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )


        self.text_serial = tk.Entry(
            input_frame,
            width=40
        )


        self.text_serial.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )



        ##################################################
        # DIMENSIONE TESTO ETICHETTA
        ##################################################

        ttk.Label(
            input_frame,
            text="Dimensione testo:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )


        self.font_spin = ttk.Spinbox(
            input_frame,
            from_=8,
            to=40,
            width=6,
            textvariable=self.label_font_size
        )


        self.font_spin.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )



        ##################################################
        # FRAME PREVIEW
        ##################################################

        preview_frame = ttk.LabelFrame(
            main_frame,
            text="Anteprima QR Code"
        )


        preview_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )


        preview_frame.rowconfigure(
            0,
            weight=1
        )


        preview_frame.columnconfigure(
            0,
            weight=1
        )



        ##################################################
        # CONTENITORE QR
        ##################################################

        self.qr_frame = ttk.Frame(
            preview_frame,
            width=300,
            height=300,
            relief="solid",
            borderwidth=1
        )


        self.qr_frame.grid(
            row=0,
            column=0,
            pady=10
        )


        self.qr_frame.grid_propagate(
            False
        )



        ##################################################
        # IMMAGINE QR
        ##################################################

        self.qr_preview = ttk.Label(
            self.qr_frame,
            text="QR CODE",
            anchor="center"
        )


        self.qr_preview.pack(
            expand=True
        )



        ##################################################
        # TESTO DESCRITTIVO SOTTO QR
        ##################################################

        self.qr_label = ttk.Label(
            preview_frame,
            text="",
            justify="center",
            anchor="center",
            font=(
                "Arial",
                self.label_font_size.get(),
                "bold"
            )
        )


        self.qr_label.grid(
            row=1,
            column=0,
            pady=(5,15)
        )



        ##################################################
        # TOOLBAR
        ##################################################

        toolbar = ttk.Frame(
            main_frame
        )


        toolbar.grid(
            row=2,
            column=0,
            pady=10
        )



        buttons = [

            (
                "▶ Crea QR",
                self.create_qr
            ),

            (
                "📂 Load",
                self.load_label
            ),

            (
                "💾 Salva",
                self.save_label
            ),

            (
                "🖨 Stampa",
                self.print_qr
            ),

            (
                "📋 Copia",
                self.copy_qr
            ),

            (
                "✖ Chiudi",
                self.destroy
            )

        ]



        for text, command in buttons:

            ttk.Button(
                toolbar,
                text=text,
                command=command,
                width=12
            ).pack(
                side="left",
                padx=3
            )



        ##################################################
        # EVENTO RESIZE QR
        ##################################################

        self.qr_preview.bind(
            "<Configure>",
            self.resize_qr_preview
        )

    ############################################################
    #
    # AGGIORNAMENTO DIMENSIONE TESTO ETICHETTA
    #
    ############################################################

    def update_label_font(
        self,
        *args
    ):

        if hasattr(
            self,
            "qr_label"
        ):

            self.qr_label.configure(
                font=(
                    "Arial",
                    self.label_font_size.get(),
                    "bold"
                )
            )



    ############################################################
    #
    # CREAZIONE QR CODE
    #
    ############################################################

    def create_qr(
        self
    ):

        main_text = self.text_data.get(
            "1.0",
            tk.END
        ).strip()


        serial = self.text_serial.get().strip()


        text = main_text


        if serial:

            text += (
                "\n\nSERIAL NUMBER: "
                + serial
            )



        if not main_text and not serial:

            messagebox.showwarning(
                "Attenzione",
                "Inserire un testo da codificare"
            )

            return



        ##################################################
        # VALIDAZIONE
        ##################################################

        if not self.validator.validate_qr_text(
            text
        ):

            messagebox.showerror(
                "Errore",
                "\n".join(
                    self.validator.get_errors()
                )
            )

            return



        ##################################################
        # GENERA QR
        ##################################################

        self.current_image = self.qr.create(
            text
        )



        ##################################################
        # VISUALIZZA QR
        ##################################################

        self.tk_image = ImageTk.PhotoImage(
            self.current_image
        )


        self.qr_preview.configure(
            image=self.tk_image,
            text=""
        )



        ##################################################
        # TESTO DESCRITTIVO
        ##################################################

        preview_text = ""


        lines = main_text.split(
            "\n"
        )


        preview_text = "\n".join(
            lines[:3]
        )


        if serial:

            preview_text += (
                "\n\nSN: "
                + serial
            )



        self.qr_label.configure(
            text=preview_text,
            font=(
                "Arial",
                self.label_font_size.get(),
                "bold"
            )
        )



        ##################################################
        # STORIA
        ##################################################

        self.history.add(
            title="QR manuale",
            content=text
        )



    ############################################################
    #
    # CARICA ETICHETTA
    #
    ############################################################

    def load_label(
        self
    ):


        dlg = LoadDialog(
            self,
            self.database
        )


        result = dlg.show()



        if result is None:

            return



        self.current_label_id = result[0]


        description = result[1]


        serial = result[2]



        self.text_data.delete(
            "1.0",
            tk.END
        )


        self.text_data.insert(
            tk.END,
            description
        )



        self.text_serial.delete(
            0,
            tk.END
        )


        self.text_serial.insert(
            0,
            serial
        )



        self.create_qr()



    ############################################################
    #
    # SALVA ETICHETTA
    #
    ############################################################

    def save_label(
        self
    ):


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
                    "PNG",
                    "*.png"
                )
            ]
        )



        if not filename:

            return



        ##################################################
        # CREA IMMAGINE COMPLETA
        ##################################################

        label_image = self.printer.create_label_image(
            self.current_image,
            self.qr_label.cget(
                "text"
            ),
            self.label_font_size.get()
        )


        label_image.save(
            filename
        )



        ##################################################
        # DATI DATABASE
        ##################################################

        description = self.text_data.get(
            "1.0",
            tk.END
        ).strip()


        serial = self.text_serial.get().strip()



        ##################################################
        # INSERT / UPDATE
        ##################################################

        if self.current_label_id is None:


            self.current_label_id = self.database.add_label(
                description,
                serial,
                filename
            )


        else:


            self.database.update_label(
                self.current_label_id,
                description,
                serial,
                filename
            )



        messagebox.showinfo(
            "Salvataggio",
            "Etichetta salvata correttamente"
        )



    ############################################################
    #
    # COPIA QR
    #
    ############################################################

    def copy_qr(
        self
    ):


        if self.current_image is None:

            messagebox.showwarning(
                "Attenzione",
                "Nessun QR disponibile"
            )

            return



        label = self.printer.create_label_image(
            self.current_image,
            self.qr_label.cget(
                "text"
            ),
            self.label_font_size.get()
        )



        self.clipboard.copy_image(
            label
        )



        messagebox.showinfo(
            "Clipboard",
            "QR copiato negli appunti"
        )



    ############################################################
    #
    # STAMPA QR
    #
    ############################################################

    def print_qr(
        self
    ):


        if self.current_image is None:

            messagebox.showwarning(
                "Attenzione",
                "Nessun QR disponibile"
            )

            return



        self.printer.print_label(
            self.current_image,
            self.qr_label.cget(
                "text"
            ),
            self.label_font_size.get()
        )

            ############################################################
    #
    # CAMBIO TEMA
    #
    ############################################################

    def toggle_theme(
        self
    ):

        self.theme.toggle()

        self.theme.apply_tkinter(
            self
        )



    ############################################################
    #
    # TAB INVENTARIO
    #
    ############################################################

    def create_inventory_tab(
        self
    ):


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



        columns = (

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




    ############################################################
    #
    # AGGIORNA INVENTARIO
    #
    ############################################################

    def refresh_inventory(
        self
    ):


        for item in self.inventory_table.get_children():

            self.inventory_table.delete(
                item
            )



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




    ############################################################
    #
    # RICERCA INVENTARIO
    #
    ############################################################

    def search_inventory(
        self
    ):


        text = self.search_asset.get()



        for item in self.inventory_table.get_children():

            self.inventory_table.delete(
                item
            )



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




    ############################################################
    #
    # CARICA ASSET DA INVENTARIO
    #
    ############################################################

    def load_asset_qr(
        self,
        event
    ):


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
    # TAB CRONOLOGIA
    #
    ############################################################

    def create_history_tab(
        self
    ):


        columns = (

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




    ############################################################
    #
    # AGGIORNA CRONOLOGIA
    #
    ############################################################

    def refresh_history(
        self
    ):


        for item in self.history_table.get_children():

            self.history_table.delete(
                item
            )



        rows = self.history.get_last(
            100
        )



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
    # TAB REPORT
    #
    ############################################################

    def create_report_tab(
        self
    ):


        ttk.Button(
            self.tab_report,
            text="Genera Report PDF Inventario",
            command=self.generate_report
        ).pack(
            pady=50
        )




    ############################################################
    #
    # GENERAZIONE REPORT
    #
    ############################################################

    def generate_report(
        self
    ):


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
            
                ############################################################
    #
    # CAMBIO TEMA
    #
    ############################################################

    def toggle_theme(
        self
    ):

        self.theme.toggle()

        self.theme.apply_tkinter(
            self
        )



    ############################################################
    #
    # TAB INVENTARIO
    #
    ############################################################

    def create_inventory_tab(
        self
    ):


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



        columns = (

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




    ############################################################
    #
    # AGGIORNA INVENTARIO
    #
    ############################################################

    def refresh_inventory(
        self
    ):


        for item in self.inventory_table.get_children():

            self.inventory_table.delete(
                item
            )



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




    ############################################################
    #
    # RICERCA INVENTARIO
    #
    ############################################################

    def search_inventory(
        self
    ):


        text = self.search_asset.get()



        for item in self.inventory_table.get_children():

            self.inventory_table.delete(
                item
            )



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




    ############################################################
    #
    # CARICA ASSET DA INVENTARIO
    #
    ############################################################

    def load_asset_qr(
        self,
        event
    ):


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
    # TAB CRONOLOGIA
    #
    ############################################################

    def create_history_tab(
        self
    ):


        columns = (

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




    ############################################################
    #
    # AGGIORNA CRONOLOGIA
    #
    ############################################################

    def refresh_history(
        self
    ):


        for item in self.history_table.get_children():

            self.history_table.delete(
                item
            )



        rows = self.history.get_last(
            100
        )



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
    # TAB REPORT
    #
    ############################################################

    def create_report_tab(
        self
    ):


        ttk.Button(
            self.tab_report,
            text="Genera Report PDF Inventario",
            command=self.generate_report
        ).pack(
            pady=50
        )




    ############################################################
    #
    # GENERAZIONE REPORT
    #
    ############################################################

    def generate_report(
        self
    ):


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
            
    ############################################################
    #
    # RESIZE ANTEPRIMA QR
    #
    ############################################################

    def resize_qr_preview(
        self,
        event
    ):


        if self.current_image is None:

            return



        width = self.qr_frame.winfo_width()

        height = self.qr_frame.winfo_height()



        size = min(
            width,
            height
        )



        if size <= 20:

            return



        img = self.current_image.resize(
            (
                size,
                size
            )
        )



        self.tk_image = ImageTk.PhotoImage(
            img
        )



        self.qr_preview.configure(
            image=self.tk_image
        )



    ############################################################
    #
    # FINE CLASSE QRGeneratorApp
    #
    ############################################################

    