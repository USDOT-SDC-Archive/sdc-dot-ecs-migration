# get IAM role for this EC2

$resp = Invoke-WebRequest -Uri http://169.254.169.254/latest/meta-data/iam/security-credentials/
$role = $resp.ParsedHtml.body.innerText

# get template

$str = Get-Content -Path c:\software\cyberduck-template.cyberduckprofile

$str = $str.Replace('s3access', $role)

Add-Content -Path 'C:\Program Files\Cyberduck\profiles\S3 (Credentials from EC2 Instance Metadata).cyberduckprofile' -Value ($str)
