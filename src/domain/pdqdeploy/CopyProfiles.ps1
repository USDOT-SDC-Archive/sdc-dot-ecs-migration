$map = @{
"name_of_host" = "primary_user";
};



foreach($key in $map.keys)
{
	$user = $map[$key];
	
	cmd.exe /c "icacls c:\Users\${user} /grant sdc\${user}:(OI)(CI)F /T /C /Q"
	cmd.exe /c "xcopy c:\Users\${user} c:\Users\${user}.SDC /E /C /I /Q /Y"
	cmd.exe /c "icacls c:\Users\${user}.SDC /grant sdc\${user}:(OI)(CI)F /T /C /Q"
}


