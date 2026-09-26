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
    for (const [key, child] of Object.entries(value)) flatten(child, prefix ? prefix + '.' + key : key, out);
  } else out[prefix] = value;
  return out;
}
function load(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
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
for (const file of sources) {
  const source = fs.readFileSync(file, 'utf8');
  const namespaceRe = /(?:useTranslations|getTranslations)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)/g;
  for (const nsMatch of source.matchAll(namespaceRe)) {
    const namespace = nsMatch[1];
    const start = nsMatch.index + nsMatch[0].length;
    const tail = source.slice(start, start + 12000);
    const callRe = /\bt(?:\.(?:rich|raw|markup|has|loading))?\s*\(\s*['\"]([^'\"]+)['\"]/g;
    for (const match of tail.matchAll(callRe)) add(namespace, match[1], file);
  }
  if (/(?:useTranslations|getTranslations)\s*\(\s*[^'\"]/.test(source)) dynamic.push(path.relative(root, file).replaceAll(path.sep, '/'));
}
const english = flatten(load(path.join(messagesDir, 'en.json')));
const locales = fs.readdirSync(messagesDir).filter((file) => file.endsWith('.json') && file !== 'en.json').map((file) => file.replace(/\.json$/, '')).sort();
const keys = [...used.keys()].sort();
const missingEnglish = keys.filter((key) => !(key in english));
const targets = locale ? locales.filter((item) => item === locale) : locales;
const coverage = {};
for (const target of targets) {
  const data = flatten(load(path.join(messagesDir, target + '.json')));
  const missing = keys.filter((key) => !(key in data));
  coverage[target] = { used: keys.length, translated: keys.length - missing.length, missing };
}
const result = { filesScanned: sources.length, usedKeys: keys.length, missingEnglish, dynamicUsages: dynamic, coverage };
if (reportJson) console.log(JSON.stringify(result, null, 2));
else {
  console.log('[i18n:used] scanned=' + sources.length + ', usedKeys=' + keys.length + ', missingEnglish=' + missingEnglish.length);
  for (const [name, stats] of Object.entries(coverage)) {
    const percent = stats.used ? ((stats.translated / stats.used) * 100).toFixed(1) : '100.0';
    console.log('[i18n:used] ' + name + ': ' + stats.translated + '/' + stats.used + ' (' + percent + '%)');
    if (stats.missing.length) console.log('  missing: ' + stats.missing.slice(0, 30).join(', ') + (stats.missing.length > 30 ? ' …' : ''));
  }
  if (dynamic.length) console.warn('[i18n:used] dynamic namespace usages: ' + dynamic.length + '; review manually.');
}
