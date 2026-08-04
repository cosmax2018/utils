from __future__ import annotations

import logging
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox, ttk

from PIL import Image, ImageTk

from .label_service import LabelService
from .models import Asset, Label
from .paths import log_path
from .platform_windows import copy_image, print_image
from .qr_service import QRService, build_email_url
from .report_service import ReportService
from .settings import AppSettings, SettingsStore
from .storage import Storage


def _configure_logging() -> None:
    options = {
        "level": logging.INFO,
        "format": "%(asctime)s %(levelname)s %(message)s",
    }
    try:
        logging.basicConfig(filename=log_path(), **options)
    except OSError:
        logging.basicConfig(**options)


_configure_logging()


class QRGeneratorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("QR Generator")
        self.geometry("950x720")
        self.minsize(820, 620)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.storage = Storage()
        self.qr_service = QRService()
        self.label_service = LabelService()
        self.report_service = ReportService()
        self.settings_store = SettingsStore()
        self.settings = self.settings_store.load()
        self.current_image: Image.Image | None = None
        self.current_label_id: int | None = None
        self.preview_photo: ImageTk.PhotoImage | None = None
        self.font_size = tk.IntVar(value=18)
        self.qr_mode = tk.StringVar(value="Email precompilata")
        self.email_recipient = tk.StringVar(value=self.settings.email_recipient)

        self._build_menu()
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        self._build_qr_tab()
        self._build_inventory_tab()
        self._build_history_tab()
        self._build_report_tab()

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Nuova etichetta", command=self.new_label)
        file_menu.add_command(label="Apri etichetta...", command=self.open_label)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.close_app)
        menu.add_cascade(label="File", menu=file_menu)

        options = tk.Menu(menu, tearoff=False)
        options.add_command(label="Colore QR...", command=self.choose_foreground)
        options.add_command(label="Sfondo QR...", command=self.choose_background)
        options.add_command(label="Logo...", command=self.choose_logo)
        options.add_command(label="Rimuovi logo", command=lambda: self.qr_service.set_logo(None))
        options.add_separator()
        options.add_command(
            label="Configura destinatario email...",
            command=self.configure_email,
        )
        menu.add_cascade(label="Opzioni", menu=options)
        self.config(menu=menu)

    def _build_qr_tab(self) -> None:
        self.qr_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.qr_tab, text="QR Code")
        self.qr_tab.columnconfigure(1, weight=1)
        self.qr_tab.rowconfigure(0, weight=1)

        form = ttk.LabelFrame(self.qr_tab, text="Contenuto", padding=10)
        form.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        ttk.Label(form, text="Testo da codificare").grid(row=0, column=0, sticky="w")
        self.text_data = tk.Text(form, width=38, height=12, wrap="word")
        self.text_data.grid(row=1, column=0, sticky="nsew", pady=(4, 10))
        ttk.Label(form, text="Numero seriale (facoltativo)").grid(row=2, column=0, sticky="w")
        self.serial_entry = ttk.Entry(form, width=38)
        self.serial_entry.grid(row=3, column=0, sticky="ew", pady=(4, 10))
        ttk.Label(form, text="Azione dopo la scansione").grid(row=4, column=0, sticky="w")
        ttk.Combobox(
            form,
            textvariable=self.qr_mode,
            values=("Email precompilata", "Testo normale"),
            state="readonly",
            width=35,
        ).grid(row=5, column=0, sticky="ew", pady=(4, 10))
        ttk.Label(form, text="Email destinatario").grid(row=6, column=0, sticky="w")
        self.email_entry = ttk.Entry(form, textvariable=self.email_recipient, width=38)
        self.email_entry.grid(row=7, column=0, sticky="ew", pady=(4, 10))
        self.email_entry.bind("<FocusOut>", lambda _event: self.save_email_recipient())
        self.email_entry.bind("<Return>", lambda _event: self.save_email_recipient())
        size_row = ttk.Frame(form)
        size_row.grid(row=8, column=0, sticky="ew")
        ttk.Label(size_row, text="Testo etichetta").pack(side="left")
        ttk.Spinbox(size_row, from_=8, to=40, width=5, textvariable=self.font_size).pack(side="right")

        preview = ttk.LabelFrame(self.qr_tab, text="Anteprima", padding=10)
        preview.grid(row=0, column=1, sticky="nsew")
        preview.columnconfigure(0, weight=1)
        preview.rowconfigure(0, weight=1)
        self.preview = ttk.Label(preview, text="Crea un QR per visualizzarlo", anchor="center")
        self.preview.grid(row=0, column=0, sticky="nsew")
        self.preview.bind("<Configure>", self._resize_preview)

        actions = ttk.Frame(self.qr_tab)
        actions.grid(row=1, column=0, columnspan=2, pady=(12, 0))
        for label, command in (
            ("Crea QR", self.create_qr),
            ("Nuovo", self.new_label),
            ("Apri", self.open_label),
            ("Salva PNG", self.save_png),
            ("Salva SVG", self.save_svg),
            ("Copia", self.copy_current),
            ("Stampa", self.print_current),
        ):
            ttk.Button(actions, text=label, command=command).pack(side="left", padx=3)

    def qr_text(self) -> str:
        main = self.text_data.get("1.0", "end").strip()
        serial = self.serial_entry.get().strip()
        if self.qr_mode.get() == "Email precompilata":
            recipient = self.email_recipient.get().strip()
            url = build_email_url(recipient, main, serial)
            self.save_email_recipient()
            return url
        if serial:
            return f"{main}\n\nSERIAL NUMBER: {serial}".strip()
        return main

    def label_text(self) -> str:
        lines = self.text_data.get("1.0", "end").strip().splitlines()[:4]
        serial = self.serial_entry.get().strip()
        if serial:
            lines.extend(("", f"SN: {serial}"))
        return "\n".join(lines)

    def create_qr(self, history_title: str = "QR manuale") -> None:
        try:
            text = self.qr_text()
            if len(text) > 4000:
                raise ValueError("Il contenuto supera 4000 caratteri")
            self.current_image = self.qr_service.create(text)
            self.storage.add_history(history_title, text)
            self._show_preview()
            self.refresh_history()
        except Exception as exc:
            self._error("Creazione QR", exc)

    def new_label(self) -> None:
        self.current_label_id = None
        self.current_image = None
        self.text_data.delete("1.0", "end")
        self.serial_entry.delete(0, "end")
        self.preview.configure(image="", text="Crea un QR per visualizzarlo")
        self.preview_photo = None
        self.tabs.select(self.qr_tab)

    def open_label(self) -> None:
        dialog = LabelDialog(self, self.storage)
        self.wait_window(dialog)
        if dialog.result is None:
            return
        label = dialog.result
        self.current_label_id = label.id
        self.text_data.delete("1.0", "end")
        self.text_data.insert("1.0", label.description)
        self.serial_entry.delete(0, "end")
        self.serial_entry.insert(0, label.serial)
        self.create_qr("Etichetta caricata")
        self.tabs.select(self.qr_tab)

    def _ensure_image(self) -> Image.Image:
        if self.current_image is None:
            raise ValueError("Creare prima il QR")
        return self.current_image

    def _full_label(self) -> Image.Image:
        return self.label_service.create(
            self._ensure_image(), self.label_text(), self.font_size.get()
        )

    def save_png(self) -> None:
        try:
            image = self._full_label()
            filename = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("Immagine PNG", "*.png")]
            )
            if not filename:
                return
            image.save(filename)
            label = Label(
                self.current_label_id,
                self.text_data.get("1.0", "end").strip(),
                self.serial_entry.get().strip(),
                filename,
            )
            self.current_label_id = self.storage.save_label(label)
            messagebox.showinfo("Salvataggio", "Etichetta salvata correttamente")
        except Exception as exc:
            self._error("Salvataggio", exc)

    def save_svg(self) -> None:
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".svg", filetypes=[("Immagine SVG", "*.svg")]
            )
            if filename:
                self.qr_service.save_svg(self.qr_text(), filename)
        except Exception as exc:
            self._error("Salvataggio SVG", exc)

    def copy_current(self) -> None:
        try:
            copy_image(self._full_label())
            messagebox.showinfo("Clipboard", "Etichetta copiata negli appunti")
        except Exception as exc:
            self._error("Clipboard", exc)

    def print_current(self) -> None:
        try:
            print_image(self._full_label())
        except Exception as exc:
            self._error("Stampa", exc)

    def choose_foreground(self) -> None:
        color = colorchooser.askcolor(color=self.qr_service.foreground)[1]
        if color:
            self.qr_service.foreground = color

    def choose_background(self) -> None:
        color = colorchooser.askcolor(color=self.qr_service.background)[1]
        if color:
            self.qr_service.background = color

    def choose_logo(self) -> None:
        filename = filedialog.askopenfilename(
            filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filename:
            try:
                self.qr_service.set_logo(filename)
            except Exception as exc:
                self._error("Logo", exc)

    def configure_email(self) -> None:
        dialog = EmailDialog(self, self.email_recipient.get())
        self.wait_window(dialog)
        if dialog.result is None:
            return
        self.email_recipient.set(dialog.result)
        self.save_email_recipient()

    def save_email_recipient(self) -> None:
        recipient = self.email_recipient.get().strip()
        if "@" not in recipient or any(char in recipient for char in "\r\n,;"):
            return
        if recipient != self.settings.email_recipient:
            self.settings = AppSettings(email_recipient=recipient)
            self.settings_store.save(self.settings)

    def close_app(self) -> None:
        self.save_email_recipient()
        self.destroy()

    def _show_preview(self) -> None:
        if self.current_image is None:
            return
        size = max(120, min(self.preview.winfo_width(), self.preview.winfo_height()) - 20)
        image = self.current_image.resize((size, size), Image.Resampling.NEAREST)
        self.preview_photo = ImageTk.PhotoImage(image)
        self.preview.configure(image=self.preview_photo, text="")

    def _resize_preview(self, _event: tk.Event) -> None:
        if self.current_image:
            self.after_idle(self._show_preview)

    def _build_inventory_tab(self) -> None:
        self.inventory_tab = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(self.inventory_tab, text="Inventario")
        toolbar = ttk.Frame(self.inventory_tab)
        toolbar.pack(fill="x", pady=(0, 8))
        self.asset_search = ttk.Entry(toolbar)
        self.asset_search.pack(side="left", fill="x", expand=True)
        self.asset_search.bind("<KeyRelease>", lambda _event: self.refresh_assets())
        for label, command in (
            ("Nuovo", self.add_asset), ("Modifica", self.edit_asset),
            ("Elimina", self.delete_asset), ("Crea QR", self.asset_to_qr),
        ):
            ttk.Button(toolbar, text=label, command=command).pack(side="left", padx=(5, 0))
        columns = ("id", "brand", "model", "serial", "user", "department")
        self.asset_table = ttk.Treeview(self.inventory_tab, columns=columns, show="headings")
        for column, title, width in zip(
            columns, ("ID", "Marca", "Modello", "Seriale", "Utente", "Reparto"),
            (50, 130, 150, 160, 150, 130),
        ):
            self.asset_table.heading(column, text=title)
            self.asset_table.column(column, width=width)
        self.asset_table.pack(fill="both", expand=True)
        self.asset_table.bind("<Double-1>", lambda _event: self.edit_asset())
        self.refresh_assets()

    def refresh_assets(self) -> None:
        self.asset_table.delete(*self.asset_table.get_children())
        for asset in self.storage.assets(self.asset_search.get()):
            self.asset_table.insert("", "end", values=(
                asset.id, asset.brand, asset.model, asset.serial, asset.user, asset.department
            ))

    def selected_asset(self) -> Asset | None:
        selection = self.asset_table.selection()
        if not selection:
            return None
        asset_id = int(self.asset_table.item(selection[0], "values")[0])
        return self.storage.asset(asset_id)

    def add_asset(self) -> None:
        self._asset_dialog(None)

    def edit_asset(self) -> None:
        asset = self.selected_asset()
        if asset:
            self._asset_dialog(asset)

    def _asset_dialog(self, asset: Asset | None) -> None:
        dialog = AssetDialog(self, asset)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.storage.save_asset(dialog.result)
                self.refresh_assets()
            except sqlite3.IntegrityError:
                messagebox.showerror("Inventario", "Il numero seriale e gia presente")
            except Exception as exc:
                self._error("Inventario", exc)

    def delete_asset(self) -> None:
        asset = self.selected_asset()
        if asset and messagebox.askyesno("Elimina", f"Eliminare {asset.serial}?"):
            self.storage.delete_asset(asset.id)
            self.refresh_assets()

    def asset_to_qr(self) -> None:
        asset = self.selected_asset()
        if not asset:
            return
        self.new_label()
        self.text_data.insert("1.0", asset.qr_text())
        self.create_qr("QR inventario")

    def _build_history_tab(self) -> None:
        self.history_tab = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(self.history_tab, text="Cronologia")
        columns = ("date", "title", "content")
        self.history_table = ttk.Treeview(self.history_tab, columns=columns, show="headings")
        for column, title, width in zip(columns, ("Data", "Tipo", "Contenuto"), (150, 160, 550)):
            self.history_table.heading(column, text=title)
            self.history_table.column(column, width=width)
        self.history_table.pack(fill="both", expand=True)
        self.refresh_history()

    def refresh_history(self) -> None:
        self.history_table.delete(*self.history_table.get_children())
        for row in self.storage.history():
            content = row["content"].replace("\n", " ")[:100]
            self.history_table.insert("", "end", values=(row["created_at"], row["title"], content))

    def _build_report_tab(self) -> None:
        self.report_tab = ttk.Frame(self.tabs, padding=30)
        self.tabs.add(self.report_tab, text="Report")
        ttk.Label(
            self.report_tab,
            text="Esporta l'inventario corrente in un report PDF multipagina.",
        ).pack(pady=(40, 15))
        ttk.Button(
            self.report_tab, text="Genera report PDF", command=self.generate_report
        ).pack()

    def generate_report(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("Documento PDF", "*.pdf")]
        )
        if not filename:
            return
        try:
            self.report_service.create_inventory(self.storage.assets(), filename)
            messagebox.showinfo("Report", "Report creato correttamente")
        except Exception as exc:
            self._error("Report", exc)

    @staticmethod
    def _error(title: str, exc: Exception) -> None:
        logging.exception("%s: %s", title, exc)
        messagebox.showerror(title, str(exc))


class LabelDialog(tk.Toplevel):
    def __init__(self, parent: tk.Widget, storage: Storage) -> None:
        super().__init__(parent)
        self.storage = storage
        self.result: Label | None = None
        self.title("Apri etichetta")
        self.geometry("760x430")
        self.transient(parent)
        self.grab_set()
        self.search = ttk.Entry(self)
        self.search.pack(fill="x", padx=10, pady=10)
        self.search.bind("<KeyRelease>", lambda _event: self.refresh())
        columns = ("id", "serial", "description", "updated")
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        for column, title, width in zip(
            columns, ("ID", "Seriale", "Descrizione", "Modificato"), (50, 130, 400, 150)
        ):
            self.table.heading(column, text=title)
            self.table.column(column, width=width)
        self.table.pack(fill="both", expand=True, padx=10)
        self.table.bind("<Double-1>", lambda _event: self.open())
        ttk.Button(self, text="Apri", command=self.open).pack(pady=10)
        self.refresh()

    def refresh(self) -> None:
        self.table.delete(*self.table.get_children())
        for label in self.storage.labels(self.search.get()):
            self.table.insert("", "end", values=(
                label.id, label.serial, label.description[:80], label.updated_at
            ))

    def open(self) -> None:
        selection = self.table.selection()
        if selection:
            label_id = int(self.table.item(selection[0], "values")[0])
            self.result = self.storage.label(label_id)
            self.destroy()


class AssetDialog(tk.Toplevel):
    FIELDS = (
        ("brand", "Marca *"), ("model", "Modello *"), ("serial", "Seriale *"),
        ("user", "Utente"), ("department", "Reparto"), ("description", "Descrizione"),
    )

    def __init__(self, parent: tk.Widget, asset: Asset | None) -> None:
        super().__init__(parent)
        self.asset = asset
        self.result: Asset | None = None
        self.title("Asset inventario")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.entries: dict[str, ttk.Entry] = {}
        for row, (name, label) in enumerate(self.FIELDS):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=6)
            entry = ttk.Entry(self, width=42)
            entry.grid(row=row, column=1, padx=10, pady=6)
            if asset:
                entry.insert(0, getattr(asset, name))
            self.entries[name] = entry
        buttons = ttk.Frame(self)
        buttons.grid(row=len(self.FIELDS), column=0, columnspan=2, pady=12)
        ttk.Button(buttons, text="Salva", command=self.save).pack(side="left", padx=4)
        ttk.Button(buttons, text="Annulla", command=self.destroy).pack(side="left", padx=4)

    def save(self) -> None:
        values = {name: entry.get().strip() for name, entry in self.entries.items()}
        if not values["brand"] or not values["model"] or not values["serial"]:
            messagebox.showwarning("Dati mancanti", "Marca, modello e seriale sono obbligatori")
            return
        self.result = Asset(id=self.asset.id if self.asset else None, **values)
        self.destroy()


class EmailDialog(tk.Toplevel):
    def __init__(self, parent: tk.Widget, recipient: str) -> None:
        super().__init__(parent)
        self.result: str | None = None
        self.title("Destinatario email")
        self.geometry("560x180")
        self.transient(parent)
        self.grab_set()
        ttk.Label(
            self,
            text="Indirizzo che ricevera le email generate dalla scansione:",
        ).pack(anchor="w", padx=15, pady=(15, 8))
        self.email_entry = ttk.Entry(self, width=65)
        self.email_entry.pack(fill="x", padx=15, pady=5)
        self.email_entry.insert(0, recipient)
        buttons = ttk.Frame(self)
        buttons.pack(pady=15)
        ttk.Button(buttons, text="Salva", command=self.save).pack(side="left", padx=4)
        ttk.Button(buttons, text="Annulla", command=self.destroy).pack(side="left", padx=4)

    def save(self) -> None:
        recipient = self.email_entry.get().strip()
        if "@" not in recipient or any(char in recipient for char in "\r\n,;"):
            messagebox.showerror("Configurazione", "Indirizzo email non valido")
            return
        self.result = recipient
        self.destroy()
