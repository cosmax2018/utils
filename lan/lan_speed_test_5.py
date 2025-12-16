import uuid
import subprocess
import json

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


def get_lan_speed_powershell():
    """
    Usa PowerShell perché è l’unico modo affidabile con docking station USB/Thunderbolt.
    """

    ps_command = r"""
    Get-NetAdapter |
    Where-Object {
        $_.Status -eq 'Up' -and
        $_.InterfaceDescription -notmatch 'Wi-Fi|Wireless' -and
        $_.InterfaceDescription -match 'Ethernet'
    } |
    Select-Object Name, InterfaceDescription, LinkSpeed |
    ConvertTo-Json
    """

    try:
        output = subprocess.check_output(
            ["powershell", "-Command", ps_command],
            shell=True
        ).decode("utf-8").strip()

        if not output:
            return "Nessuna LAN rilevata"

        data = json.loads(output)

        # Se c'è una sola scheda, data è un dict
        if isinstance(data, dict):
            return data["LinkSpeed"]

        # Se ce ne sono più, prendi la prima attiva
        if isinstance(data, list) and len(data) > 0:
            return data[0]["LinkSpeed"]

        return "Nessuna LAN attiva"

    except Exception as e:
        return f"Errore PowerShell: {e}"


if __name__ == "__main__":
    print("MAC Address:", get_mac_address())
    print("Serial Number:", get_serial_number())
    print("Velocità LAN:", get_lan_speed_powershell())
