#
# QRGenerator Professional
#
# Versione 1.0
#
# Copyright 2026
#

import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

import qrcode

import io

import os



#############################################################

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")

#############################################################


class QRGeneratorApp(ctk.CTk):

    #########################################################

    def __init__(self):

        super().__init__()

        self.title("QRGenerator Professional")

        self.geometry("1100x760")

        self.minsize(1100,760)

        self.current_image = None

        self.current_pil = None

        self.filename = None

        self.create_widgets()

    #########################################################

    def create_widgets(self):

        ###############################################
        # frame principale
        ###############################################

        self.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        ###################################################

        self.left = ctk.CTkFrame(self)

        self.left.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ###################################################

        self.right = ctk.CTkFrame(self)

        self.right.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ###################################################
        # titolo
        ###################################################

        title = ctk.CTkLabel(
            self.left,
            text="Dati da codificare",
            font=("Segoe UI",20,"bold")
        )

        title.pack(pady=(20,10))

        ###################################################

        self.text = ctk.CTkTextbox(
            self.left,
            width=450,
            height=420,
            font=("Consolas",15)
        )

        self.text.pack(
            padx=20,
            fill="both",
            expand=True
        )

        ###################################################

        self.text.bind("<KeyRelease>", self.update_qr)

        ###################################################

        lbl = ctk.CTkLabel(
            self.left,
            text="Titolo etichetta"
        )

        lbl.pack(pady=(20,5))

        ###################################################

        self.title_entry = ctk.CTkEntry(
            self.left,
            width=420
        )

        self.title_entry.pack()

        ###################################################

        self.counter = ctk.CTkLabel(
            self.left,
            text="0 caratteri"
        )

        self.counter.pack(pady=15)

        ###################################################
        # QR
        ###################################################

        lab = ctk.CTkLabel(
            self.right,
            text="Anteprima QR",
            font=("Segoe UI",20,"bold")
        )

        lab.pack(pady=(20,20))

        ###################################################

        self.preview = ctk.CTkLabel(
            self.right,
            text=""
        )

        self.preview.pack(
            expand=True
        )

        ###################################################
        # Pulsanti
        ###################################################

        self.button_frame = ctk.CTkFrame(
            self.right,
            fg_color="transparent"
        )

        self.button_frame.pack(
            pady=20
        )

        ###################################################

        self.save_button = ctk.CTkButton(

            self.button_frame,

            text="Salva PNG",

            command=self.save_png,

            width=150

        )

        self.save_button.grid(
            row=0,
            column=0,
            padx=10
        )

        ###################################################

        self.copy_button = ctk.CTkButton(

            self.button_frame,

            text="Copia",

            command=self.copy_image,

            width=150

        )

        self.copy_button.grid(
            row=0,
            column=1,
            padx=10
        )

        ###################################################

        self.print_button = ctk.CTkButton(

            self.button_frame,

            text="Stampa",

            command=self.print_image,

            width=150

        )

        self.print_button.grid(
            row=0,
            column=2,
            padx=10
        )

        ###################################################

        self.close_button = ctk.CTkButton(

            self.button_frame,

            text="Chiudi",

            command=self.destroy,

            width=150,

            fg_color="firebrick"

        )

        self.close_button.grid(
            row=0,
            column=3,
            padx=10
        )

        ###################################################

        self.status = ctk.CTkLabel(

            self,

            text="Pronto",

            anchor="w"

        )

        self.status.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0,8)
        )

    #########################################################

    def update_qr(self,event=None):

        testo = self.text.get("1.0","end").strip()

        self.counter.configure(
            text=f"{len(testo)} caratteri"
        )

        if testo=="":
            self.preview.configure(image=None)
            return

        qr = qrcode.QRCode(

            version=None,

            error_correction=qrcode.constants.ERROR_CORRECT_H,

            box_size=10,

            border=4

        )

        qr.add_data(testo)

        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGB")

        self.current_pil = img

        img = img.resize(
            (420,420)
        )

        self.current_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(420,420)
        )

        self.preview.configure(
            image=self.current_image
        )

        self.status.configure(
            text="QR aggiornato"
        )

    #########################################################

    def save_png(self):

        if self.current_pil is None:
            return

        filename = filedialog.asksaveasfilename(

            defaultextension=".png",

            filetypes=[

                ("PNG","*.png")

            ]

        )

        if filename=="":
            return

        self.current_pil.save(filename)

        self.status.configure(
            text="File salvato."
        )

    #########################################################

    def copy_image(self):

        messagebox.showinfo(

            "Funzione",

            "La copia negli appunti verrà implementata nella Parte 2."

        )

    #########################################################

    def print_image(self):

        messagebox.showinfo(

            "Funzione",

            "La stampa professionale verrà implementata nella Parte 2."

        )


#############################################################


if __name__=="__main__":

    app = QRGeneratorApp()

    app.mainloop()