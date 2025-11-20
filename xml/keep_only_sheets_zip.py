import zipfile
import shutil
import os
import sys
import xml.etree.ElementTree as ET

def keep_only_sheets_clean(input_path, sheets_to_keep, output_path=None):
    """
    Mantiene solo i fogli specificati in sheets_to_keep in un file .xlsx esistente,
    eliminando anche relazioni, tabelle e riferimenti a fogli rimossi, inclusi i nomi definiti.
    """
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_filtered.xlsx"

    temp_dir = f"{output_path}_temp"

    # 1️⃣ Estrai il file ZIP
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # 2️⃣ Carica xl/workbook.xml
    workbook_xml_path = os.path.join(temp_dir, 'xl', 'workbook.xml')
    tree = ET.parse(workbook_xml_path)
    root = tree.getroot()
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

    # Mappa nome foglio → (sheetId, rId)
    sheets = {}
    for sheet in root.find('ns:sheets', ns):
        rid = sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        sheets[sheet.attrib['name']] = (sheet.attrib['sheetId'], rid)

    # 3️⃣ Carica xl/_rels/workbook.xml.rels
    rels_path = os.path.join(temp_dir, 'xl', '_rels', 'workbook.xml.rels')
    rels_tree = ET.parse(rels_path)
    rels_root = rels_tree.getroot()
    rels_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    rId_to_target = {}
    for rel in rels_root.findall('r:Relationship', rels_ns):
        rId_to_target[rel.attrib['Id']] = rel.attrib['Target']  # es. worksheets/sheet2.xml

    # 4️⃣ Determina quali sheet eliminare
    sheets_to_keep_set = set(sheets_to_keep)
    sheets_to_remove = [name for name in sheets if name not in sheets_to_keep_set]

    # 5️⃣ Rimuovi sheet, rels e tabelle collegate
    sheets_elem = root.find('ns:sheets', ns)
    tables_dir = os.path.join(temp_dir, 'xl', 'tables')
    if not os.path.exists(tables_dir):
        os.makedirs(tables_dir)  # assicurati che esista

    for sheet_name in sheets_to_remove:
        sheetId, rId = sheets[sheet_name]

        # 🔹 Rimuovi dal workbook.xml
        for s in sheets_elem.findall('ns:sheet', ns):
            rid_attr = s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if s.attrib['name'] == sheet_name and rid_attr == rId:
                sheets_elem.remove(s)
                break

        # 🔹 Rimuovi file fisico sheet
        if rId in rId_to_target:
            target_file = rId_to_target[rId]  # worksheets/sheetX.xml
            sheet_file_path = os.path.join(temp_dir, 'xl', target_file.replace('/', os.sep))
            if os.path.exists(sheet_file_path):
                os.remove(sheet_file_path)

            # 🔹 Rimuovi rels del sheet
            rels_file_path = os.path.join(temp_dir, 'xl', '_rels', os.path.basename(target_file) + '.rels')
            if os.path.exists(rels_file_path):
                os.remove(rels_file_path)

        # 🔹 Rimuovi rel dallo XML rels
        for rel in rels_root.findall('r:Relationship', rels_ns):
            if rel.attrib['Id'] == rId:
                rels_root.remove(rel)
                break

    # 6️⃣ Rimuovi eventuali tabelle che puntano a fogli rimossi
    if os.path.exists(tables_dir):
        for table_file in os.listdir(tables_dir):
            table_path = os.path.join(tables_dir, table_file)
            tree_tbl = ET.parse(table_path)
            root_tbl = tree_tbl.getroot()
            ref = root_tbl.attrib.get('ref', '')  # es. Sheet2!A1:B10
            if any(sheet in ref for sheet in sheets_to_remove):
                os.remove(table_path)  # elimina la tabella

    # 7️⃣ Rimuovi definedNames che puntano a fogli rimossi
    defined_names_elem = root.find('ns:definedNames', ns)
    if defined_names_elem is not None:
        for defined_name in list(defined_names_elem):
            text = defined_name.text or ''
            if any(sheet in text for sheet in sheets_to_remove):
                defined_names_elem.remove(defined_name)
        # Se rimane vuoto, rimuovi l'elemento
        if len(defined_names_elem) == 0:
            root.remove(defined_names_elem)

    # 8️⃣ Salva workbook.xml e workbook.xml.rels
    tree.write(workbook_xml_path, encoding='utf-8', xml_declaration=True)
    rels_tree.write(rels_path, encoding='utf-8', xml_declaration=True)

    # 9️⃣ Ricrea il file XLSX finale
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    # 🔟 Pulisci cartella temporanea
    shutil.rmtree(temp_dir)
    print(f"✅ File salvato mantenendo solo i fogli: {sheets_to_keep}. Output: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python keep_only_sheets_clean.py <file.xlsx> <foglio1> [<foglio2> ...]")
        sys.exit(1)

    file_path = os.path.abspath(sys.argv[1])
    sheets = sys.argv[2:]
    keep_only_sheets_clean(file_path, sheets)
