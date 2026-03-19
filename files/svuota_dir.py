
# svuota_dir.py : svuota una directory lasciandola dov'e'

from pathlib import Path

def svuota_directory(percorso_dir):
    p = Path(percorso_dir)

    if not p.exists():
        print("Directory non esiste")
        return

    for item in p.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()          # cancella file/link
        elif item.is_dir():
            shutil.rmtree(item)    # cancella sottodirectory
               