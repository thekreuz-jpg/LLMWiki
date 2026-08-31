# Lint Checklist

## Compiled Wiki Notes

- [ ] Note uses one allowed tag: `topic`, `concept`, `entity`, `project`, or `log`
- [ ] `source_count` equals the number of entries in `sources`
- [ ] Every source link points to an existing file under `Raw/Sources/`
- [ ] `created` and `updated` are valid dates
- [ ] `status` is one of: `seed`, `growing`, `mature`, `archived`
- [ ] No unsupported claims without source links

## Raw Source Notes

- [ ] `Title` is present and non-empty
- [ ] `Reference` is present (URL, DOI, or identifier)
- [ ] `Created` is a valid date
- [ ] `Processed` is a boolean
- [ ] `tags` includes `"source"`

## Catalog Integrity

- [ ] `Wiki/catalog.jsonl` contains one JSON object per compiled Wiki note
- [ ] Each catalog entry includes `path`, `title`, `tag`, `topics`, `sources`, `updated`

## Source Manifest Integrity

- [ ] `Schema/source-manifest.jsonl` contains one JSON object per Raw source
- [ ] Each manifest entry includes `path`, `title`, `processed`, `covered_by`, `updated`
