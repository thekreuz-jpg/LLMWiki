# Common HyperFrames Composition Pitfalls

Based on experience building the "HyperFrames Explainer" video (30s, 5-scene composition).

## Contrast Issues

HyperFrames `check` enforces WCAG contrast ratios. Common failures:

- **Bright gradient backgrounds with white text**: Linear gradients like `#00d4ff → #0088cc` with white text fail WCAG AA (need 4.5:1 for normal text). Fix: use dark text (`color: #000`) on bright backgrounds.
- **Semi-transparent white text on dark backgrounds**: `rgba(255,255,255,0.4)` on `#0e0e10` fails. Increase to at least `rgba(255,255,255,0.75)` or use a lighter text color.
- **Small text is stricter**: Tool labels, filenames, and metadata at 10-14px need higher contrast ratios than display text.

## Timeline Density Warning

`lint` warns when a track has 5+ timed elements. For linear explainer videos with sequential scenes, this is unavoidable and acceptable. The warning is advisory — renders still succeed.

## Determinism Rules

Key rules from `hyperframes-core` that trip up new authors:

- No `Date.now()`, `performance.now()`, or unseeded `Math.random()`
- No `repeat: -1` — compute a finite repeat count
- No CSS initial `transform` paired with GSAP tween on same property — use `gsap.fromTo()`
- Full-screen backgrounds go on a child (`position:absolute; inset:0`), not the composition root
- No `<br>` in body text — use `max-width` for wrapping

## Render Performance

- Static frame dedup saves ~25% render time for compositions with hold frames
- Parallel capture (3 workers) is automatic for 700+ frames
- A 30s 30fps composition = 900 frames, renders in ~28s on GTX 1080 Ti

## Project Structure

```
<project>/
  index.html          # Main composition
  hyperframes.json    # Project config
  package.json        # Pins hyperframes version
  renders/            # Output MPIs
```

## Auth and Media

- `hyperframes auth status` reports TTS/BGM provider status
- `hyperframes doctor` verifies system requirements (Node 22+, FFmpeg)
- Media sourcing goes through `/media-use` skill, not ad-hoc URLs
