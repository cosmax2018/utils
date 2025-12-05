import subprocess
import wmi
import csv
import re

def get_domain_pcs():
    output = subprocess.check_output("net view", shell=True, text=True)
    pcs = re.findall(r"\\\\([A-Z0-9_-]+)", output, re.IGNORECASE)
    return pcs

def get_link_speed(host):
    try:
        c = wmi.WMI(computer=host)
    except:
        return None, None, None

    for nic in c.Win32_NetworkAdapter():
        # Adapter attivo e fisico (LAN)
        if nic.NetConnectionStatus == 2 and nic.PhysicalAdapter:
            name = nic.Name
            speed = nic.Speed    # in bit/s (es: 1000000000 = 1 Gbps)
            mac = nic.MACAddress
            return name, speed, mac
    
    return None, None, None


def main():
    pcs = get_domain_pcs()
    print(f"Trovati {len(pcs)} PC nel dominio.\n")

    results = []

    for pc in pcs:
        print(f"--- {pc} ---")
        name, speed, mac = get_link_speed(pc)

        if speed:
            gbps = float(speed) / 1_000_000_000
            print(f"  Interfaccia : {name}")
            print(f"  Velocità    : {gbps:.2f} Gbps")
            print(f"  MAC         : {mac}")
        else:
            print("  ❌ Non riesco a leggere la velocità della LAN")

        print()

        results.append([pc, name, speed, mac])

    with open("lan_speed_audit.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["PC", "Interfaccia", "Velocità (bit/s)", "MAC"])
        w.writerows(results)

    print("Report generato: lan_speed_audit.csv")

if __name__ == "__main__":
    main()
