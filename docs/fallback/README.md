# Static fallback for the hosted demo
1. `index.html` is one self-contained page (no scripts, no external requests); its pictures are in `img/`, built from `docs/submission/` stills (no new recordings).
2. Serve it with GitHub Pages: the owner enables Settings → Pages → Deploy from a branch → `main` → folder `/docs`; the URL then is `https://jiarong0423.github.io/payguard-ai/fallback/` (repository name unchanged; Pages on a private repository needs a paid plan, so check the repository is public first).
3. Until Pages is on, the same page can be read at `docs/fallback/index.html` in the repository, but GitHub shows its source, not the rendered page.
4. Devpost first screen: add the Pages URL as a line "If the live demo is asleep (about a minute), open the static fallback: <URL>" next to the live start link and the video; also add it to the README's first-screen link row.
5. Do not edit the page's counts without checking them against `README.md` and `docs/evidence/READBACK_20261109.md`.
