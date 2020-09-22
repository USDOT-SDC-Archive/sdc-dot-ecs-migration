$password = ConvertTo-SecureString “Password@123” -AsPlainText -Force
#$username = $env:UserName
$username = "ecsadmin"
$Cred = New-Object System.Management.Automation.PSCredential ($username, $password)

Remove-Computer -ComputerName (Get-Content "..\psinput\machines.txt") -UnjoinDomaincredential $Cred -WorkgroupName "WORKGROUP" -Force -Verbose -Restart