#!/usr/bin/env node
// Documentation artifact renderer; no game code or original game assets.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import crypto from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const options = Object.fromEntries(process.argv.slice(2).reduce((pairs, item, i, args) => {
  if (item.startsWith('--')) pairs.push([item.slice(2), args[i + 1]]);
  return pairs;
}, []));
if (!options['playwright-module'] || !options.browser) {
  throw new Error('Usage: node tools/docs/render-mermaid.mjs --playwright-module /path/to/playwright/index.mjs --browser /path/to/chrome [--mermaid-js path]');
}
const bundle = path.resolve(root, options['mermaid-js'] || 'work/diagram-renderer/mermaid.min.js');
const packageInfo = JSON.parse(await fs.readFile(path.join(path.dirname(bundle), 'package.json'), 'utf8'));
if (packageInfo.version !== '12.2.0') throw new Error('Run the pinned prepare_mermaid.py first');
const { chromium } = await import(pathToFileURL(path.resolve(options['playwright-module'])).href);
const output = path.join(root, 'artifacts/diagrams');
const galleryDir = path.join(root, 'docs/diagrams');
await fs.mkdir(output, { recursive: true });
await fs.mkdir(galleryDir, { recursive: true });
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');

async function markdownFiles(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const nested = await Promise.all(entries.sort((a, b) => a.name.localeCompare(b.name)).map(async e => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? markdownFiles(p) : e.name.endsWith('.md') ? [p] : [];
  }));
  return nested.flat();
}
const diagrams = [];
for (const file of await markdownFiles(path.join(root, 'docs'))) {
  const markdown = await fs.readFile(file, 'utf8');
  const title = markdown.match(/^# (.+)$/m)?.[1] || path.basename(file);
  const matches = [...markdown.matchAll(/^```mermaid\s*\n([\s\S]*?)^```\s*$/gm)];
  for (let index = 0; index < matches.length; index++) {
    const match = matches[index];
    const relative = path.relative(root, file).split(path.sep).join('/');
    const id = relative.replace(/^docs\//, '').replace(/\.md$/, '').replaceAll('/', '--') + (matches.length > 1 ? `--${index + 1}` : '');
    const headings = [...markdown.slice(0, match.index).matchAll(/^## (.+)$/gm)];
    const section = headings.at(-1)?.[1] || title;
    const status = relative.includes('/original-game/') ? 'Original-game reference'
      : relative.endsWith('career-and-town-graph-v2.md') ? 'Current career proposal — details unapproved'
      : 'Earlier planning draft — see modern-direction review for amendments';
    diagrams.push({ id, title, section, source: relative, sourceLine: markdown.slice(0, match.index).split('\n').length,
      status, mermaid: match[1].trim() + '\n' });
  }
}
diagrams.sort((a, b) => Number(b.source.endsWith('career-and-town-graph-v2.md')) - Number(a.source.endsWith('career-and-town-graph-v2.md')) || a.source.localeCompare(b.source));
const browser = await chromium.launch({ executablePath: options.browser, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const records = [];
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1.5 });
  await page.route(/^https?:/, route => route.abort());
  await page.setContent('<!doctype html><html><body></body></html>');
  await page.addScriptTag({ path: bundle });
  await page.evaluate(() => mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base',
    fontFamily: 'Arial, sans-serif', themeVariables: { fontSize: '16px', primaryColor: '#fff4d9', primaryTextColor: '#142c3c',
      primaryBorderColor: '#537c82', lineColor: '#45656f', secondaryColor: '#d9edf0', tertiaryColor: '#f4ded2', background: '#ffffff' },
    flowchart: { htmlLabels: false, curve: 'linear', nodeSpacing: 28, rankSpacing: 42 } }));
  for (let i = 0; i < diagrams.length; i++) {
    const diagram = diagrams[i];
    const rendered = await page.evaluate(async ({ source, id }) => {
      const { svg } = await mermaid.render(id, source);
      document.body.innerHTML = svg;
      await document.fonts.ready;
      const element = document.querySelector('svg');
      const box = element.viewBox.baseVal;
      const width = Math.ceil(box.width), height = Math.ceil(box.height);
      element.setAttribute('width', width); element.setAttribute('height', height);
      element.style.maxWidth = 'none'; element.style.background = '#ffffff';
      return { svg: element.outerHTML, width, height };
    }, { source: diagram.mermaid, id: `diagram-${i}` });
    await fs.writeFile(path.join(output, diagram.id + '.mmd'), diagram.mermaid);
    await fs.writeFile(path.join(output, diagram.id + '.svg'), rendered.svg + '\n');
    await page.setViewportSize({ width: rendered.width + 32, height: Math.min(rendered.height + 32, 3000) });
    await page.evaluate(() => { document.body.style.margin = '16px'; });
    await page.locator('svg').screenshot({ path: path.join(output, diagram.id + '.png'), animations: 'disabled' });
    const { mermaid, ...metadata } = diagram;
    records.push({ ...metadata, sourceSha256: hash(mermaid), svg: diagram.id + '.svg', png: diagram.id + '.png',
      width: rendered.width, height: rendered.height,
      svgSha256: hash(await fs.readFile(path.join(output, diagram.id + '.svg'))),
      pngSha256: hash(await fs.readFile(path.join(output, diagram.id + '.png'))) });
    console.log(`Rendered ${diagram.source}: ${rendered.width} x ${rendered.height}`);
  }
  const manifest = { renderer: 'Mermaid 12.2.0 via local Playwright/Chromium', mermaidBundleSha256: hash(await fs.readFile(bundle)),
    chromiumVersion: browser.version(), network: 'HTTP requests blocked during rendering', diagrams: records };
  await fs.writeFile(path.join(output, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  const md = ['# Rendered Mermaid diagrams', '', 'Rendered directly from the documentation source. These are diagrams, not game screenshots. Original references and earlier proposals retain their own evidence/status; the career graph is a current proposal.', '',
    'Open the SVG for full-resolution zoom, or use the offline [HTML gallery](../../artifacts/diagrams/index.html). [Rebuild instructions](../../tools/docs/README.md).', ''];
  const cards = [];
  for (const d of records) {
    md.push(`## ${d.section}`, '', `**${d.status}.** From [${d.title}](../../${d.source}).`, '',
      `[Open SVG](../../artifacts/diagrams/${d.svg}) · [PNG](../../artifacts/diagrams/${d.png})`, '',
      `![${d.section}](../../artifacts/diagrams/${d.png})`, '');
    cards.push(`<section><h2>${escape(d.section)}</h2><p class="status">${escape(d.status)}</p><p><a href="../../${escape(d.source)}">Source document</a> · <a href="${d.svg}" target="_blank">Open SVG to zoom</a> · <a href="${d.png}">PNG</a></p><a href="${d.svg}" target="_blank"><img src="${d.svg}" alt="${escape(d.section)}"></a></section>`);
  }
  await fs.writeFile(path.join(galleryDir, 'README.md'), md.join('\n'));
  await fs.writeFile(path.join(output, 'index.html'), `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jones: rendered diagrams</title><style>body{font:17px/1.5 system-ui,sans-serif;background:#f6f2e8;color:#173746;margin:0;padding:32px}main{max-width:1500px;margin:auto}h1{margin-bottom:8px}section{background:white;padding:24px;border:1px solid #ccd6d4;border-radius:12px;margin:28px 0}section img{display:block;max-width:100%;height:auto;margin:24px auto}a{color:#126678}.status{color:#5d5548;font-weight:600}h2{margin:0}</style></head><body><main><h1>Rendered Mermaid diagrams</h1><p>Documentation diagrams, not game screens. Click a diagram for its full SVG, then zoom in your browser.</p>${cards.join('\n')}</main></body></html>\n`);
} finally { await browser.close(); }
console.log(`Rendered ${records.length} diagrams; gallery: docs/diagrams/README.md`);
