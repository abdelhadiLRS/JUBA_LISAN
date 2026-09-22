# Interface Translation Consistency

JUBA LISAN keeps `messages/en.json` as the reference locale for interface message structure.

## Automated parity check

From the frontend directory:

```bash
npm run check:i18n
```

The checker compares every locale JSON file against `en.json` and fails when it finds:

- a missing translation key;
- an unexpected extra key;
- a placeholder mismatch.

Nested message objects are flattened into stable dot-separated keys. ICU-style placeholders such as `{count}` and `{price}` are compared by name, so translators can change wording without changing the runtime contract.

The check is dependency-free and runs in the frontend quality workflow before linting, type checking, tests, and the production build.

## Translation workflow

1. Add the new key to `messages/en.json`.
2. Translate the same key in every locale.
3. Preserve the placeholder names used by the English reference.
4. Run `npm run check:i18n`.
5. Run the normal frontend quality commands before merging.

This keeps new lesson, mastery, billing, and accessibility UI from silently falling back to missing-message behavior in secondary locales.
