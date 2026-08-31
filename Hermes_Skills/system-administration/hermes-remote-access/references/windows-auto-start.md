# Windows auto-start recipes — Hermes dashboard + backend (LAN)

Context: desktop-app install on Windows 10, user Kreuz, agent PC `192.168.1.69`.
Install home: `C:\Users\Kreuz\AppData\Local\hermes` (NOT `~/.hermes`).
Hermes python: `C:\Users\Kreuz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`.

## Critical: how to keep a server alive across reboots AND Hermes-session resets
- `terminal background=true` jobs are parented to the Hermes shell and are REAPED when
  the Hermes session/context resets. Never use them for a server you expect to persist.
- Use `Start-Process` (PowerShell) so the process is parented to the OS.
- Always strip the Electron-inherited env vars or the dashboard serves the broken
  `app.asar` renderer ("Desktop IPC bridge is unavailable", #52945).

## File: launch-dashboard.ps1  (detached dashboard launcher)
```powershell
Remove-Item Env:HERMES_DESKTOP        -ErrorAction SilentlyContinue
Remove-Item Env:HERMES_WEB_DIST       -ErrorAction SilentlyContinue
Remove-Item Env:HERMES_SERVE_HEADLESS -ErrorAction SilentlyContinue
& "C:\Users\Kreuz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" `
  -m hermes_cli.main dashboard --no-open --host 192.168.1.69 --port 9119 --skip-build
```
Run detached:
```powershell
Start-Process -FilePath 'powershell.exe' -ArgumentList '-NoProfile -WindowStyle Hidden -File C:\Users\Kreuz\AppData\Local\hermes\launch-dashboard.ps1' `
  -RedirectStandardOutput 'C:\Users\Kreuz\AppData\Local\hermes\logs\dashboard-standalone.log' `
  -RedirectStandardError  'C:\Users\Kreuz\AppData\Local\hermes\logs\dashboard-standalone.err'
```

## Scheduled task (AtLogOn) — already created, name `Hermes_Dashboard_LAN`
Create/refresh (admin PowerShell, will prompt UAC):
```powershell
$action   = New-ScheduledTaskAction -Execute 'C:\Users\Kreuz\AppData\Local\hermes\launch-dashboard.ps1' -WorkingDirectory 'C:\Users\Kreuz\AppData\Local\hermes'
$trigger  = New-ScheduledTaskTrigger -AtLogOn -User 'Kreuz'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal= New-ScheduledTaskPrincipal -UserId 'Kreuz' -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'Hermes_Dashboard_LAN' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
```
Test on-demand: `Start-ScheduledTask -TaskName 'Hermes_Dashboard_LAN'` then
`netstat -ano | findstr 9119` + `curl -s -o /dev/null -w "%{http_code}" http://192.168.1.69:9119`
(expect a LISTENING line and HTTP 302).

## Known gap (NOT yet closed)
The `Hermes_Dashboard_LAN` task brings the DASHBOARD back after reboot, but the BACKEND
it talks to is not auto-started, so chat fails until a backend is up. The dashboard
bundles its own backend when launched as above, so in practice the same `launch-dashboard.ps1`
provides both — but if a separate headless `hermes serve` is ever run, bind it to
loopback (127.0.0.1) and a DIFFERENT port than 9119 to avoid collision, and point the
dashboard at it. The messaging gateway is a separate `Hermes_Gateway` scheduled task;
leave it alone.

## Firewall
Rule `Hermes Dashboard (LAN 9119)` (Private profile) already exists. If re-created:
allow TCP 9119 inbound, Private profile only.
