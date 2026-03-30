import subprocess
import re

def adb_shell(serial, cmd):
    result = subprocess.run(
        ["adb", "-s", serial, "shell"] + cmd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def get_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]
    return [line.split()[0] for line in lines if "device" in line]

def get_imei_root(serial):
    # comando che richiede root
    raw = adb_shell(serial, ["su", "-c", "service call iphonesubinfo 1"])
    
    # parsing dell'output (hex -> ascii)
    hex_values = re.findall(r"0x[0-9a-fA-F]+", raw)
    
    imei = ""
    for h in hex_values:
        # converte ogni blocco hex in stringa
        try:
            bytes_obj = bytes.fromhex(h[2:])
            imei += bytes_obj.decode(errors="ignore")
        except:
            pass
    
    # pulizia: tieni solo numeri
    imei = "".join(filter(str.isdigit, imei))
    
    return imei if imei else "IMEI non trovato"

if __name__ == "__main__":
    devices = get_devices()
    
    if not devices:
        print("Nessun dispositivo collegato")
    else:
        for dev in devices:
            imei = get_imei_root(dev)
            print(f"{dev} -> IMEI: {imei}")