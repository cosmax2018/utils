import difflib
import hashlib
from pathlib import Path


DIR_A = Path("C:/Users/ITMACOS/Downloads/miei-scritti-main/miei-scritti-main")  # prima directory
DIR_B = Path("C:/Users/ITMACOS/Downloads/miei-scritti/miei-scritti")            # seconda directory


def get_txt_files(directory):
    return {
        f.name: f
        for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() == ".txt"
    }


def file_hash(path: Path) -> str:
    """
    Calcola hash SHA-256 del file
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_lines(path: Path):
    """
    Ritorna le linee del file:
    - senza righe vuote
    - senza spazi iniziali/finali
    """
    lines = []
    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line + "\n")
    return lines


def compare_files(file_a: Path, file_b: Path):
    lines_a = normalized_lines(file_a)
    lines_b = normalized_lines(file_b)

    diff = difflib.unified_diff(
        lines_a,
        lines_b,
        fromfile=str(file_a),
        tofile=str(file_b),
        lineterm=""
    )

    if next(diff, None) is None:
        return False    # esce...
        
    for line in diff:
        print(f'differences:\n{line}')        
        
    return True


def main():
    files_a = get_txt_files(DIR_A)
    files_b = get_txt_files(DIR_B)

    common_files = set(files_a) & set(files_b)

    if not common_files:
        print("Nessun file .txt con nome identico trovato.")
        return

    for filename in sorted(common_files):
        file_a = files_a[filename]
        file_b = files_b[filename]

        size_a = file_a.stat().st_size
        size_b = file_b.stat().st_size

        if size_a != size_b:
            hash_a = file_hash(file_a)
            hash_b = file_hash(file_b)

            if compare_files(file_a, file_b):
                print("\n" + "=" * 90)
                print(f"FILE: {filename}")
                print(f"Dimensioni: {size_a} vs {size_b}")
                print(f"SHA-256 A: {hash_a}")
                print(f"SHA-256 B: {hash_b}")
                print("=" * 90)

            


if __name__ == "__main__":
    main()
