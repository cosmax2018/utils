import socket
import time

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 1024 * 1024  # 1 MB

def run_server():
    print(f"Server in ascolto su {HOST}:{PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f"Connessione da: {addr}")

    total_received = 0
    start = time.time()

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        total_received += len(data)

    end = time.time()
    conn.close()
    s.close()

    elapsed = end - start
    mbps = (total_received * 8) / (elapsed * 1_000_000)
    print(f"Ricevuti: {total_received / 1_000_000:.2f} MB in {elapsed:.2f} s → {mbps:.2f} Mbps")

if __name__ == "__main__":
    run_server()
