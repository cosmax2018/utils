# Script centrale di audit LAN
# Questo script:
# scopre i computer del dominio (net view)
# pinga ogni PC
# prende il MAC
# testa la velocità LAN collegandosi all’agent remoto

genera un report finale
import subprocess
import socket
import time
import csv
import re

PORT = 5001
BUFFER_SIZE = 1024 * 1024
TEST_DURATION = 3  # secondi


def get_domain_pcs():
    output = subprocess.check_output("net view", shell=True, text=True)
    pcs = re.findall(r"\\\\([A-Z0-9_-]+)", output, re.IGNORECASE)
    return pcs


def ping(host):
    try:
        output = subprocess.check_output(f"ping -n 1 {host}", shell=True, text=True)
        time_ms = re.search(r"tempo=([0-9]+)ms", output)
        return int(time_ms.group(1)) if time_ms else None
    except:
        return None


def get_mac(ip):
    try:
        subprocess.run("arp -d", shell=True)  # svuota cache
        subprocess.run(f"ping -n 1 {ip}", shell=True, stdout=subprocess.DEVNULL)
        output = subprocess.check_output("arp -a", shell=True, text=True)
        match = re.search(rf"{ip}\s+([a-fA-F0-9-]+)", output)
        return match.group(1) if match else None
    except:
        return None


def test_lan_speed(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, PORT))
    except:
        return None

    data = b"X" * BUFFER_SIZE
    start = time.time()
    sent = 0

    while time.time() - start < TEST_DURATION:
        try:
            s.sendall(data)
            sent += len(data)
        except:
            break

    s.close()

    elapsed = time.time() - start
    if elapsed == 0:
        return None

    mbps = (sent * 8) / (elapsed * 1_000_000)
    return mbps


def resolve_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except:
        return None


def main():
    pcs = get_domain_pcs()
    print(f"Trovati {len(pcs)} PC nel dominio.\n")

    results = []

    for pc in pcs:
        print(f"--- {pc} ---")

        ip = resolve_ip(pc)
        if not ip:
            print("  ❌ Impossibile risolvere IP\n")
            continue

        latency = ping(pc)
        mac = get_mac(ip)
        speed = test_lan_speed(ip)

        print(f"  IP      : {ip}")
        print(f"  Ping    : {latency} ms")
        print(f"  MAC     : {mac}")
        print(f"  LAN Mbps: {speed:.2f} Mbps" if speed else "  ❌ Test velocità fallito")
        print()

        results.append([pc, ip, latency, mac, speed])

    # Salva report CSV
    with open("audit_lan_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["PC", "IP", "Ping (ms)", "MAC", "Speed Mbps"])
        writer.writerows(results)

    print("\nReport generato: audit_lan_report.csv")


if __name__ == "__main__":
    main()
