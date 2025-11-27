Search-ADAccount -AccountInactive -TimeSpan 30.00:00:00 -UsersOnly |Sort-Object |  Where-Object { $_.Enabled -eq $true } | FT Name,ObjectClass -A 

#vecchia versione:
#Search-ADAccount -AccountInactive -TimeSpan 30.00:00:00 -UsersOnly |Sort-Object | FT Name,ObjectClass -A