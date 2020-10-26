$password = ConvertTo-SecureString “Password@123” -AsPlainText -Force
#$username = $env:UserName
$username = "ecsadmin"
$Cred = New-Object System.Management.Automation.PSCredential ($username, $password)

Rename-Computer -ComputerName (Get-Content "..\psinput\machines.txt") -NewName ECSDWTST05 -LocalCredential $Cred -Force -Verbose -Restart