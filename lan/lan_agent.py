
# Agent (server) da installare su ogni PC del dominio

# Creiamo un piccolo server che rimane in ascolto sulla
# porta 5001 per il test di velocità LAN.

import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 1024 * 1024  # 1 MB

def handle_client(conn, addr):
    total_received = 0
    start = time.time()

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        total_received += len(data)

    elapsed = time.time() - start
    conn.close()

    if elapsed > 0:
        mbps = (total_received * 8) / (elapsed * 1_000_000)
        print(f"{addr[0]} → {mbps:.2f} Mbps")

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(50)

    print(f"[AGENT] In ascolto su {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    server()
