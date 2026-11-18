import app from './app.js';
import { config } from './config.js';
import { waitForDatabase } from './db.js';
import { connectRedis, redis } from './redis.js';
import { pool } from './db.js';

async function start() {
  await waitForDatabase();
  await connectRedis();

  const server = app.listen(config.port, '0.0.0.0', () => {
    console.log(`Backend listening on port ${config.port}`);
  });

  async function shutdown() {
    server.close();
    if (redis.isOpen) await redis.quit();
    await pool.end();
    process.exit(0);
  }

  process.on('SIGTERM', shutdown);
  process.on('SIGINT', shutdown);
}

start().catch(error => {
  console.error('Failed to start backend:', error);
  process.exit(1);
});
