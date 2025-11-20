import zipfile
import xml.etree.ElementTree as ET
import os
import shutil
import sys
import re

def sanitize_name(name):
    """Rende il nome compatibile con Excel: ASCII, max 31 caratteri, caratteri validi"""
    name = re.sub(r'[\\/*?:[\]]', '_', name)
    name = ''.join(c if ord(c) < 128 else '_' for c in name)
    return name[:31]

def rebuild_xlsx(input_path, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_rebuild{ext}"

    temp_dir = "temp_xlsx_rebuild"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # 1️⃣ Estrai contenuto
    with zipfile.ZipFile(input_path, 'r') as zin:
        zin.extractall(temp_dir)

    ns = {'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    ns_rel = {'rel':'http://schemas.openxmlformats.org/package/2006/relationships'}

    # 2️⃣ Workbook.xml
    workbook_path = os.path.join(temp_dir, "xl", "workbook.xml")
    tree_wb = ET.parse(workbook_path)
    root_wb = tree_wb.getroot()
    sheets_elem = root_wb.find('ns:sheets', ns)

    # 3️⃣ Workbook.xml.rels
    rels_path = os.path.join(temp_dir, "xl", "_rels", "workbook.xml.rels")
    tree_rels = ET.parse(rels_path)
    root_rels = tree_rels.getroot()

    # Ricostruisci fogli attivi, sheetId sequenziali e r:id coerenti
    active_sheet_files = []
    new_sheetId = 1
    sheet_rid_map = {}
    for sheet in sheets_elem.findall('ns:sheet', ns):
        rid = sheet.attrib.get(f'{{{NS_R}}}id') or sheet.attrib.get('id')
        if rid:
            # Rinomina foglio
            name_safe = sanitize_name(sheet.attrib['name'])
            sheet.attrib['name'] = name_safe
            # Aggiorna sheetId sequenziale
            sheet.attrib['sheetId'] = str(new_sheetId)
            new_sheetId += 1
            sheet_rid_map[rid] = sheet.attrib['sheetId']

            # Trova file foglio corrispondente
            for rel in root_rels.findall('rel:Relationship', ns_rel):
                if rel.attrib.get('Id') == rid:
                    active_sheet_files.append(rel.attrib['Target'].replace('/', os.sep))
                    break

    # 4️⃣ Rimuovi definedNames che puntano a fogli non esistenti
    definedNames = root_wb.find('ns:definedNames', ns)
    if definedNames is not None:
        for dn in list(definedNames):
            if dn.text and '!' in dn.text:
                sheet_in_ref = dn.text.split('!')[0].replace("'", "")
                if sheet_in_ref not in [sheet.attrib['name'] for sheet in sheets_elem.findall('ns:sheet', ns)]:
                    definedNames.remove(dn)
        if len(definedNames) == 0:
            root_wb.remove(definedNames)

    # 5️⃣ Identifica tabelle attive
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

    # Salva workbook.xml aggiornato
    tree_wb.write(workbook_path, encoding='utf-8', xml_declaration=True)

    # 6️⃣ Copia in cartella pulita
    cleaned_dir = "temp_xlsx_rebuild_clean"
    if os.path.exists(cleaned_dir):
        shutil.rmtree(cleaned_dir)
    shutil.copytree(temp_dir, cleaned_dir)

    # 7️⃣ Rimuovi fogli e rels orfani
    ws_dir = os.path.join(cleaned_dir, "xl", "worksheets")
    if os.path.exists(ws_dir):
        active_sheet_rels = {os.path.basename(fa) + ".rels" for fa in active_sheet_files}
        rels_subdir = os.path.join(ws_dir, "_rels")
        if os.path.exists(rels_subdir):
            for f in os.listdir(rels_subdir):
                full_path = os.path.join(rels_subdir, f)
                if os.path.isfile(full_path) and f not in active_sheet_rels:
                    os.remove(full_path)
        for f in os.listdir(ws_dir):
            full_path = os.path.join(ws_dir, f)
            if os.path.isfile(full_path) and f not in [os.path.basename(fa) for fa in active_sheet_files]:
                os.remove(full_path)

    # 8️⃣ Rimuovi tabelle orfane
    tables_dir = os.path.join(cleaned_dir, "xl", "tables")
    if os.path.exists(tables_dir):
        for f in os.listdir(tables_dir):
            full_path = os.path.join(tables_dir, f)
            if os.path.isfile(full_path) and f not in [os.path.basename(fa) for fa in active_table_files]:
                os.remove(full_path)

    # 9️⃣ Ricrea XLSX finale
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root_dir, _, files in os.walk(cleaned_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, cleaned_dir)
                zout.write(full_path, rel_path)

    # 10️⃣ Pulisci temporanei
    shutil.rmtree(temp_dir)
    shutil.rmtree(cleaned_dir)

    print(f"✅ File XLSX completamente ricostruito e compatibile COM: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python rebuild_xlsx.py <file.xlsx>")
        sys.exit(1)

    file_path = os.path.abspath(sys.argv[1])
    rebuild_xlsx(file_path)
