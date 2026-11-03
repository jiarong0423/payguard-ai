# Third-Party Dependency Notices

This inventory covers the exact dependency identities locked for the PayGuard public source candidate. It is an inventory and review record, not a replacement for upstream license texts. The release owner must bind the final dependency review to the candidate package digest and detached manifest SHA-256 before publication.

## Lock identities

| Ecosystem | Lock SHA-256 | Entries | Review basis |
| --- | --- | ---: | --- |
| Root Python | `bd163e5de790527ec4b5486ec884463c40fd8331a00e122d27f65de0938a270a` | 17 | Exact local lock; installed-wheel license metadata and declared license-file hashes reviewed; final candidate digest binding remains required |
| Gemini Python | `36554331392d6102519a4ead5778704c4ff89e79da6bb9d6648b656f130724bb` | 25 | Exact hash-locked profile; installed-wheel license metadata and declared license-file hashes reviewed; final candidate digest binding remains required |
| Frontend npm | `0f98893564efb5556cc0a92710feedcb9da085108f9668fee93f29940b87f09d` | 107 | License expressions copied from the exact npm lock metadata |

## Root Python inventory

Review status for every identity in this section: `LOCKED_IDENTITY_RECORDED_INSTALLED_LICENSE_METADATA_REVIEWED`.

`annotated-doc==0.0.5`, `annotated-types==0.8.0`, `anyio==4.15.1`, `certifi==2026.7.22`, `click==8.5.0`, `fastapi==0.142.2`, `h11==0.16.0`, `httpcore==1.0.9`, `httpx==0.28.1`, `idna==3.20`, `opentelemetry-api==1.45.0`, `pydantic==2.13.5`, `pydantic-core==2.46.5`, `starlette==1.7.0`, `typing-extensions==4.16.0`, `typing-inspection==0.4.4`, `uvicorn==0.54.0`.

## Gemini Python inventory

Review status for every identity in this section: `HASH_LOCKED_IDENTITY_RECORDED_INSTALLED_LICENSE_METADATA_REVIEWED`.

`annotated-types==0.8.0`, `anyio==4.15.1`, `certifi==2026.7.22`, `cffi==2.1.1`, `charset-normalizer==3.5.2`, `cryptography==50.0.2`, `distro==1.9.0`, `google-auth==2.60.0`, `google-genai==2.28.0`, `h11==0.16.0`, `httpcore==1.0.9`, `httpx==0.28.1`, `idna==3.20`, `pyasn1==0.6.4`, `pyasn1-modules==0.4.2`, `pycparser==3.0`, `pydantic==2.13.5`, `pydantic-core==2.46.5`, `requests==2.34.2`, `sniffio==1.3.1`, `tenacity==9.1.4`, `typing-extensions==4.16.0`, `typing-inspection==0.4.4`, `urllib3==2.8.0`, `websockets==16.1.1`.

## Metadata review boundary

The Python review matches locally installed distribution versions to the exact locks above and records their declared license metadata and hashes of declared local license files. It does not establish legal redistribution clearance or replace upstream license texts. The installed `httpx` wheels declare `BSD-3-Clause` in the License field but no License-File entry; no license-file presence is inferred for that package.

## Excluded optional profile

The optional PayPal Agent Toolkit dependency profile is not distributed in this public candidate and is not part of its installation instructions or lock inventory. PayPal integration uses the official Sandbox REST API through the reviewed gateway. Exclusion does not remediate the private profile's package versions or establish current vulnerability clearance for the remaining locks.

## Frontend npm inventory by lock-declared license

### MIT

`@bryntum/core-community@8.0.0`, `@bryntum/core-react-community@8.0.0`, `@bryntum/engine-community@8.0.0`, `@bryntum/grid-community@8.0.0`, `@bryntum/grid-react-community@8.0.0`, `@bryntum/scheduler-community@8.0.0`, `@bryntum/scheduler-react-community@8.0.0`, `@jridgewell/gen-mapping@0.3.13`, `@jridgewell/remapping@2.3.5`, `@jridgewell/resolve-uri@3.1.2`, `@jridgewell/sourcemap-codec@1.6.0`, `@jridgewell/trace-mapping@0.3.31`, `@oxc-project/types@0.152.0`, `@rolldown/binding-android-arm-eabi@1.2.12`, `@rolldown/binding-android-arm64@1.2.12`, `@rolldown/binding-darwin-arm64@1.2.12`, `@rolldown/binding-darwin-x64@1.2.12`, `@rolldown/binding-freebsd-x64@1.2.12`, `@rolldown/binding-linux-arm-gnueabihf@1.2.12`, `@rolldown/binding-linux-arm64-gnu@1.2.12`, `@rolldown/binding-linux-arm64-musl@1.2.12`, `@rolldown/binding-linux-ppc64-gnu@1.2.12`, `@rolldown/binding-linux-s390x-gnu@1.2.12`, `@rolldown/binding-linux-x64-gnu@1.2.12`, `@rolldown/binding-linux-x64-musl@1.2.12`, `@rolldown/binding-openharmony-arm64@1.2.12`, `@rolldown/binding-win32-arm64-msvc@1.2.12`, `@rolldown/binding-win32-x64-msvc@1.2.12`, `@rolldown/pluginutils@1.0.1`, `@tailwindcss/node@4.3.3`, `@tailwindcss/oxide@4.3.3`, `@tailwindcss/oxide-android-arm64@4.3.3`, `@tailwindcss/oxide-darwin-arm64@4.3.3`, `@tailwindcss/oxide-darwin-x64@4.3.3`, `@tailwindcss/oxide-freebsd-x64@4.3.3`, `@tailwindcss/oxide-linux-arm-gnueabihf@4.3.3`, `@tailwindcss/oxide-linux-arm64-gnu@4.3.3`, `@tailwindcss/oxide-linux-arm64-musl@4.3.3`, `@tailwindcss/oxide-linux-x64-gnu@4.3.3`, `@tailwindcss/oxide-linux-x64-musl@4.3.3`, `@tailwindcss/oxide-wasm32-wasi@4.3.3`, `@tailwindcss/oxide-win32-arm64-msvc@4.3.3`, `@tailwindcss/oxide-win32-x64-msvc@4.3.3`, `@tailwindcss/vite@4.3.3`, `@vitejs/plugin-react@6.1.1`, `ag-charts-community@14.2.0`, `ag-charts-core@14.2.0`, `ag-charts-locale@14.2.0`, `ag-charts-types@14.2.0`, `ag-grid-community@36.2.0`, `ag-grid-react@36.2.0`, `ag-stack@36.2.0`, `enhanced-resolve@5.26.0`, `fdir@6.5.0`, `fsevents@2.3.3`, `jiti@2.7.0`, `js-tokens@4.0.0`, `loose-envify@1.4.0`, `magic-string@0.30.21`, `nanoid@3.3.19`, `object-assign@4.1.1`, `picomatch@4.0.7`, `postcss@8.5.28`, `prop-types@15.8.1`, `react@19.3.0`, `react-dom@19.3.0`, `react-is@16.13.1`, `rolldown@1.2.12`, `scheduler@0.28.0`, `tailwindcss@4.3.3`, `tapable@2.3.3`, `tinyglobby@0.2.17`, `vite@8.3.2`.

The seven `@bryntum/*-community` packages are the Bryntum Scheduler Community tier and its React wrapper, used by the evidence deadline board in step 03. Each declares `"license": "MIT"` in the lock and ships an MIT `LICENSE` file (`Copyright (c) 2009-2026 Bryntum AB`). No trial, Business or Enterprise Bryntum package is used; `frontend/src/optional/vitePlugin.js` stops the build if one is declared. See `docs/BRYNTUM_LICENSE_CHECK.md`.

### MPL-2.0

`lightningcss@1.32.0`, `lightningcss-android-arm64@1.32.0`, `lightningcss-darwin-arm64@1.32.0`, `lightningcss-darwin-x64@1.32.0`, `lightningcss-freebsd-x64@1.32.0`, `lightningcss-linux-arm-gnueabihf@1.32.0`, `lightningcss-linux-arm64-gnu@1.32.0`, `lightningcss-linux-arm64-musl@1.32.0`, `lightningcss-linux-x64-gnu@1.32.0`, `lightningcss-linux-x64-musl@1.32.0`, `lightningcss-win32-arm64-msvc@1.32.0`, `lightningcss-win32-x64-msvc@1.32.0`, `vite/node_modules/lightningcss@1.33.0`, `vite/node_modules/lightningcss-android-arm64@1.33.0`, `vite/node_modules/lightningcss-darwin-arm64@1.33.0`, `vite/node_modules/lightningcss-darwin-x64@1.33.0`, `vite/node_modules/lightningcss-freebsd-x64@1.33.0`, `vite/node_modules/lightningcss-linux-arm-gnueabihf@1.33.0`, `vite/node_modules/lightningcss-linux-arm64-gnu@1.33.0`, `vite/node_modules/lightningcss-linux-arm64-musl@1.33.0`, `vite/node_modules/lightningcss-linux-x64-gnu@1.33.0`, `vite/node_modules/lightningcss-linux-x64-musl@1.33.0`, `vite/node_modules/lightningcss-win32-arm64-msvc@1.33.0`, `vite/node_modules/lightningcss-win32-x64-msvc@1.33.0`.

### Other lock-declared licenses

- OFL-1.1: `@fontsource-variable/inter@5.3.0` (the Inter variable font, self-hosted: the woff2 files are bundled into `dist` and served from the same origin; no font CDN).
- Apache-2.0: `detect-libc@2.1.2`.
- ISC: `graceful-fs@4.2.11`, `picocolors@1.1.1`.
- BSD-3-Clause: `source-map-js@1.2.2`.
- 0BSD: `tslib@2.9.1`.

### Commercial (AG Studio, loaded only by /dashboard.html)

`ag-charts-enterprise@14.2.0`, `ag-grid-enterprise@36.2.0`, `ag-studio@3.0.0`, `ag-studio-react@3.0.0`.

These four packages are proprietary software of AG Grid Ltd under its commercial licence (lock-declared license `Commercial`). The repository does not vendor them and holds no licence key; `npm ci` fetches them from the npm registry. Without a licence key AG Studio runs in trial mode: served locally on `127.0.0.1` no watermark was seen; on a public host AG's documentation says a trial licence key is needed to remove the watermark and console warnings, and the hosted demo currently has no key. Only the separate dashboard entry imports them; the seller console and the evidence page use the MIT Community packages above. See `docs/AG_STUDIO_NOTES.md`.

## Project and provider names

PayPal, Gemini, React, AG Grid, and all other names remain the property of their respective owners. Their presence identifies interoperability or a locked dependency and does not imply endorsement. The candidate's own source license is in `LICENSE`.
