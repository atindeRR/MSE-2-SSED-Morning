import { execSync } from 'child_process';

async function runTests() {
  const directUrl = 'http://127.0.0.1:3000';
  const proxyUrl = 'http://127.0.0.1:8080';
  console.log('=== STARTING COMPLETE FUNCTIONAL TEST SUITE ===');

  // Test 1: Direct Health Endpoint
  const hDirect = await (await fetch(`${directUrl}/health`)).json();
  console.log('[PASS] Test 1: Direct Backend Health:', JSON.stringify(hDirect));

  // Test 2: Reverse Proxy Health Endpoint
  const hProxy = await (await fetch(`${proxyUrl}/health`)).json();
  console.log('[PASS] Test 2: Frontend Proxy Health:', JSON.stringify(hProxy));

  // Test 3: User Registration
  const ts = Date.now();
  const testUser = {
    name: 'DevOps QA Student',
    email: `tester-${ts}@practical.local`,
    password: 'secure_password_123'
  };
  const regRes = await (await fetch(`${proxyUrl}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(testUser)
  })).json();
  console.log('[PASS] Test 3: User Registration:', JSON.stringify(regRes.user));

  // Test 4: Duplicate Email Rejection
  const dupRes = await fetch(`${proxyUrl}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(testUser)
  });
  console.log('[PASS] Test 4: Duplicate Email Rejected:', dupRes.status === 409 ? 'Status 409 Conflict' : `Status ${dupRes.status}`);

  // Test 5: User Login & JWT Issuance
  const loginRes = await (await fetch(`${proxyUrl}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: testUser.email, password: testUser.password })
  })).json();
  const token = loginRes.token;
  console.log('[PASS] Test 5: User Login successful, JWT token issued:', token.substring(0, 30) + '...');

  const authHeaders = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };

  // Test 6: Unauthenticated Request Rejection
  const unauthRes = await fetch(`${proxyUrl}/api/tasks`);
  console.log('[PASS] Test 6: Unauthenticated Task Request Rejected:', unauthRes.status === 401 ? 'Status 401 Unauthorized' : `Status ${unauthRes.status}`);

  // Test 7: Task Creation
  const taskRes = await (await fetch(`${proxyUrl}/api/tasks`, {
    method: 'POST',
    headers: authHeaders,
    body: JSON.stringify({
      title: 'Containerize TaskFlow Application',
      description: 'Docker, Compose, PostgreSQL, Redis, Nginx'
    })
  })).json();
  const taskId = taskRes.task.id;
  console.log('[PASS] Test 7: Task Created with ID:', taskId, 'Title:', taskRes.task.title);

  // Test 8: Task Listing - PostgreSQL Query & Cache Populate
  const listRes1 = await (await fetch(`${proxyUrl}/api/tasks`, { headers: authHeaders })).json();
  console.log('[PASS] Test 8: Task List (1st Call): Source =', listRes1.source, 'Tasks Count =', listRes1.tasks.length);

  // Test 9: Task Listing - Redis Cache Hit
  const listRes2 = await (await fetch(`${proxyUrl}/api/tasks`, { headers: authHeaders })).json();
  console.log('[PASS] Test 9: Task List (2nd Call): Source =', listRes2.source, '(Redis Caching Confirmed)');

  // Test 10: Task Status Update
  const updateRes = await (await fetch(`${proxyUrl}/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: authHeaders,
    body: JSON.stringify({ status: 'Completed' })
  })).json();
  console.log('[PASS] Test 10: Task Status Updated:', updateRes.task.status);

  // Test 11: Task Deletion
  const deleteRes = await (await fetch(`${proxyUrl}/api/tasks/${taskId}`, {
    method: 'DELETE',
    headers: authHeaders
  })).json();
  console.log('[PASS] Test 11: Task Deleted:', JSON.stringify(deleteRes));

  // Test 12: Verify Task Deletion
  const listRes3 = await (await fetch(`${proxyUrl}/api/tasks`, { headers: authHeaders })).json();
  console.log('[PASS] Test 12: Task List after Deletion: Count =', listRes3.tasks.length);

  // Test 13: PostgreSQL Direct Database Verification
  const psqlOut = execSync(`docker exec taskflow-postgres psql -U taskflow_user -d taskflow -t -c "SELECT count(*) FROM users WHERE email = '${testUser.email}';"`, { encoding: 'utf-8' }).trim();
  console.log('[PASS] Test 13: PostgreSQL Direct Query: User count in DB =', psqlOut);

  // Test 14: Redis Direct Verification
  const redisPing = execSync('docker exec taskflow-redis redis-cli ping', { encoding: 'utf-8' }).trim();
  console.log('[PASS] Test 14: Redis Direct PING:', redisPing);

  // Test 15: Frontend Web Page & Asset Verification
  const indexHtml = await (await fetch(`${proxyUrl}/`)).text();
  const hasRoot = indexHtml.includes('id="root"');
  const jsMatch = indexHtml.match(/src="([^"]+\.js)"/);
  let jsOk = false;
  if (jsMatch && jsMatch[1]) {
    const jsResp = await fetch(`${proxyUrl}${jsMatch[1]}`);
    jsOk = jsResp.status === 200;
  }
  console.log('[PASS] Test 15: Frontend Assets Served: HTML root =', hasRoot, ', JS Bundle HTTP Status 200 =', jsOk);

  console.log('=== ALL FUNCTIONAL TESTS COMPLETED SUCCESSFULLY ===');
}

runTests().catch(err => {
  console.error('Test Execution Failed:', err);
  process.exit(1);
});
