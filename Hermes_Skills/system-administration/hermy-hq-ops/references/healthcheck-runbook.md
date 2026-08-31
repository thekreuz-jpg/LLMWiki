# Hermy HQ Health-Check Runbook (validated 2026-08-18)

Exact commands run during a live "check my hermes install" session, with the real outputs that
act as pass/fail signals. Re-run in this order; stop at the first failing component.

## 1. Hermes agent status
```
hermes status
```
Check: `Nous Portal  ✓ logged in`, model line present. Confirms desktop app + auth.

## 2. Postgres service
```
sc.exe query postgresql-x64-18
```
PASS: `STATE              : 4  RUNNING`

## 3. Scheduled tasks (logon auto-start)
```
schtasks.exe /query /tn HermesBridge /v /fo LIST
schtasks.exe /query /tn Hermes_Dashboard_LAN /v /fo LIST
```
Read `Last Result` + `Last Run Time`:
- `0`            = clean run
- `-1073741510`  = `0xC0000142` = process init failure at logon (env not set / crashed on connect)
NOTE: `Status: Ready` means an idle/At-logon task is NOT currently executing — judge health by
ports + Last Result, not "Ready".

## 4. Listening ports (bash, NOT PowerShell $_ — see Pitfalls in SKILL.md)
```
netstat -ano | grep LISTENING | grep -E ':3000|:9119|:5432'
```
PASS: `:5432` always; `:9119` when LAN dashboard up; `:3000` when Hermy HQ app up.

## 5. HTTP probes
```
curl -s -m4 -o /dev/null -w '%{http_code}\n' http://localhost:3000
curl -s -m4 -o /dev/null -w '%{http_code}\n' http://192.168.1.69:9119
```
PASS: `302` on `:9119` (redirect to login); `:3000` returns app HTML (200).

## 6. Confirm DB credential (diagnosis of 28P01)
psql is NOT on PATH — use full path:
```
"C:\Program Files\PostgreSQL\18\bin\psql.exe" "host=localhost port=5432 dbname=postgres user=postgres sslmode=disable" -c "SELECT 1;"
```
`FATAL: password authentication failed for user "postgres"` (code 28P01) means the password in
`DATABASE_URL` is wrong. A literal `***` in `hermy-hq/.env` and `hermes-bridge/run-bridge.bat` is
the usual cause. Do NOT reset the password without the user's explicit go-ahead.

## Recovery: restart LAN dashboard (detached, exactly what start-dashboard.bat does)
```
powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Users\Kreuz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe' -ArgumentList '-m','hermes_cli.main','dashboard','--no-open','--host','192.168.1.69','--port','9119','--skip-build' -WindowStyle Hidden -WorkingDirectory 'C:\Users\Kreuz\AppData\Local\hermes\hermes-agent'"
```
Foreground smoke test prints `HERMES_DASHBOARD_READY port=9119`.

## Recovery: bridge / Hermy HQ (after fixing DATABASE_URL password)
Run as the bridge task does (from `run-bridge.bat`):
```
cd /d C:\Users\Kreuz\hermy-hq\hermes-bridge
set DATABASE_URL=postgres://postgres:<REAL_PASSWORD>@localhost:5432/hermyhq?sslmode=disable
set HERMES_BOARD=default
set HERMES_BIN=hermes
set HERMES_WIKI=C:\Users\Kreuz\Documents\SyncVault
set BRIEF_HOUR=7
node bridge.mjs
```
The Hermy HQ web app reads `DATABASE_URL` from `C:\Users\Kreuz\hermy-hq\.env` (same value).
