# Hermes Remote Access — exact commands

Verified on Windows 10 host (Hermes terminal = MSYS bash, POSIX syntax).

## 1. Local launch (loopback, safe default)
```
hermes dashboard --no-open
# binds 127.0.0.1:9119
```

## 2. SSH tunnel from another machine
On host: `hermes dashboard --no-open`
On client:
```
ssh -L 9119:127.0.0.1:9119 <user>@<host-ip>
# browser on client: http://127.0.0.1:9119
```
Requires OpenSSH Server enabled on host.

## 3. Bind to LAN with basic_auth
Write to ~/.hermes/.env (chmod 600):
```
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=<strong password>
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)
```
Launch:
```
hermes dashboard --no-open --host 0.0.0.0 --port 9119
```
Client hits `http://<host-ip>:9119`.

## 4. Status / stop
```
hermes dashboard --status
hermes dashboard --stop
```

## 5. Probe from client (verify before reporting success)
```
curl -s -o /dev/null -w "%{http_code}\n" http://<host-ip>:9119
```

## Important
`--insecure` is DEPRECATED/NO-OP since June 2026 hardening. Non-loopback bind always
requires an auth provider. Do not rely on it to expose the dashboard.
