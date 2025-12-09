import uuid
import subprocess
import wmi

def get_mac_address():
    # Usa uuid.getnode() e formatta come MAC
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

def get_lan_speed():
    c = wmi.WMI()
    
    # Recupera la prima scheda di rete fisica con velocità nota
    for nic in c.Win32_NetworkAdapter():
        if nic.Speed and nic.NetConnectionStatus == 2:  # 2 = connessa
            speed_mbps = int(nic.Speed) / 1_000_000
            return f"{speed_mbps} Mbps"

    return "Nessuna scheda LAN attiva trovata"

if __name__ == "__main__":
    print("MAC Address:", get_mac_address())
    print("Serial Number:", get_serial_number())
    print("Velocità LAN:", get_lan_speed())
