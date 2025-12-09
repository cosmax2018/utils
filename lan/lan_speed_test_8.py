import json
import subprocess

def get_lan_speed_safe():
    try:
        # Prendiamo TUTTI gli adattatori Up in formato JSON
        ps = r"""
        $adapters = Get-NetAdapter;
        $list = @();
        foreach ($a in $adapters) {
            $list += [PSCustomObject]@{
                Name = $a.Name;
                Desc = $a.InterfaceDescription;
                Status = $a.Status;
                Speed = $a.LinkSpeed;
            }
        }
        $list | ConvertTo-Json
        """
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps]
        ).decode("utf-8", errors="ignore")

        data = json.loads(out)

        # Convert JSON to list always
        if isinstance(data, dict):
            data = [data]

        # scegliamo l’adattatore corretto
        for a in data:
            desc = a["Desc"].lower()
            if ("wifi" in desc or "wireless" in desc or "virtual" in desc or "bluetooth" in desc):
                continue
            if a["Status"] == "Up" and a["Speed"] and a["Speed"] != "0 bps":
                return f"{a['Name']} ({a['Speed']})"

        return "Nessuna LAN rilevata"

    except Exception as e:
        return f"Errore: {e}"

print(get_lan_speed_safe())
