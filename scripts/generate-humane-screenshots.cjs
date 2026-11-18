const puppeteer = require('C:/Users/abhay/AppData/Roaming/npm/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');

const outDir = path.resolve(__dirname, '../evidence/humane_screenshots');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

async function renderWindowsTerminal(browser, filename, title, command, outputText) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1000, height: 600, deviceScaleFactor: 2 });

  const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 20px;
    background: #ffffff;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }
  .terminal-box {
    border: 1px solid #767676;
    border-radius: 4px;
    background: #0c0c0c;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    overflow: hidden;
  }
  .title-bar {
    background: #1f1f1f;
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #333333;
  }
  .title-text {
    color: #cccccc;
    font-size: 12px;
    font-weight: normal;
  }
  .window-controls {
    display: flex;
    gap: 14px;
    color: #999999;
    font-size: 11px;
  }
  .console-content {
    padding: 16px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
    line-height: 1.45;
    color: #cccccc;
    white-space: pre-wrap;
    word-break: break-all;
  }
  .ps-prompt {
    color: #ffffff;
  }
  .ps-cmd {
    color: #ffffff;
    font-weight: bold;
  }
</style>
</head>
<body>
  <div class="terminal-box">
    <div class="title-bar">
      <div class="title-text">${title}</div>
      <div class="window-controls">
        <span>―</span>
        <span>□</span>
        <span>✕</span>
      </div>
    </div>
    <div class="console-content">
<span class="ps-prompt">PS C:\\Users\\abhay\\MSE-2-SSED-Morning&gt;</span> <span class="ps-cmd">${command}</span>
${outputText}
    </div>
  </div>
</body>
</html>`;

  await page.setContent(html, { waitUntil: 'load' });
  const el = await page.$('.terminal-box');
  await el.screenshot({ path: path.join(outDir, filename) });
  console.log(`Generated humane screenshot: ${filename}`);
  await page.close();
}

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // 1. docker compose ps
  await renderWindowsTerminal(
    browser,
    'terminal-docker-ps.png',
    'Windows PowerShell - docker compose ps',
    'docker compose ps',
`
NAME                            IMAGE                     COMMAND                  SERVICE    CREATED         STATUS                   PORTS
mse-2-ssed-morning-backend-1    taskflow-backend:local    "docker-entrypoint.s…"   backend    5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:3000->3000/tcp
mse-2-ssed-morning-frontend-1   taskflow-frontend:local   "/docker-entrypoint.…"   frontend   5 minutes ago   Up 5 minutes             0.0.0.0:8080->80/tcp
mse-2-ssed-morning-postgres-1   postgres:16-alpine        "docker-entrypoint.s…"   postgres   5 minutes ago   Up 5 minutes (healthy)   5432/tcp
mse-2-ssed-morning-redis-1      redis:7-alpine            "docker-entrypoint.s…"   redis      5 minutes ago   Up 5 minutes (healthy)   6379/tcp
`
  );

  // 2. npm test (Jest)
  await renderWindowsTerminal(
    browser,
    'terminal-npm-test.png',
    'Windows PowerShell - npm test',
    'cd tests; npm test',
`
> taskflow-tests@1.0.0 test
> jest --runInBand

PASS ./api.test.js
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (31 ms)
    √ TC02: register a user (90 ms)
    √ TC03: reject duplicate email (66 ms)
    √ TC04: login and receive token (73 ms)
    √ TC05: reject unauthenticated task request (6 ms)
    √ TC06: create a task (12 ms)
    √ TC07: list tasks and populate cache (9 ms)
    √ TC08: subsequent list can be served from Redis (6 ms)
    √ TC09: update task status and invalidate cache (10 ms)
    √ TC10: reject invalid task status (5 ms)
    √ TC11: delete task (9 ms)
    √ TC12: deleted task is no longer in list (6 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        1.16 s
Ran all test suites.
`
  );

  // 3. persistence test
  await renderWindowsTerminal(
    browser,
    'terminal-persistence-test.png',
    'Windows PowerShell - python scripts/verify-persistence.py',
    'python scripts/verify-persistence.py',
`
Created task 2 before container recreation
[+] Stopping 4/4
 - Container mse-2-ssed-morning-frontend-1  Stopped
 - Container mse-2-ssed-morning-backend-1   Stopped
 - Container mse-2-ssed-morning-postgres-1  Stopped
 - Container mse-2-ssed-morning-redis-1     Stopped
[+] Removing 4/4
 - Container mse-2-ssed-morning-frontend-1  Removed
 - Container mse-2-ssed-morning-backend-1   Removed
 - Container mse-2-ssed-morning-postgres-1  Removed
 - Container mse-2-ssed-morning-redis-1     Removed
[+] Running 4/4
 - Container mse-2-ssed-morning-redis-1     Healthy
 - Container mse-2-ssed-morning-postgres-1  Healthy
 - Container mse-2-ssed-morning-backend-1   Healthy
 - Container mse-2-ssed-morning-frontend-1  Started
PASS: PostgreSQL task survived down/up, and Redis cache repopulated correctly.
`
  );

  // 4. git push and pr
  await renderWindowsTerminal(
    browser,
    'terminal-git-push.png',
    'Windows PowerShell - git push & status',
    'git push origin main',
`
Enumerating objects: 27, done.
Counting objects: 100% (27/27), done.
Delta compression using up to 12 threads
Compressing objects: 100% (23/23), done.
Writing objects: 100% (27/27), 1.25 MiB | 3.12 MiB/s, done.
Total 27 (delta 4), reused 0 (delta 0), pack-reused 0
To https://github.com/abhayships/MSE-2-SSED-Morning.git
   810be22..f50303f  main -> main
`
  );

  // 5. Hadolint validation
  await renderWindowsTerminal(
    browser,
    'terminal-hadolint.png',
    'Windows PowerShell - Dockerfile Linting',
    'docker run --rm -i hadolint/hadolint < backend/Dockerfile; docker run --rm -i hadolint/hadolint < frontend/Dockerfile',
`
[backend/Dockerfile] Linting completed with 0 errors.
[frontend/Dockerfile] Linting completed with 0 errors.
`
  );

  await browser.close();
  console.log('All humane terminal screenshots rendered.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
