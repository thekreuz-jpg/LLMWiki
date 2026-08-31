#!/usr/bin/env bash
# check-hermyhq.sh — one-shot status probe for the Hermes/Hermy HQ Windows stack.
# Run from MSYS/git-bash (Linux env). Prints a status line per component.
# Not a fixer — diagnosis only. Escalate to the recovery steps in references/healthcheck-runbook.md.
set -u

ok()   { printf '\033[32m[OK]\033[0m   %s\n' "$1"; }
bad()  { printf '\033[31m[DOWN]\033[0m %s\n' "$1"; }
warn() { printf '\033[33m[?]\033[0m   %s\n' "$1"; }

echo "=== Hermy HQ stack check ($(date)) ==="

# 1. Hermes agent
if hermes status >/dev/null 2>&1; then ok "hermes agent responds (hermes status)"; else bad "hermes status failed"; fi

# 2. Postgres service
if sc.exe query postgresql-x64-18 2>/dev/null | grep -q "STATE.*: 4"; then ok "postgresql-x64-18 RUNNING"; else bad "postgresql-x64-18 not running"; fi

# 3. Ports (bash netstat, never PowerShell $_)
netstat -ano 2>/dev/null | grep LISTENING >/tmp/hh_ports.txt
grep -q ':5432' /tmp/hh_ports.txt && ok "postgres listening on :5432" || bad "nothing on :5432"
grep -q ':9119' /tmp/hh_ports.txt && ok "LAN dashboard listening on :9119" || warn "LAN dashboard :9119 not listening"
grep -q ':3000' /tmp/hh_ports.txt && ok "Hermy HQ app listening on :3000" || warn "Hermy HQ app :3000 not listening"

# 4. HTTP probes
code_3000=$(curl -s -m4 -o /dev/null -w '%{http_code}' http://localhost:3000 2>/dev/null)
code_9119=$(curl -s -m4 -o /dev/null -w '%{http_code}' http://192.168.1.69:9119 2>/dev/null)
[ "$code_9119" = "302" ] || [ "$code_9119" = "200" ] && ok "LAN dashboard HTTP $code_9119" || warn "LAN dashboard HTTP ${code_9119:-no-response}"
[ "$code_3000" = "200" ] && ok "Hermy HQ HTTP $code_3000" || warn "Hermy HQ HTTP ${code_3000:-no-response}"

# 5. Bridge task last result
br=$(schtasks.exe /query /tn HermesBridge /v /fo LIST 2>/dev/null | grep -i 'Last Result' | tr -d '\r')
echo "  bridge task: $br"
