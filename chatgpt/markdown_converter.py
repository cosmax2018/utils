
# script Python per **convertire i file Markdown esportati in questo formato “lineare” 
# pronto da incollare**.

import os

INPUT_DIR = "conversazioni_markdown"
OUTPUT_DIR = "conversazioni_chatgpt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for fname in os.listdir(INPUT_DIR):
    if not fname.endswith(".md"):
        continue

    with open(os.path.join(INPUT_DIR, fname), "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = ["Contesto storico: conversazione precedente tra utente e assistente.\n"]
    role = ""
    for line in lines:
        line = line.strip()
        if line.startswith("## "):
            role = "Utente" if "User" in line else "Assistente"
        elif line and not line.startswith("#"):
            output_lines.append(f"{role}: {line}\n")

    out_fname = os.path.join(OUTPUT_DIR, fname)
    with open(out_fname, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

print(f"Convertiti {len(os.listdir(OUTPUT_DIR))} file in formato ChatGPT pronto da incollare.")