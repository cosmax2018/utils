import subprocess, json

# ottieni lista pacchetti outdated
result = subprocess.run(["pip", "list", "--outdated", "--format=json"],
                        capture_output=True, text=True)

packages = json.loads(result.stdout)

for pkg in packages:
    name = pkg["name"]
    print(f"Aggiorno {name}...")
    subprocess.run(["pip", "install", "--upgrade", name])
