# Live Free-Model List — endpoint & snapshot

## Endpoint
`GET https://portal.nousresearch.com/api/nous/recommended-models`

- Public, no auth. Returns JSON `{"freeRecommendedModels": [...], "paidRecommendedModels": [...]}`.
- Each free entry: `{ "modelName": "vendor/model:free", "displayName": "...", "source": "local"|"openrouter", "tokenPrice": "$0.00/1M", "contextLength": <int|null>, "isVisionModel": <bool>, "isCompactionModel": <bool> }`.
- Also cached on disk at `$HERMES_HOME/cache/nous_recommended_cache.json` (last-known-good; used when live fetch fails).
- Hermes reads this in `hermes_cli/models.py::union_with_portal_free_recommendations` (~line 699) and filters free-tier users via `partition_nous_models_by_tier` (~line 671).

## How to fetch
```bash
python - <<'PY'
import urllib.request, json
d = json.loads(urllib.request.urlopen(
    urllib.request.Request("https://portal.nousresearch.com/api/nous/recommended-models",
    headers={"Accept":"application/json"}), timeout=8).read().decode())
print("\n".join(m["modelName"] for m in d.get("freeRecommendedModels", [])))
PY
```

## Snapshot — fetched 2026-08-11
Live `freeRecommendedModels` (authoritative; the repo curated list was stale):
1. `upstage/solar-pro4:free`        — general/large, best free reasoning pick
2. `tencent/hy3:free`               — small/fast (user's prior default)
3. `poolside/laguna-s-2.1:free`     — coding, 262144 ctx
4. `stepfun/step-3.7-flash:free`    — vision + compaction
5. `poolside/laguna-xs-2.1:free`    — coding, 262144 ctx

## Known stale curated entry (do NOT set)
- `inclusionai/ring-2.6-1t:free` — listed in `hermes_cli/models.py` free tier but
  NOT in the live list; backend returns HTTP 404 "requires available credits".

## Re-verify before asserting "strongest"
The roster drifts. Re-fetch the endpoint; do not rank by the curated list's
parameter counts, which are out of date.
