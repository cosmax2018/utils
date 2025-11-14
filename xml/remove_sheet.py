import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import shutil

def remove_sheet(xlsx_path, sheet_name, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(xlsx_path)
        output_path = f"{base}_modified{ext}"

    temp_dir = "temp_xlsx_dir"
    
    # 1. Estrai tutto il contenuto dello xlsx
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    with zipfile.ZipFile(xlsx_path, 'r') as zin:
        zin.extractall(temp_dir)

    # 2. Identifica il sheet da eliminare nel workbook.xml
    workbook_path = os.path.join(temp_dir, "xl", "workbook.xml")
    tree = ET.parse(workbook_path)
    root = tree.getroot()
    ns = {'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    # Trova il foglio da eliminare
    sheets = root.find('ns:sheets', ns)
    sheet_to_remove = None
    sheet_id = None
    for sheet in sheets.findall('ns:sheet', ns):
        if sheet.attrib.get('name') == sheet_name:
            sheet_to_remove = sheet
            sheet_id = sheet.attrib.get('r:id')
            break
    if sheet_to_remove is None:
        print(f"❌ Foglio '{sheet_name}' non trovato!")
        shutil.rmtree(temp_dir)
        return False
    
    sheets.remove(sheet_to_remove)
    tree.write(workbook_path, xml_declaration=True, encoding='UTF-8')

    # 3. Rimuovi il file sheetN.xml corrispondente
    # Bisogna risolvere il riferimento r:id nel workbook.xml.rels
    rels_path = os.path.join(temp_dir, "xl", "_rels", "workbook.xml.rels")
    tree_rels = ET.parse(rels_path)
    root_rels = tree_rels.getroot()
    ns_rel = {'rel':'http://schemas.openxmlformats.org/package/2006/relationships'}
    target_sheet_file = None

    for rel in root_rels.findall('rel:Relationship', ns_rel):
        if rel.attrib.get('Id') == sheet_id:
            target_sheet_file = rel.attrib.get('Target').replace('/', os.sep)
            root_rels.remove(rel)
            break

    tree_rels.write(rels_path, xml_declaration=True, encoding='UTF-8')

    # Cancella i file fisici: sheet xml + rels
    if target_sheet_file:
        full_sheet_path = os.path.join(temp_dir, "xl", target_sheet_file)
        if os.path.exists(full_sheet_path):
            os.remove(full_sheet_path)
        rels_sheet = full_sheet_path.replace('.xml', '.xml.rels')
        if os.path.exists(rels_sheet):
            os.remove(rels_sheet)

    # 4. Ricrea il file xlsx
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zout.write(full_path, rel_path)

    shutil.rmtree(temp_dir)
    print(f"✅ Foglio '{sheet_name}' eliminato. Nuovo file: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python remove_sheet.py <file.xlsx> <sheet_name>")
        sys.exit(1)

    file_path = os.path.abspath(sys.argv[1])
    sheet_name = sys.argv[2]

    remove_sheet(file_path, sheet_name)
