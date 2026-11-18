import { randomBytes } from 'node:crypto';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const envPath = resolve(root, '.env');
const [command, ...args] = process.argv.slice(2);

function parseTemplate() {
  return Object.fromEntries(
    readFileSync(resolve(root, '.env.example'), 'utf8')
      .split(/\r?\n/)
      .map(line => line.match(/^\s*([A-Z][A-Z0-9_]*)=(.*)$/))
      .filter(Boolean)
      .map(([, key, value]) => [key, value.trim()])
  );
}

function validatePort(port) {
  if (!/^\d+$/.test(port) || Number(port) < 1 || Number(port) > 65535) {
    throw new Error('The frontend host port must be between 1 and 65535.');
  }
  return port;
}

if (command === 'init') {
  if (args.length && (args.length !== 2 || args[0] !== '--frontend-port')) {
    throw new Error('Usage: node tools/configure-env.mjs init [--frontend-port PORT]');
  }
  if (existsSync(envPath)) {
    console.log('Existing .env preserved. No credentials were changed or printed.');
    process.exit(0);
  }

  const template = parseTemplate();
  const database = template.POSTGRES_DB;
  const user = template.POSTGRES_USER;
  if (!database || !user || template.PORT !== '3000') {
    throw new Error('The template must contain the inspected database/user and PORT=3000.');
  }
  const frontendPort = validatePort(args[1] || template.FRONTEND_HOST_PORT || '8080');
  const password = randomBytes(24).toString('hex');
  const jwtSecret = randomBytes(32).toString('hex');
  const databaseUrl = `postgresql://${encodeURIComponent(user)}:${password}@postgres:5432/${encodeURIComponent(database)}`;

  const contents = [
    '# Local runtime configuration. Keep this file out of Git and screenshots.',
    `POSTGRES_DB=${database}`,
    `POSTGRES_USER=${user}`,
    `POSTGRES_PASSWORD=${password}`,
    `DATABASE_URL=${databaseUrl}`,
    `REDIS_URL=${template.REDIS_URL || 'redis://redis:6379'}`,
    `JWT_SECRET=${jwtSecret}`,
    'PORT=3000',
    `FRONTEND_HOST_PORT=${frontendPort}`,
    ''
  ].join('\n');

  writeFileSync(envPath, contents, { flag: 'wx', mode: 0o600 });
  console.log('Created local .env with generated PostgreSQL and JWT secrets. Secret values were not printed.');
  console.log(`Frontend host port: ${frontendPort}`);
} else if (command === 'dockerhub') {
  const [username] = args;
  if (args.length !== 1 || !/^[a-z0-9][a-z0-9_-]*$/.test(username || '')) {
    throw new Error('Usage: node tools/configure-env.mjs dockerhub YOUR_DOCKERHUB_USERNAME');
  }
  if (!existsSync(envPath)) {
    throw new Error('Initialize the local .env before configuring the Docker Hub username.');
  }
  const contents = readFileSync(envPath, 'utf8');
  const line = `DOCKERHUB_USERNAME=${username}`;
  const updated = /^DOCKERHUB_USERNAME=.*$/m.test(contents)
    ? contents.replace(/^DOCKERHUB_USERNAME=.*$/m, line)
    : `${contents.trimEnd()}\n${line}\n`;
  writeFileSync(envPath, updated, { mode: 0o600 });
  console.log(`Docker Hub username configured: ${username}. Existing secrets were not printed.`);
} else {
  throw new Error('Commands: init [--frontend-port PORT], dockerhub USERNAME');
}
