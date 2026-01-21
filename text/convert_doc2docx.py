#
# convert_doc2docx.py : converte tutti i files in una dir da .doc a .docx
#
from pathlib import Path
import re
import win32com.client as win32

WD_FORMAT_DOCX = 16  # .docx

def safe_filename(name):
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def convert_doc_to_docx(input_dir, output_dir=None):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir) if output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    word = win32.Dispatch("Word.Application")
    word.Visible = False

    try:
        for doc_path in input_dir.glob("*.doc"):
            safe_name = safe_filename(doc_path.stem)
            docx_path = output_dir / f"{safe_name}.docx"

            print(f"Converto: {doc_path.name}")
            print(f"  → {docx_path.name}")

            doc = word.Documents.Open(
                str(doc_path.resolve()),
                ReadOnly=True,
                AddToRecentFiles=False
            )

            doc.SaveAs(str(docx_path.resolve()), FileFormat=WD_FORMAT_DOCX)
            doc.Close(False)

    finally:
        word.Quit()

    print("Conversione completata.")


# -------------------------
# USO
# -------------------------
if __name__ == "__main__":
    convert_doc_to_docx(
        input_dir=r"D:\miei-scritti",
        output_dir=r"D:\miei-scritti\docx"
    )
