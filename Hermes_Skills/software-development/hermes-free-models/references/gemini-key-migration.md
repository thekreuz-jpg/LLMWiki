# Google Gemini API Key Migration: Standard → Auth

## The pattern
Google is phasing out **Standard** API keys in favor of **Authorization (Auth) keys**
for the Gemini API. Auth keys are bound to a Google Cloud service account and
created automatically for all new keys in Google AI Studio.

## Timeline
- **June 19, 2026** — Gemini API began rejecting requests from unrestricted
  Standard keys.
- **September 2026** — Gemini API will reject ALL Standard keys. Hard cutoff.

## Symptoms of a rejected Standard key
- HTTP 401 `UNAUTHENTICATED` with message: *"Google Gemini rejected this API
  key's type — you do NOT need OAuth. Google began rejecting legacy 'Standard'
  Google Cloud keys for the Gemini API on June 19, 2026..."*
- The same key works for other Google Cloud APIs but fails for Gemini.
- "Out of credits" is a red herring — check the HTTP status code. 401 = key type,
  404 = model deprecated, 429/credit-exhausted = actual quota.

## How to check your key type
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Look at the **Key Type** column.
   - `Standard` → will stop working in September 2026 (or already failing if unrestricted).
   - `Authorization` → current, works.

## Fix
1. In AI Studio, click **Create API key** — new keys are automatically Auth keys.
2. Copy the new key.
3. Update `~/.hermes/.env`:
   ```
   GEMINI_API_KEY=<new_key>
   # or GOOGLE_API_KEY=<new_key>  (takes precedence if both set)
   ```
4. **Restart** the Hermes desktop app (quit fully, reopen) so `.env` is reloaded.
5. Switch model → pick a current model (e.g. `gemini-3.6-flash`). Avoid deprecated
   slugs like `gemini-2.5-flash` (returns 404 "no longer available to new users").

## Also note: model deprecation
- `gemini-2.5-flash` is deprecated → use `gemini-3.6-flash`.
- Always verify the model slug exists before switching; the desktop picker may
  list models that have been retired server-side.

## Distinguishing error types
| Error | Meaning | Action |
|-------|---------|--------|
| HTTP 401 + "rejected this API key's type" | Standard key deprecated | Create Auth key |
| HTTP 404 + "no longer available" | Model deprecated | Pick newer model slug |
| HTTP 429 / "out of credits" | Quota exhausted | Wait for reset or add billing |
| HTTP 403 | Key invalid/regenerate | Create new key |
