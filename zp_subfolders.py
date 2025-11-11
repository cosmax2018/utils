import os
import zipfile
import shutil

def compress_subfolders(root_folder):
    """
    Comprime ogni sottocartella della cartella radice in un file ZIP con massima compressione
    e cancella la sottocartella dopo la compressione.
    
    :param root_folder: Percorso della cartella radice.
    """
    if not os.path.isdir(root_folder):
        print("Errore: La cartella specificata non esiste.")
        return
    
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):  # Verifica che sia una cartella
            zip_filename = os.path.join(root_folder, f"{folder_name}.zip")
            
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=folder_path)
                        zipf.write(file_path, arcname)
            
            print(f"Cartella compressa: {zip_filename}")
            # shutil.rmtree(folder_path)  # Cancella la sottocartella dopo la compressione
            # print(f"Cartella eliminata: {folder_path}")

if __name__ == "__main__":
    root_path = input("Inserisci il percorso della cartella radice: ")
    compress_subfolders(root_path)
