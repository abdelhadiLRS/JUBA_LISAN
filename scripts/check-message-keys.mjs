import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const messagesDir = path.join(root, 'messages');
const referenceFile = path.join(messagesDir, 'en.json');

function flatten(value, prefix = '', out = {}) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    for (const [key, child] of Object.entries(value)) {
      const next = prefix ? `${prefix}.${key}` : key;
      flatten(child, next, out);
    }
    return out;
  }
  out[prefix] = typeof value === 'string' ? value : JSON.stringify(value);
  return out;
}

function load(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function placeholders(value) {
  return [...String(value).matchAll(/\{([a-zA-Z0-9_]+)(?:\s*,[^}]*)?\}/g)]
    .map((match) => match[1])
    .sort();
}

const reference = flatten(load(referenceFile));
const files = fs.readdirSync(messagesDir)
  .filter((file) => file.endsWith('.json') && file !== 'en.json')
  .sort();

let failed = false;

for (const file of files) {
  const locale = flatten(load(path.join(messagesDir, file)));
  const missing = Object.keys(reference).filter((key) => !(key in locale));
  const extra = Object.keys(locale).filter((key) => !(key in reference));
  const placeholderMismatches = Object.keys(reference)
    .filter((key) => key in locale)
    .filter((key) => JSON.stringify(placeholders(reference[key])) !== JSON.stringify(placeholders(locale[key])));

  if (missing.length || extra.length || placeholderMismatches.length) {
    failed = true;
    console.error(`[i18n] ${file}`);
    if (missing.length) console.error(`  missing: ${missing.join(', ')}`);
    if (extra.length) console.error(`  extra: ${extra.join(', ')}`);
    if (placeholderMismatches.length) console.error(`  placeholder mismatch: ${placeholderMismatches.join(', ')}`);
  } else {
    console.log(`[i18n] ${file}: OK`);
  }
}

if (failed) process.exit(1);
console.log(`[i18n] ${files.length} locales match en.json keys and placeholders.`);
