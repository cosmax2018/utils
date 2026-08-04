from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .models import Asset


class ReportService:
    def create_inventory(self, assets: list[Asset], filename: str | Path) -> None:
        pdf = canvas.Canvas(str(filename), pagesize=A4)
        width, height = A4

        def header() -> float:
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(18 * mm, height - 20 * mm, "Inventario Asset")
            pdf.setFont("Helvetica", 8)
            pdf.drawRightString(
                width - 18 * mm,
                height - 20 * mm,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
            )
            y = height - 32 * mm
            pdf.setFont("Helvetica-Bold", 8)
            for x, title in zip(
                (18, 50, 88, 124, 160),
                ("Marca", "Modello", "Seriale", "Utente", "Reparto"),
            ):
                pdf.drawString(x * mm, y, title)
            pdf.line(18 * mm, y - 2 * mm, width - 18 * mm, y - 2 * mm)
            pdf.setFont("Helvetica", 8)
            return y - 7 * mm

        y = header()
        for asset in assets:
            if y < 18 * mm:
                pdf.showPage()
                y = header()
            values = (asset.brand, asset.model, asset.serial, asset.user, asset.department)
            limits = (18, 22, 20, 20, 16)
            for x, value, limit in zip((18, 50, 88, 124, 160), values, limits):
                pdf.drawString(x * mm, y, str(value)[:limit])
            y -= 6 * mm
        pdf.save()
