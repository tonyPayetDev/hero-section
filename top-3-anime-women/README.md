# Top 3 — Anime women (parody landing page)

A one-page, standalone static site: a tongue-in-cheek "top 3" ranking of anime
women, with three portraits on top and three ranked cards below.

## Files

| File | Purpose |
|---|---|
| `index.html` | Page content (French copy) |
| `style.css` | Dark manga styling, speed lines, podium, cards |
| `script.js` | Scroll reveal + animated joke stats |
| `images/*.svg` | Original stylized placeholder portraits |

## Swapping the portraits

Drop your own visuals into `images/` keeping the same file names
(`01-androide.svg`, `02-gardienne.svg`, `03-genie.svg`), or update the three
`<img src>` in `index.html`. Portraits render in a 4:5 frame.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy

`/deploy-to-coolify top-3-anime-women` — a minimal nginx `Dockerfile` is already
included.
