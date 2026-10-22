# Relief Feet — Static Website

A hand-crafted, four-page static site for **Relief Feet**, a 5.0-rated reflexology clinic in MGR Nagar, Kolathur, Chennai. Built with plain HTML, CSS and vanilla JavaScript only — no frameworks, no build step, no forms of any kind.

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Home — editorial hero, marquee tickers, animated stats, sticky "why reflexology", visit process |
| `services.html` | Treatments grid (sticker-book tiles), package philosophy, FAQ (`<details>` accordions) |
| `reviews.html` | Real Google reviews as scattered postcards with JS topic filtering + live count |
| `contact.html` | Address, embedded map, auto-highlighted today's hours row, live Chennai clock |

## Design language
- Palette sampled directly from the clinic logo: deep teal `#07271f`, jade `#159680`, saffron `#eab308`.
- Display type: Fraunces; body: Outfit (Google Fonts).
- Signature motion (CSS-first): staggered letter drop-in headlines, tilted dual marquee tickers, breathing radial washes, magnetic buttons, pointer parallax, taped postcard scatter, hard-offset sticker shadows, pulsing call pill, rotating SVG badge stamp.

## Anti-AI-slop rules followed
Deliberately avoided: centered hero trio (eyebrow + gradient headline + two CTAs), indigo/violet gradients, glassmorphism cards, aurora blobs everywhere, identical 3-card feature rows, emoji-in-gradient-box icons, looping stock video backgrounds, fake logo marquees, numbered timeline cards, oversized sparse headings, dark bg + single neon accent, mono-uppercase-wide tracking body text, beige+terracotta+serif spa cliché, green rounded-pill wellness look, serif-italic poetry, hairline grids, dense broadsheet columns, swiss red-block layouts, terminal/brutalist gimmicks. No lorem ipsum anywhere.

## SEO
- Unique `<title>` + meta description per page, canonical links, Open Graph & Twitter cards.
- Schema.org JSON-LD: `MedicalBusiness` with address, geo, 24-hour opening specs, `aggregateRating` (5.0 / 86) and `Review` entries.
- Semantic landmarks, skip link, one `h1` per page, alt text, `aria-current`, `aria-live` filter status.
- `sitemap.xml` + `robots.txt`; lazy-loaded iframe/images; `prefers-reduced-motion` respected.

## Run locally
```bash
# any static server works, e.g.
python3 -m http.server 8000
```
Then open http://localhost:8000

> Note: `canonical`/OG URLs use `https://relieffeet.in/` as a placeholder — replace with the real production domain before deploying.
