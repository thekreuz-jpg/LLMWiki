# Windows Python version-gate debugging

Reproduction: a Hermes skill or script hard-fails with a Python version error even after installing a newer interpreter.

## Symptoms
- `last30days v3 requires Python 3.12+`
- `Detected Python 3.11.15` or older
- `where python` shows `C:\Users\<user>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe` first
- `py -0` shows the desired version is installed but not default

## Root cause
`terminal.backend: local` still inherits the Hermes-installed venv Python before system Pythons on PATH. Fresh `terminal()` shells do not automatically source `~/.config/last30days/.env` or other skill-specific env files.

## Fix
Use the explicit interpreter path:

```
C:\Users\Kreuz\AppData\Local\Programs\Python\Python312\python.exe
```

Invoke all skill scripts with this path until PATH order is changed globally.

## Verify
```powershell
where python
py -0
& 'C:\Users\Kreuz\AppData\Local\Programs\Python\Python312\python.exe' --version
```
