#
# load_dialog.py
#
# Finestra caricamento etichette QR
#
# Copyright 2026
#

import tkinter as tk

from tkinter import ttk



class LoadDialog(tk.Toplevel):


    ############################################################

    def __init__(

            self,

            parent,

            database

        ):


        super().__init__(parent)


        self.parent = parent

        self.database = database


        self.result = None



        self.title(
            "Carica etichetta QR"
        )


        self.geometry(
            "750x450"
        )


        self.resizable(
            True,
            True
        )


        self.create_gui()


        self.load_data()



        self.transient(parent)

        self.grab_set()



    ############################################################
    #
    # GUI
    #
    ############################################################


    def create_gui(self):


        ##################################################
        # ricerca
        ##################################################


        search_frame = ttk.Frame(
            self
        )

        search_frame.pack(

            fill="x",

            padx=10,

            pady=10

        )


        ttk.Label(

            search_frame,

            text="Cerca:"

        ).pack(

            side="left"

        )


        self.search_text = tk.StringVar()


        self.search_text.trace(

            "w",

            self.search_changed

        )


        self.entry_search = ttk.Entry(

            search_frame,

            textvariable=self.search_text

        )


        self.entry_search.pack(

            side="left",

            fill="x",

            expand=True,

            padx=10

        )



        ##################################################
        # tabella
        ##################################################


        table_frame = ttk.Frame(

            self

        )


        table_frame.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=5

        )



        columns = (

            "id",

            "serial",

            "description",

            "date"

        )


        self.table = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings"

        )



        self.table.heading(

            "id",

            text="ID"

        )


        self.table.heading(

            "serial",

            text="SERIALE"

        )


        self.table.heading(

            "description",

            text="DESCRIZIONE"

        )


        self.table.heading(

            "date",

            text="MODIFICATO"

        )



        self.table.column(

            "id",

            width=50

        )


        self.table.column(

            "serial",

            width=120

        )


        self.table.column(

            "description",

            width=400

        )


        self.table.column(

            "date",

            width=130

        )



        scrollbar = ttk.Scrollbar(

            table_frame,

            orient="vertical",

            command=self.table.yview

        )


        self.table.configure(

            yscrollcommand=scrollbar.set

        )



        self.table.pack(

            side="left",

            fill="both",

            expand=True

        )


        scrollbar.pack(

            side="right",

            fill="y"

        )



        self.table.bind(

            "<Double-1>",

            self.open_selected

        )



        ##################################################
        # pulsanti
        ##################################################


        button_frame = ttk.Frame(

            self

        )


        button_frame.pack(

            pady=10

        )



        ttk.Button(

            button_frame,

            text="Apri",

            command=self.open_selected

        ).pack(

            side="left",

            padx=5

        )



        ttk.Button(

            button_frame,

            text="Annulla",

            command=self.close

        ).pack(

            side="left",

            padx=5

        )



    ############################################################
    #
    # caricamento dati
    #
    ############################################################


    def load_data(self):


        self.table.delete(

            *self.table.get_children()

        )


        rows = self.database.get_labels()



        for row in rows:


            self.table.insert(

                "",

                tk.END,

                values=(

                    row[0],

                    row[1],

                    row[2][:60],

                    row[3]

                )

            )



    ############################################################
    #
    # ricerca
    #
    ############################################################


    def search_changed(

            self,

            *args

        ):


        text = self.search_text.get()


        self.table.delete(

            *self.table.get_children()

        )


        if text:


            rows = self.database.search_labels(

                text

            )

        else:


            rows = self.database.get_labels()



        for row in rows:


            self.table.insert(

                "",

                tk.END,

                values=(

                    row[0],

                    row[1],

                    row[2][:60],

                    row[3]

                )

            )



    ############################################################
    #
    # apertura
    #
    ############################################################


    def open_selected(

            self,

            event=None

        ):


        selected = self.table.selection()


        if not selected:

            return



        values = self.table.item(

            selected[0]

        )[

            "values"

        ]



        label_id = values[0]


        self.result = self.database.get_label(

            label_id

        )


        self.close()



    ############################################################
    #
    # chiusura
    #
    ############################################################


    def close(self):


        self.grab_release()

        self.destroy()



    ############################################################
    #
    # ritorno risultato
    #
    ############################################################


    def show(self):


        self.wait_window()


        return self.result