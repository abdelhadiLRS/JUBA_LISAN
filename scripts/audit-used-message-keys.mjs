import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceDir = path.join(root, 'frontend', 'src');
const messagesDir = path.join(sourceDir, 'messages');
const localeArg = process.argv.find((arg) => arg.startsWith('--locale='));
const locale = localeArg ? localeArg.slice('--locale='.length) : null;
const reportJson = process.argv.includes('--json');

function flatten(value, prefix = '', out = {}) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    for (const [key, child] of Object.entries(value)) {
      flatten(child, prefix ? prefix + '.' + key : key, out);
    }
  } else if (prefix) {
    out[prefix] = value;
  }
  return out;
}

function load(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['messages', 'node_modules', '.next'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walk(full));
    else if (/\.(ts|tsx)$/.test(entry.name)) files.push(full);
  }
  return files;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^$()|[\]{}\\]/g, '\\$&');
}

const sources = walk(sourceDir);
const used = new Map();
const dynamic = [];

function add(namespace, key, file) {
  if (!namespace || !key || key.includes('$')) return;
  const full = namespace + '.' + key;
  if (!used.has(full)) used.set(full, []);
  const rel = path.relative(root, file).replaceAll(path.sep, '/');
  if (!used.get(full).includes(rel)) used.get(full).push(rel);
}

function addDynamic(file, expression, kind) {
  const rel = path.relative(root, file).replaceAll(path.sep, '/');
  dynamic.push({ file: rel, kind, expression: expression.trim() });
}

for (const file of sources) {
  const source = fs.readFileSync(file, 'utf8');
  const bindings = new Map();

  // Capture the actual binding for both client and server next-intl APIs:
  // const t = useTranslations('foo')
  // const t = await getTranslations('foo')
  const bindingRe =
    /(?:(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:await\s+)?)?(useTranslations|getTranslations)\s*\(\s*(['"])([^'"]+)\3\s*\)/g;

  for (const match of source.matchAll(bindingRe)) {
    bindings.set(match[1] || 't', match[4]);
  }

  // Also recognize destructured getTranslations() results when present.
  const destructuredRe =
    /const\s*\{\s*([^}]+)\s*\}\s*=\s*(?:await\s+)?getTranslations\s*\(\s*(['"])([^'"]+)\2\s*\)/g;

  for (const match of source.matchAll(destructuredRe)) {
    for (const part of match[1].split(',')) {
      const pieces = part.trim().split(/\s*:\s*/);
      const binding = pieces[0].trim();
      if (/^[A-Za-z_$][\w$]*$/.test(binding)) bindings.set(binding, match[3]);
    }
  }

  for (const [binding, namespace] of bindings) {
    const escaped = escapeRegExp(binding);
    const callRe = new RegExp(
      `\\b${escaped}(?:\\.(?:rich|raw|markup|has|loading))?\\s*\\(\\s*(['"])([^'"]+)\\1`,
      'g',
    );
    for (const match of source.matchAll(callRe)) {
      add(namespace, match[2], file);
    }

    const dynamicCallRe = new RegExp(
      `\\b${escaped}(?:\\.(?:rich|raw|markup|has|loading))?\\s*\\(\\s*([^'"][^)]*)\\)`,
      'g',
    );
    for (const match of source.matchAll(dynamicCallRe)) {
      addDynamic(file, match[1], 'key');
    }
  }

  const dynamicNamespaceRe =
    /(?:useTranslations|getTranslations)\s*\(\s*([^'"][^)]*)\)/g;
  for (const match of source.matchAll(dynamicNamespaceRe)) {
    addDynamic(file, match[1], 'namespace');
  }
}

const english = flatten(load(path.join(messagesDir, 'en.json')));
const locales = fs
  .readdirSync(messagesDir)
  .filter((file) => file.endsWith('.json') && file !== 'en.json')
  .map((file) => file.replace(/\.json$/, ''))
  .sort();

const keys = [...used.keys()].sort();
const missingEnglish = keys.filter((key) => !(key in english));
const targets = locale ? locales.filter((item) => item === locale) : locales;
const coverage = {};

for (const target of targets) {
  const data = flatten(load(path.join(messagesDir, target + '.json')));
  const missing = keys.filter((key) => !(key in data));
  coverage[target] = {
    used: keys.length,
    translated: keys.length - missing.length,
    missing,
  };
}

const result = {
  filesScanned: sources.length,
  usedKeys: keys.length,
  missingEnglish,
  dynamicUsages: dynamic,
  coverage,
};

if (reportJson) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(
    `[i18n:used] scanned=${sources.length}, usedKeys=${keys.length}, missingEnglish=${missingEnglish.length}`,
  );

  for (const [name, stats] of Object.entries(coverage)) {
    const percent = stats.used ? ((stats.translated / stats.used) * 100).toFixed(1) : '100.0';
    console.log(`[i18n:used] ${name}: ${stats.translated}/${stats.used} (${percent}%)`);
    if (stats.missing.length) {
      console.log(
        '  missing: ' +
          stats.missing.slice(0, 30).join(', ') +
          (stats.missing.length > 30 ? ' …' : ''),
      );
    }
  }

  if (dynamic.length) {
    console.warn(
      '[i18n:used] dynamic translation usage found: ' +
        dynamic.length +
        '; review these calls manually.',
    );
  }
}
