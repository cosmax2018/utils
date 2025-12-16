import json
import os
from datetime import datetime

INPUT_FILE = "conversations.json"
OUTPUT_DIR = "conversazioni_markdown"


def safe_filename(name: str) -> str:
    """Rende il titolo sicuro per il filesystem"""
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()


def load_conversations(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_messages(conversation):
    """
    Ricostruisce i messaggi in ordine cronologico
    gestendo correttamente parts come stringhe o dizionari
    """
    mapping = conversation.get("mapping", {})
    messages = []

    for node in mapping.values():
        msg = node.get("message")
        if not msg:
            continue

        content = msg.get("content", {})
        parts = content.get("parts", [])
        if not parts:
            continue

        text_chunks = []

        for part in parts:
            if isinstance(part, str):
                text_chunks.append(part)
            elif isinstance(part, dict):
                # caso più comune: {"type": "text", "text": "..."}
                if "text" in part:
                    text_chunks.append(part["text"])

        if not text_chunks:
            continue

        role = msg.get("author", {}).get("role", "unknown")
        timestamp = msg.get("create_time")

        messages.append({
            "role": role,
            "text": "\n".join(text_chunks),
            "timestamp": timestamp
        })

    messages.sort(key=lambda x: x["timestamp"] or 0)
    return messages



def format_markdown(title, messages):
    lines = [f"# {title}\n"]

    for m in messages:
        role = m["role"].capitalize()
        lines.append(f"## {role}\n")
        lines.append(m["text"].strip() + "\n")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_conversations(INPUT_FILE)
    exported = 0

    for conv in data:
        title = conv.get("title") or "Conversazione senza titolo"
        messages = extract_messages(conv)

        if not messages:
            continue

        filename = safe_filename(title)[:80]
        timestamp = conv.get("create_time")
        if timestamp:
            dt = datetime.fromtimestamp(timestamp)
            filename = f"{dt:%Y-%m-%d}_{filename}"

        output_path = os.path.join(OUTPUT_DIR, f"{filename}.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(format_markdown(title, messages))

        exported += 1

    print(f"Esportate {exported} conversazioni in '{OUTPUT_DIR}'")


if __name__ == "__main__":
    main()
