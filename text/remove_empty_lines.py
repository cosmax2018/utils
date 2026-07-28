
# remove_empty_lines.py

import argparse
from pathlib import Path

def remove_empty_lines(input_file, output_file=None):
    input_path = Path(input_file)

    if output_file is None:
        output_path = input_path
    else:
        output_path = Path(output_file)

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    filtered_lines = [line for line in lines if line.strip()]

    with output_path.open("w", encoding="utf-8", newline="") as f:
        f.writelines(filtered_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Elimina le righe vuote da un file Python."
    )
    parser.add_argument(
        "file",
        help="File .py da processare"
    )

    args = parser.parse_args()

    input_file = Path(args.file)

    if not input_file.is_file():
        parser.error(f"Il file '{input_file}' non esiste.")

    remove_empty_lines(input_file)


if __name__ == "__main__":
    main()