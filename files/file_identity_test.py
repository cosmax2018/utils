# -------------------------------------------------------------------------------------------
#
# file_identity_test.py : testa se due files sono identici byte a byte
#                
# -------------------------------------------------------------------------------------------
#
# written by Massimiliano Cosmelli ( @_°° massimiliano.cosmelli@accelleron-industries.com )
#
#                   CopyRight 2025-2026 Accelleron Industries 
#
# -------------------------------------------------------------------------------------------

import os,sys,hashlib
from pathlib import Path

def check_identity(file1,file2):
    
    file1 = Path(f"{file1}")
    file2 = Path(f"{file2}") 

    def sha256(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
        
    print()
    print(f"file1: {file1}")
    print(f"file2: {file2}")
    print(f"size file1: {file1.stat().st_size}")
    print(f"size file2: {file2.stat().st_size}")
    print(f"sha256 file1: {sha256(file1)}")
    print(f"sha256 file2: {sha256(file2)}")
    print(f"identici: {sha256(file1) == sha256(file2)}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: file_identity_test.py <file1> <file2>")
        sys.exit(1)
        
    check_identity(sys.argv[1],sys.argv[2])
    
    