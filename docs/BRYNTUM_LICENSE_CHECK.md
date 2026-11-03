# Bryntum licence check

Checked on 2026-11-01 (UTC) for `8.0.0-beta.1` and again on 2026-11-04 (UTC) for the `8.0.0` general-availability release now pinned. This is a reading of public package metadata. It is not legal advice.

## Verdict

| Route | Can this public MIT repository depend on it? |
| --- | --- |
| `@bryntum/scheduler-community` and `@bryntum/scheduler-react-community` (Community tier, `8.0.0`) | **Allowed, as a pinned dependency.** Both packages and their five Bryntum dependencies declare MIT, and each tarball carries an MIT `LICENSE` file. MIT permits use, copying, modification and distribution, including in this MIT repository, provided the copyright and permission notice is kept (it is, inside each package). The repository still does not vendor or commit any Bryntum code; `npm ci` fetches the exact versions from the lock. |
| `@bryntum/*-trial` packages | **Not allowed.** They are commercial software that requires a paid licence. A trial is for evaluation, not for a public open-source dependency. |
| `@bryntum/*-business` / `*-enterprise` packages | **Not allowed without a licence key and written terms from Bryntum.** These tiers are commercial and run in trial mode until a licence key is registered. |
| A hackathon licence from Bryntum | **Not found.** No licence grant for participants was found. The hackathon rules, read later on 2026-11-01, ask entrants to use any Bryntum tools; the Community tier is one. |

Since 2026-11-01 the Community tier is a real, exactly pinned dependency of `frontend/package.json` and `frontend/package-lock.json`. It powers the evidence deadline board in step 03 of the seller console (`frontend/src/board/`); the optional time evidence timeline in `frontend/src/optional/` is not mounted (no console file imports it). This is allowed because of the MIT evidence below: the Community README says "The Community tier of Bryntum Scheduler is licensed under the MIT license" (source 3), the tarball holds the standard MIT `LICENSE` text with `Copyright (c) 2009-2026 Bryntum` (source 4), and every Bryntum entry in the lock declares `"license": "MIT"`. The Vite plugin (`frontend/src/optional/vitePlugin.js`) stops the build when `package.json` or the lock declares any Bryntum package that is not `-community` (trial, Business, Enterprise, the commercial `@bryntum/scheduler-react` wrapper) or not MIT, when a Bryntum version is not exact, or when an installed imported package does not declare MIT.

## Sources

One short quote per source, at most.

1. **Hackathon page:** <https://paypalaihackathon.devpost.com/>. Not reachable from the environment of this check; read later on 2026-11-01 in a separate session. It lists a "Best Use of Bryntum" prize, 3 × $1,000, and asks entrants to "use any Bryntum tools". No sponsor licence terms were found there.
2. **Bryntum Scheduler placeholder package:** <https://www.npmjs.com/package/@bryntum/scheduler> (read through `registry.npmjs.org`): "A Business or Enterprise tier package runs in trial mode until you register a license key."
3. **Community tier package README:** <https://www.npmjs.com/package/@bryntum/scheduler-community> (version `8.0.0-beta.1`, and again in the `8.0.0` tarball's `package/README.md`): "The Community tier of Bryntum Scheduler is licensed under the MIT license."
4. **Community tier tarball (beta, superseded):** <https://registry.npmjs.org/@bryntum/scheduler-community/-/scheduler-community-8.0.0-beta.1.tgz>. It holds `package/LICENSE`, which is the standard MIT text with the line `Copyright (c) 2009-2026 Bryntum`. The dependencies `@bryntum/core-community`, `@bryntum/grid-community` and `@bryntum/engine-community` (all `8.0.0-beta.1`) each declare `"license": "MIT"`.
5. **Trial package README:** <https://www.npmjs.com/package/@bryntum/scheduler-trial> (version `7.3.8`, `"license": "Commercial"`): "Bryntum Scheduler is commercial software and requires a paid license."
6. **Bryntum End User License:** <https://bryntum.com/products/license/>. *Not read.* bryntum.com did not resolve from this environment. Sources 2 and 5 link to it for the commercial tiers.
7. **General-availability tarballs, `8.0.0` (2026-11-04, optimise r24):** for each of the seven packages, `npm view <pkg>@8.0.0 license dist.tarball dist.integrity` against `registry.npmjs.org`, then `npm pack <pkg>@8.0.0` into an empty temporary directory and a read of `package/LICENSE` and `package/package.json` inside the tarball. `@bryntum/scheduler-community@8.0.0` was published at 2026-11-03T11:55:04Z; the dist-tags were `latest: 8.0.0`, `next: 8.0.0-beta.1`. Every `package.json` declares `"license": "MIT"` and a `-community` name; every `package/LICENSE` is the same 21-line standard MIT text (sha256 `4a5d1d9f3eca911eab453d8de37f90d8b34167573940ef45c0fef6db6bf18108`), now with the line `Copyright (c) 2009-2026 Bryntum AB`. The sha512 of each packed tarball equals the registry `dist.integrity` below and the integrity `npm install` wrote to the lock. The README's "Features per tier" table marks `EventDrag`, `EventResize`, `EventTooltip` and `EventDragCreate` as Community; `TimeRanges`, `ResourceTimeRanges` and `NonWorkingTime` are Business or Enterprise only, and no `TimeRanges.js` ships in the Community `lib/Scheduler/feature/` folder. The Community core mentions a licence key only in documentation for the Business and Enterprise tiers; no trial mode or watermark code was found in the Community `lib/` folders, and none appeared in the rendered board.

## Package identity checked

Pinned since 2026-11-04 (optimise r24), `8.0.0`, read from the registry and the packed tarballs:

| Package | Version | Licence | npm integrity |
| --- | --- | --- | --- |
| `@bryntum/scheduler-community` | 8.0.0 | MIT | `sha512-NcvzQqTy8zeOXrGT/mkHvdJyMeULYMZq/qDnBLSzX301k4uRmrrPQKD6oc7+jSs7xgukPLYbW4+xD9lro4rREw==` |
| `@bryntum/core-community` | 8.0.0 | MIT | `sha512-46olNPneMyxy6Y5kAEv+AqQOCOjlsHaSrE+GZ+MvcK2Jq7oO4cV2ueSrMwAcSL1Qgd1zv0jiW0znDPiUYlO7qQ==` |
| `@bryntum/grid-community` | 8.0.0 | MIT | `sha512-mP05jXRp2w0uIEX3lB1oIUd4KzTYpUts0AeGQxlfEuZ/amdKi4kJnPdTxzhMqdFv7kTrz+g+/Nun/qpiYres0A==` |
| `@bryntum/engine-community` | 8.0.0 | MIT | `sha512-jBXH8qJtBwXYI48XttHLiHqFzU3Rmq/rqc7oiE3FIibGcSQDx/LmpauJDJgWExcBQwzutQwHACLEalA2E19lXQ==` |
| `@bryntum/scheduler-react-community` | 8.0.0 | MIT | `sha512-L2DnKJfCTjSjugdT0+RIKFXJVuOcTW7MzTakLIXwXGkBcf4XkqtHxm7SBOfn79ycKalnuxi0Y4bwubIMmrJvYw==` |
| `@bryntum/core-react-community` | 8.0.0 | MIT | `sha512-L/2iQAf39h44UK0BzQ8aq2oAXjttd8EXMa0zkG4J9dZAiygLZzvkTaY5xhDonz15wx7YQIUm9/Yv7wkAbhdZog==` |
| `@bryntum/grid-react-community` | 8.0.0 | MIT | `sha512-9i3JKafRlMjwVjcoZf6WM5AMW9JafpsQ9CmLmIyzA/ENmUFGFhlUhFYJm44VlcYVKDKuf8uAbLGR57DuwYXhEw==` |

The dependency graph is unchanged from the beta: `scheduler-community` needs `core`, `grid` and `engine`; `scheduler-react-community` needs `scheduler`, `core-react` and `grid-react`; all at exactly `8.0.0`. `tests/frontend_bryntum_board_contract.mjs` holds this integrity table and fails if the lock drifts from it.

Previously pinned, `8.0.0-beta.1` (checked 2026-11-01):


| Package | Version | Licence | npm integrity |
| --- | --- | --- | --- |
| `@bryntum/scheduler-community` | 8.0.0-beta.1 | MIT | `sha512-gAmrN/gnEZrECpnnaMDQrOLB1BloMP4q1bfrNlbUBMBdCxtuuuh38u1tn6Ms3D0YaefxtXw36sujnWCAdgVMAA==` |
| `@bryntum/core-community` | 8.0.0-beta.1 | MIT | `sha512-KA10nIhE1RbH555/oNWLGRim2SWbNm0SQn6T3zECTEyEk5EhTjHhwjglWzL85eBma9wBz4g5UxaYE8uQyA24ug==` |
| `@bryntum/grid-community` | 8.0.0-beta.1 | MIT | `sha512-HEh5Mzd2aBtWD7mSJYumMdIHLg8Dq/3mP9D7hEI+lNIqp4t5PUiWVlfk+o66+ns0bRv3Z60VlfDtkHN+dD39Tw==` |
| `@bryntum/engine-community` | 8.0.0-beta.1 | MIT | `sha512-l6C0Y9fwYw050zysAXDAODTHUlqZUoxcr/SZXxSKxZk6wwVuDBfEgpbvy7rIXw+gBta/GQXT9aX1O28RjkuOQA==` |
| `@bryntum/scheduler-react-community` | 8.0.0-beta.1 | MIT | `sha512-o1EMzSjsJl6U11GD3JhBd2NCN8omLd0xOFMBYeF7jJAduLwYo0xDJPVsNieSb7DDEz6VDNLh+HcloxLAIBkbEQ==` |
| `@bryntum/core-react-community` | 8.0.0-beta.1 | MIT | `sha512-pNF+Zyxtzk3dTBLn75rXpU+Fd5gbg2MngTgASpJ1r3W84LRsG0zTdx7BR0G2O94jeFNxPfqltnQ7ZaXZrT4buA==` |
| `@bryntum/grid-react-community` | 8.0.0-beta.1 | MIT | `sha512-bSITKL9y6lYWFwfDRZsDnlWu876LjTRNmAN+zgaKkF21BMqKpp4YLQBDa80tMXVx5hKprY5lCzqQ6Hn16/191A==` |

`8.0.0-beta.1` was published on 2026-10-30. The general-availability release `8.0.0` was published on 2026-11-03 under `"license": "MIT"` and is pinned since 2026-11-04 after the tarball check in source 7 (the upgrade changed only the seven Bryntum entries of the lock). Pin the exact version and re-check the licence before any later upgrade. The `8.0.0` third-party notices (`licenses.md`) list Font Awesome 6 Free, the Poppins, Roboto Flex and Montserrat fonts (SIL OFL 1.1, used by Bryntum's demos, not by the themes), a Tree Walker polyfill and a Map/Set polyfill (Salesforce bundle only), chronograph (MIT), Monaco editor (MIT), AG Charts Community (MIT) and AG Charts Enterprise as optional and commercial, used only with Bryntum's separate Chart package, which this repository does not install. The board and the timeline load Font Awesome from the local package so that Bryntum never falls back to a CDN. The React wrapper is the MIT Community wrapper `@bryntum/scheduler-react-community` (checked on the npm registry on 2026-11-01, when `latest` was `8.0.0-beta.1`, `"license": "MIT"`); the similarly named `@bryntum/scheduler-react` (`7.3.8`) declares `Commercial` and is refused by the guard.

## How the repository stays open source

- `frontend/package.json` pins `@bryntum/core-community`, `@bryntum/scheduler-community` and `@bryntum/scheduler-react-community` at exactly `8.0.0`; the lock holds those and their four Bryntum dependencies, all MIT, with the `8.0.0` integrities above. `tests/frontend_bryntum_board_contract.mjs` and `tests/frontend_optional_timeline.mjs` fail if a non-Community, non-MIT or unpinned Bryntum package appears.
- No Bryntum source, trial bundle or build output is committed (`node_modules/` and `dist/` are ignored). The hosted image installs the lock with `npm ci`.
- No file in `frontend/src` imports `@bryntum/*` directly. Only the virtual module written by `frontend/src/optional/vitePlugin.js` can reach the packages, and only when they are installed and declare MIT.
- The Bryntum code and CSS sit in the lazily loaded board chunk; the console's first load does not include them. If the packages are missing, the board shows its plain list only.

To check locally:

```sh
cd frontend
npm ci
npm run build   # logs "Bryntum Scheduler: on (@bryntum/scheduler-community@8.0.0, MIT Community tier)"
```

## What to ask Bryntum for any route beyond the Community tier

The Community tier needs no request. To use Business or Enterprise features, a trial build, or a hackathon licence, the project owner would need written answers from Bryntum (for example at <https://bryntum.com/contact/>) to these questions:

1. May a public, MIT-licensed hackathon repository reference `@bryntum/scheduler-business` or `-enterprise` as an optional, locally installed package, with no Bryntum code in the repository?
2. Will Bryntum issue a licence key for PayPal AI Hackathon participants, and does it cover a publicly reachable demo and the recorded video during judging?
3. May a trial-mode build appear in a public demo or in the submission video?

Until those answers exist in writing, only the Community tier is used.

## Features the board uses (optimise r24)

The evidence deadline board uses only Community-tier features: `EventDrag` and `EventResize` with validators (for the seller's "Collect evidence" plan bars), `EventTooltip`, and the built-in event keyboard navigation. Editors, menus, drag-create and the Delete key stay off. The "now" line and the per-case due lines are not the `TimeRanges` feature, which is Business tier: the board draws them with the Community `getCoordinateFromDate` and `getRowFor` methods. The plan is held in the page and the tab's `sessionStorage` only.
