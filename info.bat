@echo off 
REM -------------------------------------------------------------------------------------------
REM
REM  info.bat : extract info from a local machine under windows
REM
REM -------------------------------------------------------------------------------------------
REM
REM  written by Massimiliano Cosmelli ( @_°° massimiliano.cosmelli@accelleron-industries.com )
REM
REM                 use this software permitted under MIT License 2025
REM
REM -------------------------------------------------------------------------------------------

set OUT_FILE=%computername%.txt

REM ** machine info **
wmic computersystem  get name > %OUT_FILE%
wmic csproduct get name >> %OUT_FILE%
wmic bios get serialnumber >> %OUT_FILE%
wmic baseboard get product,Manufacturer,version,serialnumber >> %OUT_FILE%
wmic COMPUTERSYSTEM get TotalPhysicalMemory >> %OUT_FILE%
wmic diskdrive get serialnumber >> %OUT_FILE%

REM ** windows license **
wmic os get "serialnumber" >> %OUT_FILE%
wmic path softwarelicensingservice get OA3xOriginalProductKey >> %OUT_FILE%
wmic os list brief >> %OUT_FILE%

REM ** programs installed **
wmic product list brief >> %OUT_FILE%

REM ** MS-OFFICE **
wmic product where "Name like '%%OFFICE%%'" get Name  >> %OUT_FILE%

REM ** ADOBE Acrobat **
wmic product where "Name like '%%ADOBE%%'" get Name >> %OUT_FILE%

echo si prega di inviare per email a reti.sistemi@softeco.it
echo il file %OUT_FILE%
echo grazie.

pause
REM exit
