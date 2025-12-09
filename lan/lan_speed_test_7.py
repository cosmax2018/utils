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


def get_lan_speed():
    """
    Rileva la LAN attiva (USB-C, Docking, PCIe, ecc.)
    usando PowerShell. Funziona in tutti i casi.
    """

    ps_command = r"""
    Get-NetAdapter |
    Where-Object {
        $_.Status -eq 'Up' -and
        $_.LinkSpeed -ne $null -and
        $_.InterfaceDescription -notmatch 'Wi-Fi|Wireless|Bluetooth|Virtual|Hyper|VMware'
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

        # Caso singolo adattatore
        if isinstance(data, dict):
            return f"{data['Name']} ({data['LinkSpeed']})"

        # Caso più adattatori Up
        if isinstance(data, list) and len(data) > 0:
            best = data[0]
            return f"{best['Name']} ({best['LinkSpeed']})"

        return "Nessuna LAN attiva"

    except Exception as e:
        return f"Errore PowerShell: {e}"


if __name__ == "__main__":
    print("MAC:", get_mac_address())
    print("Serial:", get_serial_number())
    print("LAN:", get_lan_speed())
