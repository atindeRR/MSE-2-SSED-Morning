"""Verify an API-created task survives container recreation; never delete volumes."""
import json
import os
import secrets
import subprocess
from urllib.request import Request, urlopen

base = os.environ.get('BASE_URL', 'http://localhost:3000')
compose = ['docker', 'compose']
if os.environ.get('COMPOSE_FILE'):
    compose += ['-f', os.environ['COMPOSE_FILE']]

def request(path, payload=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    data = json.dumps(payload).encode() if payload is not None else None
    with urlopen(Request(base + path, data=data, headers=headers), timeout=15) as r:
        return json.load(r)

email = 'persistence-' + secrets.token_hex(8) + '@example.com'
password = secrets.token_hex(16)
request('/api/auth/register', {'name': 'Persistence Verification', 'email': email, 'password': password})
token = request('/api/auth/login', {'email': email, 'password': password})['token']
task = request('/api/tasks', {'title': 'PostgreSQL persistence verified', 'description': 'This task must survive docker compose down and up without volume deletion.'}, token)['task']
print('Created task', task['id'], 'before container recreation', flush=True)
subprocess.run(compose + ['down'], check=True)
subprocess.run(compose + ['up', '-d', '--wait', '--wait-timeout', '180'], check=True)
# Re-login also works if the deployment rotated the JWT secret.
token = request('/api/auth/login', {'email': email, 'password': password})['token']
tasks = request('/api/tasks', token=token)
assert any(t['id'] == task['id'] and t['title'] == task['title'] for t in tasks['tasks'])
assert tasks['source'] == 'postgres', 'Redis must start empty after recreation'
assert request('/api/tasks', token=token)['source'] == 'redis-cache'
print('PASS: PostgreSQL task survived down/up, and Redis cache repopulated correctly.')
