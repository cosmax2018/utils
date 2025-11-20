import zipfile
import shutil
import os
from lxml import etree
import sys

def rebuild_single_sheet(input_file, output_file, sheet_to_keep):
    """
    Ricostruisce un XLSX preservando sharedStrings, tabelle, rels, ecc.,
    copiando solo il foglio specificato.
    
    :param input_file: path del file XLSX originale
    :param output_file: path del file XLSX ricostruito
    :param sheet_to_keep: nome del foglio da mantenere
    """
    temp_dir = input_file + "_tmp"
    
    # 1. Estrai tutto il contenuto ZIP in cartella temporanea
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # 2. Trova i file dei fogli e rimuovi quelli che non vogliamo
    sheets_dir = os.path.join(temp_dir, "xl", "worksheets")
    sheet_files = [f for f in os.listdir(sheets_dir) if f.endswith(".xml") and not f.startswith("_rels")]

    for f in sheet_files:
        # Controlla il nome del foglio in workbook.xml
        workbook_path = os.path.join(temp_dir, "xl", "workbook.xml")
        tree = etree.parse(workbook_path)
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        keep = False
        for sheet in tree.findall('.//ns:sheet', namespaces=ns):
            if f[:-4].lower() in sheet.get('name').lower() and sheet_to_keep.lower() in sheet.get('name').lower():
                keep = True
                break
        if not keep:
            os.remove(os.path.join(sheets_dir, f))
            # Rimuovi anche il rel corrispondente se esiste
            rel_file = os.path.join(sheets_dir, "_rels", f + ".rels")
            if os.path.exists(rel_file):
                os.remove(rel_file)

    # 3. Ricrea il file XLSX
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    # 4. Pulizia cartella temporanea
    shutil.rmtree(temp_dir)
    print(f"File ricostruito mantenendo solo il foglio '{sheet_to_keep}': {output_file}")

# --------------------------
# Uso da linea di comando
# --------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python rebuild_single_sheet.py <file_input.xlsx> <nome_foglio>")
        sys.exit(1)

    input_path = sys.argv[1]
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_single_sheet.xlsx"    
    # output_file = sys.argv[2]
    sheet_to_keep = sys.argv[2]

    rebuild_single_sheet(input_path, output_path, sheet_to_keep)
