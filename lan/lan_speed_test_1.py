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
        result = result.decode().split("\n")[1].strip()
        return result
    except:
        return "N/D"

def get_lan_speed_only():
    c = wmi.WMI()

    for nic in c.Win32_NetworkAdapter():

        # ---- Identificazione della LAN ----
        #   AdapterTypeID == 0 → Ethernet  (LAN)
        #   Skippa Wi-Fi (9) e altri
        #
        if nic.AdapterTypeID != 0:
            continue

        # Deve essere connessa
        if nic.NetConnectionStatus != 2:  # 2 = Connected
            continue

        # Deve avere velocità nota
        if nic.Speed:
            speed_mbps = int(nic.Speed) / 1_000_000
            return f"{speed_mbps} Mbps"

    return "Nessuna LAN attiva trovata"

if __name__ == "__main__":
    print("MAC Address:", get_mac_address())
    print("Serial Number:", get_serial_number())
    print("Velocità LAN:", get_lan_speed_only())
