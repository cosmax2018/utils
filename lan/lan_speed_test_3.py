import uuid
import subprocess
import wmi

def get_mac_address():
    mac_num = uuid.getnode()
    mac = ":".join([f"{(mac_num >> ele) & 0xff:02x}" for ele in range(40, -1, -8)])
    return mac.upper()

def get_serial_number():
    try:
        result = subprocess.check_output(["wmic", "bios", "get", "serialnumber"], shell=True)
        return result.decode().split("\n")[1].strip()
    except:
        return "N/D"

def get_lan_speed_docking_safe():

    c = wmi.WMI()

    # Parole chiave da evitare
    blacklist = ["wifi", "wireless", "wlan", "virtual", "vmware", 
                 "hyper-v", "bluetooth", "loopback", "ndis"]

    for nic in c.Win32_NetworkAdapter():

        name = (nic.Name or "").lower()

        # Skip interfacce non desiderate
        if any(bad in name for bad in blacklist):
            continue

        # Deve avere hardware reale (USB o PCI)
        if not getattr(nic, "PhysicalAdapter", False):
            continue

        # Deve essere abilitata
        if not getattr(nic, "NetEnabled", False):
            continue

        # Deve essere connessa (status 2)
        if nic.NetConnectionStatus != 2:
            continue

        # Deve avere velocità nota
        if nic.Speed:
            speed_mbps = int(nic.Speed) / 1_000_000
            return f"{speed_mbps} Mbps"

    return "Nessuna LAN attiva trovata"

if __name__ == "__main__":
    print("MAC Address:", get_mac_address())
    print("Serial Number:", get_serial_number())
    print("Velocità LAN:", get_lan_speed_docking_safe())
