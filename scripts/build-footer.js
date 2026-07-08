#!/usr/bin/env node
// Stamps partials/footer.html into every index.html's <footer class="site-footer">...</footer> block.
// Run after editing the partial: node scripts/build-footer.js

const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const partial = fs.readFileSync(path.join(root, 'partials', 'footer.html'), 'utf8').trim();

const footerRegex = /<footer class="site-footer">[\s\S]*?<\/footer>/;

function findHtmlFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === 'node_modules' || entry.name === 'partials' || entry.name === 'scripts' || entry.name === 'docs' || entry.name === '.git') return [];
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return findHtmlFiles(full);
    if (entry.name === 'index.html') return [full];
    return [];
  });
}

const files = findHtmlFiles(root);
let changed = 0;

for (const file of files) {
  const html = fs.readFileSync(file, 'utf8');
  if (!footerRegex.test(html)) {
    console.log(`skip (no footer found): ${path.relative(root, file)}`);
    continue;
  }
  const updated = html.replace(footerRegex, partial);
  if (updated !== html) {
    fs.writeFileSync(file, updated, 'utf8');
    changed++;
    console.log(`updated: ${path.relative(root, file)}`);
  }
}

console.log(`\n${changed} file(s) updated, ${files.length} scanned.`);
