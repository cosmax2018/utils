
function Get-RandomCharacters($length, $characters) {
    $random = 1..$length | ForEach-Object { Get-Random -Maximum $characters.length }
    $private:ofs=""
    return [String]$characters[$random]
}
 
function Scramble-String([string]$inputString){     
    $characterArray = $inputString.ToCharArray()   
    $scrambledStringArray = $characterArray | Get-Random -Count $characterArray.Length     
    $outputString = -join $scrambledStringArray
    return $outputString 
}

function Get-RandomPassword($n_lowercase, $n_uppercase, $n_numbers, $n_symbols) {
	$password  = Get-RandomCharacters -length $n_lowercase -characters 'abcdefghiklmnoprstuvwxyz'
	$password += Get-RandomCharacters -length $n_uppercase -characters 'ABCDEFGHKLMNOPRSTUVWXYZ'
	$password += Get-RandomCharacters -length $n_numbers   -characters '1234567890'
	$password += Get-RandomCharacters -length $n_symbols   -characters '!"§$%&/()=?}][{@#*+'
	$password  = Scramble-String $password	
	return $password
}

$Disabled_users = (Get-ADUser -Filter * -Property Enabled | Where-Object {$_.Enabled -like 'false'} | FT Name, Enabled -Autosize)

foreach ($User in $Disabled_users.SamAccountName)
{

	Set-ADAccountPassword -identity $User -NewPassword (ConvertTo-SecureString $new_random_passwd -AsPlainText -force)
	
	
	# if($Enabled)
	# {
		# $new_random_passwd = Get-RandomPassword(12,2,3,5)
		# Set-ADAccountPassword -identity $SAM -NewPassword (ConvertTo-SecureString $new_random_passwd -AsPlainText -force)
	# }
	# else
	# {
		# Write-Host "ATTENZIONE: L'utente" $user.name "risulta disabilitato, pertanto non sono state apportate modifiche."
	# }
	
	Write-Host "L'utente" $User.name "risulta abilitato"
}