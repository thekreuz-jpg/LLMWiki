---
name: stealth-web-scraping
description: Bypass Cloudflare and DataDome anti-bot protections.
---
# Trigger conditions
Use when standard `web_extract`, `requests`, or `urllib` fail with 403 Forbidden, 429 Too Many Requests, or CAPTCHA challenges (e.g., Cloudflare, DataDome) on heavily protected sites.

# Instructions
Standard automated tools are aggressively blocked via TLS/JA3 fingerprinting and headless browser detection.

## 1. Python Approach (`curl_cffi`)
Do not use standard `requests` or `urllib`. Use `curl_cffi` to spoof real browser fingerprints:
```python
from curl_cffi import requests
# Spoof a modern browser to bypass TLS fingerprinting
response = requests.get("https://example.com/api/data", impersonate="chrome110")
```

## 2. Playwright Approach
Standard Playwright gets flagged immediately by advanced WAFs. You must use the `playwright-stealth` package to evade headless detection.

## 3. Workflow Strategy
- **Target APIs over HTML:** Before attempting to scrape and parse complex DOMs (which requires full browser rendering), inspect the network traffic to find the underlying JSON API endpoints feeding the data (e.g., search or pagination endpoints).
- **Bypass on the API:** Hit these JSON endpoints using `curl_cffi`. This avoids the need for heavy DOM parsing and is vastly more stable for extracting large catalogs or lists.
- **Example Use Case:** Extracting a full inventory from sites like Total Wine that paginate over thousands of items via Javascript/JSON.
