# set-autologon.ps1 — enable Windows auto-login for the current user.
# Self-elevates to admin. Captures the password via a LOCAL secure prompt
# (NEVER sent to any chat/terminal log). After running, every reboot logs
# the user in automatically, which fires the Hermes_Dashboard_LAN AtLogOn
# task → dashboard up on 192.168.1.69:9119 with no manual step.
#
# USAGE (on the agent PC): right-click → "Run with PowerShell", or from an
# elevated PowerShell:  & "C:\Users\Kreuz\AppData\Local\hermes\set-autologon.ps1"
# Then type the Windows password at the local prompt. Reboot to test.
#
# UNDO: `control userpasswords2` → check "Users must enter a password",
# or set AutoAdminLogon=0 in HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon.

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

$user   = $env:USERNAME
$domain = $env:COMPUTERNAME
$pass   = Read-Host -Prompt "Enter Windows password for $user" -AsSecureString
$BSTR   = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)
$plain  = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$key = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
Set-ItemProperty -Path $key -Name "AutoAdminLogon"   -Value "1"     -Type String -Force
Set-ItemProperty -Path $key -Name "DefaultUserName"  -Value $user   -Type String -Force
Set-ItemProperty -Path $key -Name "DefaultDomainName"-Value $domain -Type String -Force
Set-ItemProperty -Path $key -Name "DefaultPassword"  -Value $plain  -Type String -Force
Remove-ItemProperty -Path $key -Name "AutoLogonCount" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Auto-login ENABLED for $user on $domain." -ForegroundColor Green
Write-Host "On next reboot Windows logs in automatically; Hermes_Dashboard_LAN (AtLogOn) starts the dashboard." -ForegroundColor Cyan
Read-Host "Press Enter to exit"
