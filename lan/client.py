
# Da lanciare sul PC che esegue il test.

# pip install psutil

# uso:
# avvia il client con  > python client.py

# nota:  Questo test misura principalmente la velocità di upload 
#        del client verso il server (il caso più utile per test LAN).

import socket
import uuid
import psutil
import time

SERVER_IP = "192.168.1.10"   # <--- Metti IP del server
PORT = 5001
BUFFER_SIZE = 1024 * 1024  # 1 MB
TEST_DURATION = 5  # secondi

# ---- Mostra MAC address + info rete ----
def show_network_info():
    addrs = psutil.net_if_addrs()
    for iface, info_list in addrs.items():
        ipv4 = None
        mac = None
        for info in info_list:
            if info.family == socket.AF_INET:
                ipv4 = info.address
            if info.family == psutil.AF_LINK:
                mac = info.address

        if ipv4:
            print(f"Interfaccia: {iface}")
            print(f"  IPv4: {ipv4}")
            print(f"  MAC : {mac}")
            print("")

def test_upload_speed():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))

    print("\nInvio dati...")
    data = b"X" * BUFFER_SIZE

    start = time.time()
    sent = 0

    while time.time() - start < TEST_DURATION:
        s.sendall(data)
        sent += len(data)

    s.close()

    elapsed = time.time() - start
    mbps = (sent * 8) / (elapsed * 1_000_000)
    print(f"Inviati: {sent/1_000_000:.2f} MB in {elapsed:.2f}s → {mbps:.2f} Mbps")

if __name__ == "__main__":
    show_network_info()
    test_upload_speed()
