import difflib
from pathlib import Path

DIR_A = Path("C:/Users/ITMACOS/Downloads/miei-scritti-main/miei-scritti-main")  # prima directory
DIR_B = Path("C:/Users/ITMACOS/Downloads/miei-scritti/miei-scritti")            # seconda directory

def get_txt_files(directory):
    """
    Ritorna un dizionario {nome_file: Path}
    solo per file .txt
    """
    return {
        f.name: f
        for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() == ".txt"
    }


def compare_files(file_a: Path, file_b: Path):
    """
    Mostra le differenze tra due file di testo
    """
    with file_a.open(encoding="utf-8", errors="ignore") as fa:
        a_lines = fa.readlines()

    with file_b.open(encoding="utf-8", errors="ignore") as fb:
        b_lines = fb.readlines()

    diff = difflib.unified_diff(
        a_lines,
        b_lines,
        fromfile=str(file_a),
        tofile=str(file_b),
        lineterm=""
    )

    if next(diff, None) is None:
        return False    # esce...
        
    for line in diff:
        print(line)

    return True

def main():
    files_a = get_txt_files(DIR_A)
    files_b = get_txt_files(DIR_B)

    common_files = set(files_a.keys()) & set(files_b.keys())

    if not common_files:
        print("Nessun file .txt con nome identico trovato.")
        return

    for filename in sorted(common_files):
        file_a = files_a[filename]
        file_b = files_b[filename]

        size_a = file_a.stat().st_size
        size_b = file_b.stat().st_size

        if size_a != size_b:
            if compare_files(file_a, file_b):
                print("\n" + "=" * 80)
                print(f"DIFFERENZE PER FILE: {filename}")
                print(f"Dimensioni: {size_a} vs {size_b}")
                print("=" * 80)

            


if __name__ == "__main__":
    main()
