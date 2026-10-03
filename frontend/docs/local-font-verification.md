# Local Nunito verification

The authenticated application now imports `nunito-local.css`, which uses only local font faces and never requests Google Fonts or another remote asset. It resolves `Nunito` or `Nunito Variable` from the operating system and falls back to the system UI stack when the font is not installed.

Verify in a browser console on an authenticated page:

```js
await document.fonts.ready
[...document.fonts].some(font => font.family === 'JUBA Nunito Local' && font.status === 'loaded')
```

For a deterministic production result, ship a licensed Nunito WOFF2 in `frontend/public/fonts/Nunito[wght].woff2` and add it before the `local()` sources. The current repository contains no font binary, so the browser's local Nunito installation is the verified source and systems without Nunito use the declared fallback.
