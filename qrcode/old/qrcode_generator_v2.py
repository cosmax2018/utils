
# qrcode_generator_v2.py : generatore di QR Code

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import tempfile
import os


class QRGenerator:

    def __init__(self, root):

        self.root = root
        self.root.title("Generatore QR Code")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.qr_image = None
        self.qr_filename = None

        #########################################
        # Casella testo
        #########################################

        frame_input = tk.LabelFrame(root, text="Dati da codificare")
        frame_input.pack(fill="x", padx=10, pady=10)

        self.text = tk.Text(frame_input, height=8, width=70)
        self.text.pack(padx=10, pady=10)

        #########################################
        # Area QR
        #########################################

        frame_qr = tk.LabelFrame(root, text="QR Code")
        frame_qr.pack(fill="both", expand=True, padx=10)

        self.lbl_qr = tk.Label(frame_qr)
        self.lbl_qr.pack(expand=True)

        #########################################
        # Pulsanti
        #########################################

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(
            frame_buttons,
            text="Crea QR Code",
            width=18,
            command=self.create_qr
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame_buttons,
            text="Stampa",
            width=12,
            command=self.print_qr
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_buttons,
            text="Chiudi",
            width=12,
            command=root.destroy
        ).grid(row=0, column=2, padx=5)

    ########################################################

    def create_qr(self):

        text = self.text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning(
                "Attenzione",
                "Inserire del testo."
            )
            return

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4
        )

        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGB")

        self.qr_filename = os.path.join(
            tempfile.gettempdir(),
            "ultimo_qrcode.png"
        )

        img.save(self.qr_filename)

        preview = img.resize((250, 250))

        self.qr_image = ImageTk.PhotoImage(preview)

        self.lbl_qr.configure(image=self.qr_image)

    ########################################################

    def print_qr(self):

        if self.qr_filename is None:
            messagebox.showwarning(
                "Attenzione",
                "Creare prima il QR Code."
            )
            return

        os.startfile(self.qr_filename, "print")


############################################################

root = tk.Tk()

QRGenerator(root)

root.mainloop()