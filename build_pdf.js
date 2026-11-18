import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { marked } from 'file:///C:/Users/Ayushman/AppData/Roaming/npm/node_modules/marked/lib/marked.esm.js';

const rootDir = process.cwd();
const mdPath = path.join(rootDir, '202401100300089_Ayushman Bhowmik.md');
const htmlPath = path.join(rootDir, 'submission_doc.html');
const pdfPath = path.join(rootDir, '202401100300089_Ayushman Bhowmik.pdf');

console.log('Reading markdown file...');
let mdContent = fs.readFileSync(mdPath, 'utf8');

// Replace image references with base64 data URIs so headless browser loads them instantaneously
mdContent = mdContent.replace(/!\[([^\]]*)\]\((images\/[^\)]+)\)/g, (match, alt, imgRelPath) => {
  const decodedRelPath = decodeURIComponent(imgRelPath);
  const fullImgPath = path.join(rootDir, decodedRelPath);
  if (fs.existsSync(fullImgPath)) {
    console.log(`Embedding image: ${decodedRelPath}`);
    const imgData = fs.readFileSync(fullImgPath);
    const base64 = imgData.toString('base64');
    const ext = path.extname(fullImgPath).replace('.', '').toLowerCase();
    const mime = ext === 'png' ? 'image/png' : ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : 'image/png';
    return `![${alt}](data:${mime};base64,${base64})`;
  } else {
    console.warn(`Warning: Image not found at ${fullImgPath}`);
    return match;
  }
});

const bodyHtml = marked.parse(mdContent);

const fullHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Docker Practical Examination Documentation</title>
<style>
  @page {
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #24292e;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }
  h1 {
    font-size: 20pt;
    border-bottom: 2px solid #eaecef;
    padding-bottom: 8px;
    margin-top: 16px;
    margin-bottom: 12px;
    color: #0366d6;
  }
  h2 {
    font-size: 15pt;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
    color: #24292e;
  }
  h3 {
    font-size: 12pt;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
    color: #24292e;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 16px;
    page-break-inside: avoid;
    font-size: 9.5pt;
  }
  th, td {
    border: 1px solid #d0d7de;
    padding: 6px 10px;
    text-align: left;
  }
  th {
    background-color: #f6f8fa;
    font-weight: 600;
  }
  tr:nth-child(even) td {
    background-color: #fbfcfd;
  }
  code {
    background-color: rgba(175, 184, 193, 0.2);
    padding: 2px 5px;
    border-radius: 4px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 85%;
  }
  pre {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 12px;
    overflow-x: auto;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
  }
  pre code {
    background-color: transparent;
    padding: 0;
    font-size: inherit;
  }
  img {
    max-width: 95%;
    height: auto;
    display: block;
    margin: 12px auto;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    page-break-inside: avoid;
  }
  hr {
    border: 0;
    height: 1px;
    background: #e1e4e8;
    margin: 20px 0;
  }
  blockquote {
    border-left: 4px solid #0366d6;
    padding: 4px 12px;
    color: #57606a;
    background-color: #f6f8fa;
    margin: 12px 0;
  }
  ul, ol {
    padding-left: 24px;
    margin-bottom: 12px;
  }
  li {
    margin-bottom: 4px;
  }
  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>
${bodyHtml}
</body>
</html>`;

fs.writeFileSync(htmlPath, fullHtml, 'utf8');
console.log('Generated HTML at:', htmlPath);

// Find Chrome or Edge
const browserPaths = [
  'C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe',
  'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
  'C:\\\\Program Files\\\\BraveSoftware\\\\Brave-Browser\\\\Application\\\\brave.exe'
];

let browserPath = browserPaths.find(p => fs.existsSync(p));

if (!browserPath) {
  console.error('No supported browser found for PDF conversion.');
  process.exit(1);
}

console.log('Using browser:', browserPath);

const cmd = `"${browserPath}" --headless=new --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="${pdfPath}" "${htmlPath}"`;
console.log('Generating PDF...');
try {
  execSync(cmd, { stdio: 'inherit' });
  console.log('Successfully generated PDF at:', pdfPath);
  const stats = fs.statSync(pdfPath);
  console.log('PDF file size:', (stats.size / 1024).toFixed(1), 'KB');
} catch (err) {
  console.error('Error generating PDF:', err.message);
  process.exit(1);
}
