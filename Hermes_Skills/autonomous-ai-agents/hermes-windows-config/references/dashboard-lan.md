# Web Dashboard LAN Binding — verified working recipe (Windows)

Goal: expose `hermes dashboard` on the LAN so another PC on the same network can reach it.

## 1. Credentials (basic auth)

Dashboard creds live in `$HERMES_HOME/.env` → `C:\Users\Kreuz\AppData\Local\hermes\.env` (NOT `~/.hermes/.env`).

Append (generate a strong random password, don't reuse a guessable one):

```powershell
$ENV = "$env:LOCALAPPDATA\hermes\.env"
$PW  = (openssl rand -base64 18 | tr -dc 'A-Za-z0-9' | head -c 24)
$SEC = (openssl rand -base64 32)
Add-Content $ENV @"

# Dashboard basic auth (added $(Get-Date -Format yyyy-MM-dd))
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=hermes
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=$PW
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$SEC
"@
# file should already be 0600-equivalent; tighten if needed (icacls)
```

## 2. Launch bound to the LAN interface

```bash
hermes dashboard --no-open --host 192.168.1.69 --port 9119 --skip-build
```

- `--skip-build` avoids an npm build step (use when npm isn't handy, e.g. Scheduled Tasks). Pre-built dist lives under `.../app.asar.unpacked/dist`.
- The non-loopback bind forces the auth gate. Expect `GET /` → `302 /login?next=%2F`.
- Verify the socket from this machine:
  ```bash
  powershell.exe -Command "Get-NetTCPConnection -LocalPort 9119"   # expect State=Listen on 192.168.1.69
  curl -s -o /dev/null -w "%{http_code}\n" http://192.168.1.69:9119/   # expect 302
  ```

## 3. Firewall — required for other PCs to connect

Windows Defender Firewall (Private profile enabled) drops inbound 9119 from other machines. Add an allow rule. **This needs Administrator PowerShell** — Hermes' terminal is non-elevated and returns `Access is denied` (exit 5) from `New-NetFirewallRule`.

Run AS ADMIN:
```powershell
New-NetFirewallRule -DisplayName "Hermes Dashboard (LAN 9119)" `
  -Direction Inbound -Action Allow -Protocol TCP -LocalPort 9119 -Profile Private
```
Remove later:
```powershell
Remove-NetFirewallRule -DisplayName "Hermes Dashboard (LAN 9119)"
```

## 4. Connect from the other PC
Browser → `http://192.168.1.69:9119` → log in with the basic-auth creds above. Must be on the same `192.168.1.0/24` LAN.

## Pitfalls encountered (and the fix)
- **Wrong `.env` path**: appending to `~/.hermes/.env` silently produced "No such file or directory" (that dir doesn't exist here). Use `$LOCALAPPDATA\hermes\.env`.
- **`New-NetFirewallRule -Program '...app.asar.unpacked\dist\*'`** → rejected ("invalid characters"). The `-Program` field dislikes the wildcard/long path; drop `-Program` and scope by port+profile only.
- **Access denied** on firewall rule → must run PowerShell as Admin. Hermes terminal can't elevate.
- **MSYS `netstat`** didn't show the Windows listener; `Get-NetTCPConnection` is authoritative.
- **Port readback typo**: 9119, not 9199.

## Alternative: SSH tunnel (no firewall change)
If you enable OpenSSH Server on the host, keep the dashboard on loopback and tunnel:
```bash
# other PC:
ssh -L 9119:127.0.0.1:9119 user@192.168.1.69
# then open http://127.0.0.1:9119 on the other PC
```
Safer for untrusted networks since nothing is exposed.
