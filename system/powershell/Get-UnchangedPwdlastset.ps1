
param (
    [int]    $PwdAge = 180,
    [ValidatePattern('(?# OU Path should start with "LDAP://")^LDAP://.*')]
    [string] $SearchBase
)
$PwdDate = (Get-Date).AddDays(-$PwdAge).ToFileTime()

$SearcherProps = @{
    Filter   = "(&(objectclass=user)(objectcategory=person)(pwdlastset<=$PwdDate))"
    PageSize = 500
}

if ($SearchBase) {
    $SearcherProps.SearchRoot = $SearchBase
}

(New-Object DirectoryServices.DirectorySearcher -Property $SearcherProps).FindAll() | ForEach-Object {
    New-Object -TypeName PSCustomObject -Property @{
        samaccountname = $_.Properties.samaccountname -join ''
        pwdlastset     = [datetime]::FromFileTime([long](-join $_.Properties.pwdlastset))
        enabled        = -not [bool]([long](-join $_.properties.useraccountcontrol) -band 2)
    }
}