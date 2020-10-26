rem ==========================
rem set local administrator password not to expire
powershell Set-LocalUser -Name "Administrator" -PasswordNeverExpires $True

rem re-init EC2 workstation functionality in the new environment
powershell C:\ProgramData\Amazon\EC2-Windows\Launch\Scripts\InitializeInstance.ps1

