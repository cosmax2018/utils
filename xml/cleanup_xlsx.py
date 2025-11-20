import zipfile
import xml.etree.ElementTree as ET
import os
import shutil
import sys

def cleanup_xlsx(input_path, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_cleaned{ext}"

    temp_dir = "temp_xlsx_cleanup"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # 1️⃣ Estrai tutto il contenuto
    with zipfile.ZipFile(input_path, 'r') as zin:
        zin.extractall(temp_dir)

    # 2️⃣ Leggi workbook.xml e workbook.xml.rels
    workbook_path = os.path.join(temp_dir, "xl", "workbook.xml")
    tree = ET.parse(workbook_path)
    root = tree.getroot()
    ns = {'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

    sheets_elem = root.find('ns:sheets', ns)
    active_sheet_rids = {}
    for sheet in sheets_elem.findall('ns:sheet', ns):
        rid = sheet.attrib.get(f'{{{NS_R}}}id') or sheet.attrib.get('id')  # fallback
        if rid is not None:
            active_sheet_rids[rid] = sheet.attrib['name']

    # Relazioni workbook.xml.rels
    rels_path = os.path.join(temp_dir, "xl", "_rels", "workbook.xml.rels")
    tree_rels = ET.parse(rels_path)
    root_rels = tree_rels.getroot()
    ns_rel = {'rel':'http://schemas.openxmlformats.org/package/2006/relationships'}

    active_sheet_files = []
    for rel in root_rels.findall('rel:Relationship', ns_rel):
        rid = rel.attrib.get('Id')
        if rid in active_sheet_rids:
            active_sheet_files.append(rel.attrib['Target'].replace('/', os.sep))

    # 3️⃣ Leggi ciascun foglio per identificare tabelle effettive
    active_table_files = set()
    for sheet_file in active_sheet_files:
        sheet_path = os.path.join(temp_dir, "xl", sheet_file)
        sheet_dir = os.path.dirname(sheet_path)
        rels_sheet_path = os.path.join(sheet_dir, "_rels", os.path.basename(sheet_path) + ".rels")
        if os.path.exists(rels_sheet_path):
            tree_s = ET.parse(rels_sheet_path)
            root_s = tree_s.getroot()
            for rel in root_s.findall('rel:Relationship', ns_rel):
                target = rel.attrib.get('Target')
                if target and target.startswith("../tables/"):
                    table_file = target.replace("../", "").replace('/', os.sep)
                    active_table_files.add(table_file)

    # 4️⃣ Copia tutto in una cartella pulita
    cleaned_dir = "temp_xlsx_cleaned"
    if os.path.exists(cleaned_dir):
        shutil.rmtree(cleaned_dir)
    shutil.copytree(temp_dir, cleaned_dir)

    # 5️⃣ Rimuovi fogli orfani e rels orfani
    ws_dir = os.path.join(cleaned_dir, "xl", "worksheets")
    if os.path.exists(ws_dir):
        # Mantieni rels dei fogli attivi
        active_sheet_rels = {os.path.basename(fa) + ".rels" for fa in active_sheet_files}
        rels_subdir = os.path.join(ws_dir, "_rels")
        if os.path.exists(rels_subdir):
            for f in os.listdir(rels_subdir):
                full_path = os.path.join(rels_subdir, f)
                if os.path.isfile(full_path) and f not in active_sheet_rels:
                    os.remove(full_path)

        # Rimuovi fogli orfani
        for f in os.listdir(ws_dir):
            full_path = os.path.join(ws_dir, f)
            if os.path.isfile(full_path) and f not in [os.path.basename(fa) for fa in active_sheet_files]:
                os.remove(full_path)

    # 6️⃣ Rimuovi tabelle orfane
    tables_dir = os.path.join(cleaned_dir, "xl", "tables")
    if os.path.exists(tables_dir):
        for f in os.listdir(tables_dir):
            full_path = os.path.join(tables_dir, f)
            if os.path.isfile(full_path) and f not in [os.path.basename(fa) for fa in active_table_files]:
                os.remove(full_path)

    # 7️⃣ Ricrea il file XLSX finale
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root_dir, _, files in os.walk(cleaned_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, cleaned_dir)
                zout.write(full_path, rel_path)

    # Pulisci cartelle temporanee
    shutil.rmtree(temp_dir)
    shutil.rmtree(cleaned_dir)
    print(f"✅ File XLSX pulito creato: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cleanup_xlsx.py <file.xlsx>")
        sys.exit(1)
    
    file_path = os.path.abspath(sys.argv[1])
    cleanup_xlsx(file_path)
