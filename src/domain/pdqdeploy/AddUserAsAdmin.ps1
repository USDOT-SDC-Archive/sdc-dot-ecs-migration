$map = @{
"name_of_machine" = "primary_username";
};


$LocalGroup = "Administrators"
$Computer   = $env:computername
$Domain     = $env:userdomain
$DomainUser = $map[$Computer]

([ADSI]"WinNT://$Computer/$LocalGroup,group").psbase.Invoke("Add",([ADSI]"WinNT://$Domain/$DomainUser").path)
