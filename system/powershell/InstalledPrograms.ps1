$username= $env:Username
$date= Get-Date -uformat "%d-%m-%Y"
$pc= $env:COMPUTERNAME
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table –AutoSize > "$home\desktop\$date $pc $username.txt"