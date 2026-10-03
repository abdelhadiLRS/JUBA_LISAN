# Verified Nunito + Cairo local installation

The repository currently contains a CSS file using OS-installed Nunito. The new installer changes it to bundled WOFF2 only **after** validating the supplied combined package. Running the installer locally is required; committing the installer alone does not install the binaries.

## Install from the project root

Download `JUBA-Nunito-Cairo-local-fonts.zip` from the conversation. Use the generated combined package, not the original TTF archives.

```bash
python scripts/install_local_fonts.py /path/to/JUBA-Nunito-Cairo-local-fonts.zip
python scripts/install_local_fonts.py --check
```

Python 3.10+ is enough. No internet, npm package or font converter is needed. The installer verifies three pinned SHA-256 fingerprints, WOFF2 signatures/lengths and OFL licenses before writes. It selects only the five expected files rather than extracting arbitrary archive paths. A different existing binary stops installation instead of overwriting it. Safe reruns do not duplicate the root import.

It writes three fonts and two license files to `frontend/public/fonts`, replaces `frontend/src/app/(app)/nunito-local.css`, and adds its import to `frontend/src/app/layout.tsx`. Nunito supplies Latin text, Cairo supplies Arabic; both are available in Dashboard, Chat and Landing. Cairo has weights 200-1000 and a slant axis; it is not Nunito's italic face.

Inspect and commit the installed files:

```bash
git diff -- frontend/src/app/layout.tsx 'frontend/src/app/(app)/nunito-local.css'
git add frontend/public/fonts frontend/src/app/layout.tsx 'frontend/src/app/(app)/nunito-local.css'
git commit -m "style(fonts): bundle verified Nunito and Cairo WOFF2"
git push origin main
```

Do not skip reviewing unrelated local changes before committing. Restart the application or rebuild its production bundle.

## Browser verification

DevTools Network must show successful same-origin `/fonts/*.woff2` responses with no Google Fonts request. On Arabic pages:

```js
await document.fonts.load('700 16px "JUBA Cairo Local"', 'اللغة العربية')
await document.fonts.load('700 16px "JUBA Nunito Local"', 'Learning')
[...document.fonts].filter(f => f.status === 'loaded').map(f => ({family:f.family, weight:f.weight, style:f.style}))
```

Check the Rendered Fonts panel on Arabic and Latin text to confirm the actual faces, not just computed font-family. Test Arabic joining, diacritics, Arabic-Indic digits and mixed LTR/RTL text.

## Verification performed here

The actual combined package passed isolated installation, rerun, installed-check, corrupt-font rejection, conflicting-binary rejection and incomplete-package rejection. No Next.js build or browser-rendering test was run. WOFF2 files are still not in GitHub until the local installation/commit above is performed.
