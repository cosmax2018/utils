
# compara due files sorgenti .py ed evidenzia le differenze

import sys
import difflib
import re

def clean_code(lines):
    """Rimuove commenti e spazi vuoti dalle righe di codice."""
    cleaned_lines = []
    for line in lines:
        line = re.sub(r'#.*', '', line).strip()  # Rimuove i commenti
        if line:
            cleaned_lines.append(line)
    return cleaned_lines

def compare_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = clean_code(f1.readlines())
        lines2 = clean_code(f2.readlines())
    
    differ = difflib.Differ()
    diff = list(differ.compare(lines1, lines2))
    
    print("\nDifferenze trovate:")
    line_num1, line_num2 = 1, 1
    for line in diff:
        if line.startswith(" "):
            line_num1 += 1
            line_num2 += 1
        elif line.startswith("-"):
            print(f"{file1}, riga {line_num1}: {line[2:]}")
            line_num1 += 1
        elif line.startswith("+"):
            print(f"{file2}, riga {line_num2}: {line[2:]}")
            line_num2 += 1
        elif line.startswith("?"):
            continue  # Linee di aiuto di difflib, non necessarie

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python compare.py file1.py file2.py")
    else:
        compare_files(sys.argv[1], sys.argv[2])
