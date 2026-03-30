# -------------------------------------------------------------------------------------------
#
# serial.py : legge il seriale dai cell Android collegati via USB
#
# -------------------------------------------------------------------------------------------
#
# written by Massimiliano Cosmelli ( @_°° massimiliano.cosmelli@accelleron-industries.com )
#
#                   CopyRight 2025-2026 Accelleron Industries 
#
# -------------------------------------------------------------------------------------------

import subprocess

def get_connected_devices():
    ADB_PATH= r"C:\Users\ITMACOS\scrcpy-win64-v3.3.2\adb.exe"
    result = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]
    
    devices = []
    for line in lines:
        if "device" in line:
            serial = line.split()[0]
            devices.append(serial)
    
    return devices

def get_device_info(serial):
    info = {}
    
    def adb_shell(cmd):
        result = subprocess.run(
            ["adb", "-s", serial, "shell"] + cmd,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    info["serial"] = serial
    info["model"] = adb_shell(["getprop", "ro.product.model"])
    info["brand"] = adb_shell(["getprop", "ro.product.brand"])
    
    return info

if __name__ == "__main__":
    devices = get_connected_devices()
    
    if not devices:
        print("Nessun dispositivo collegato")
    else:
        for dev in devices:
            info = get_device_info(dev)
            print("Dispositivo trovato:")
            for k, v in info.items():
                print(f"  {k}: {v}")
            print("-" * 30)