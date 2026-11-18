const puppeteer = require('C:/Users/abhay/AppData/Roaming/npm/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.resolve(__dirname, '../evidence/screenshots');
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function run() {
  const email = 'abhay.202401100300005@kiet.edu';
  const password = 'Password@123';
  const name = 'Abhay Singh Tomar';

  // 1. Register user via backend API
  try {
    const regRes = await fetch('http://localhost:3000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
  } catch (e) {
    console.log('User might already exist:', e.message);
  }

  // 2. Login to get token
  const loginRes = await fetch('http://localhost:3000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const loginData = await loginRes.json();
  const token = loginData.token;
  const user = loginData.user;

  // 3. Add tasks
  const sampleTasks = [
    { title: 'Frontend & Backend Containerization', description: 'Production multi-stage Dockerfiles created following best practices' },
    { title: 'Multi-Container Orchestration', description: 'Docker Compose orchestrating Frontend, Backend, PostgreSQL, and Redis' },
    { title: 'PostgreSQL Storage & Redis Caching', description: 'Data persistence and sub-millisecond query caching verified' }
  ];

  for (const t of sampleTasks) {
    await fetch('http://localhost:3000/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify(t)
    });
  }

  // Populate cache
  await fetch('http://localhost:3000/api/tasks', {
    headers: { Authorization: `Bearer ${token}` }
  });

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // Screenshot 1: Auth / Login page
  const page1 = await browser.newPage();
  await page1.setViewport({ width: 1280, height: 800 });
  await page1.goto('http://localhost:8080/', { waitUntil: 'networkidle2' });
  await page1.screenshot({ path: path.join(SCREENSHOT_DIR, '01-taskflow-login.png'), fullPage: true });
  console.log('Saved 01-taskflow-login.png');

  // Screenshot 2: Dashboard with logged in user and tasks
  const page2 = await browser.newPage();
  await page2.setViewport({ width: 1280, height: 900 });
  await page2.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded' });
  await page2.evaluate((token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  }, token, user);
  await page2.goto('http://localhost:8080/', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1000));
  await page2.screenshot({ path: path.join(SCREENSHOT_DIR, '02-taskflow-dashboard.png'), fullPage: true });
  console.log('Saved 02-taskflow-dashboard.png');

  // Screenshot 3: Backend health endpoint
  const page3 = await browser.newPage();
  await page3.setViewport({ width: 1000, height: 600 });
  await page3.goto('http://localhost:3000/health', { waitUntil: 'networkidle2' });
  await page3.screenshot({ path: path.join(SCREENSHOT_DIR, '03-backend-health.png') });
  console.log('Saved 03-backend-health.png');

  await browser.close();
  console.log('All browser evidence screenshots captured successfully.');
}

run().catch(err => {
  console.error('Error capturing evidence:', err);
  process.exit(1);
});
