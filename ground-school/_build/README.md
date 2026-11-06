# Student Pilot Permit study site — how it's built

Temporary, phone-first copy of the SAFA Ground School **Student Pilot Permit** section (ROC-A + PSTAR) for Grade 10s,
published at `/safa-ame/ground-school/` while the full Google Sites ground school is finished.

- **Pages** are the same HTML files the Apps Script web app serves (Drive folder `ONLINE GROUND SCHOOL`), unchanged except:
  `spp-local.js` is loaded first and `spp-local.css` last, plus a few wording swaps (progress is on this device, not shared with a teacher).
- **spp-local.js** stands in for Google: `google.script.run.track/getSppData` save to and read from `localStorage` (`safa-spp-rows-v1`),
  `SITE_LINKS` points every page id at this folder, `SAFA_CONFIG` = ROC-A 70% / 25 Qs, PSTAR 90% / 50 Qs, and it adds the top bar + menu.
- **Part overview pages** (`*-title.html`) are rebuilt by `overview.py` from the hub pages' `COURSE` data (the Drive originals couldn't be pulled).
- Only Student Pilot Permit pages are included. Nothing links to the full ground school site. C172 and Policy show as "coming soon".

## Rebuild after a page changes in Drive
1. Put the page files in `src/` (download from the Drive folder), `site/` = files in `_build/site/`, `tools/` = the .py files here.
2. `python3 tools/build.py` → `dist/`. Then `python3 tools/check.py` (phone + desktop: errors, sideways scroll) and `python3 tools/links.py` (no links outside the site).
3. Copy `dist/*` over `ground-school/` and push.

## Retire it
When the full site launches, delete `ground-school/` and give students the main site link. Their progress on this copy does not carry over.
