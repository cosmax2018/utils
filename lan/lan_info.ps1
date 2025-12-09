$adapter = Get-NetAdapter |
    Where-Object { $_.Status -eq "Up" -and $_.LinkSpeed -gt 0 }

if (-not $adapter) {
    Write-Host "❌ Nessuna LAN rilevata"
    exit
}

# IP Address
$ip = (Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 |
        Select-Object -ExpandProperty IPAddress)

# MAC address della LAN attiva (docking)
$macDocking = $adapter.MacAddress

# MAC address del PC (scheda integrata)
$macPC = (Get-NetAdapter |
            Where-Object { $_.InterfaceDescription -match "I219" } |
            Select-Object -ExpandProperty MacAddress)

# Serial Number del PC
$serial = (Get-WmiObject Win32_BIOS).SerialNumber

# Velocità link
$linkSpeed = $adapter.LinkSpeed

Write-Host "LAN rilevata:"
Write-Host "  Interfaccia: $($adapter.Name)"
Write-Host "  Descrizione: $($adapter.InterfaceDescription)"
Write-Host "  IP address : $ip"
Write-Host "  MAC Docking: $macDocking"
Write-Host "  MAC PC     : $macPC"
Write-Host "  Serial PC  : $serial"
Write-Host "  Velocità   : $linkSpeed"
