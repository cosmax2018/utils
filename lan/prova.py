import subprocess

ps_command = r"""
Get-NetAdapter |
Select-Object Name, InterfaceDescription, Status, LinkSpeed
"""

result = subprocess.check_output(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command]
)

print(result.decode("utf-8", errors="ignore"))
