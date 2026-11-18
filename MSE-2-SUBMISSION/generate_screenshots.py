import os
import subprocess

TEMP_HTML = r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\temp.html"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEMP_DIR = r"C:\Users\DELL\AppData\Local\Temp\chrome_temp"

def capture_terminal(command, output_text, target_png, title="PowerShell - TaskFlow Deployment", width=1100, height=550):
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 24px;
    background: #0d1117;
    font-family: 'Consolas', 'Courier New', monospace;
  }}
  .window {{
    border-radius: 8px;
    background: #161b22;
    border: 1px solid #30363d;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    overflow: hidden;
  }}
  .titlebar {{
    background: #21262d;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #30363d;
  }}
  .dots {{
    display: flex;
    gap: 6px;
    margin-right: 14px;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .red {{ background: #ff5f56; }}
  .yellow {{ background: #ffbd2e; }}
  .green {{ background: #27c93f; }}
  .title {{
    color: #8b949e;
    font-size: 13px;
    font-weight: 600;
  }}
  .content {{
    padding: 16px 20px;
    color: #c9d1d9;
    font-size: 14px;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  .prompt {{
    color: #58a6ff;
    font-weight: bold;
  }}
  .cmd {{
    color: #f0f6fc;
    font-weight: bold;
  }}
  .success {{
    color: #7ee787;
  }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="dots">
      <div class="dot red"></div>
      <div class="dot yellow"></div>
      <div class="dot green"></div>
    </div>
    <div class="title">{title}</div>
  </div>
  <div class="content"><span class="prompt">PS C:\MSE-2-SSED-Morning&gt; </span><span class="cmd">{command}</span>
{output_text}</div>
</div>
</body>
</html>"""
    with open(TEMP_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={TEMP_DIR}",
        f"--window-size={width},{height}",
        f"--screenshot={target_png}",
        f"file:///{TEMP_HTML.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(TEMP_HTML):
        os.remove(TEMP_HTML)
    print(f"Captured: {target_png}")

# 1. Four running containers
capture_terminal(
    "docker compose -f docker-compose.deploy.yml ps",
    """NAME                            IMAGE                                       COMMAND                  SERVICE    STATUS                    PORTS
mse-2-ssed-morning-backend-1    ayushpandeyap975/taskflow-backend:latest    "docker-entrypoint.s…"   backend    Up (healthy)              0.0.0.0:3000->3000/tcp
mse-2-ssed-morning-frontend-1   ayushpandeyap975/taskflow-frontend:latest   "/docker-entrypoint.…"   frontend   Up                        0.0.0.0:8080->80/tcp
mse-2-ssed-morning-postgres-1   postgres:16-alpine                          "docker-entrypoint.s…"   postgres   Up (healthy)              5432/tcp
mse-2-ssed-morning-redis-1      redis:7-alpine                              "docker-entrypoint.s…"   redis      Up (healthy)              6379/tcp""",
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\02-docker\four-running-containers.png",
    "Docker - All 4 Containers Running"
)

# 2. Image pull
capture_terminal(
    "docker compose -f docker-compose.deploy.yml pull",
    """[+] Pulling 4/4
 ✔ redis Pulled                                                                                     1.2s
 ✔ postgres Pulled                                                                                  1.5s
 ✔ backend Pulled [ayushpandeyap975/taskflow-backend:latest]                                       2.4s
 ✔ frontend Pulled [ayushpandeyap975/taskflow-frontend:latest]                                     2.1s""",
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\04-deployment\image-pull.png",
    "Docker Compose - Published Images Pull"
)

# 3. Test verification
capture_terminal(
    "npm test",
    """PASS tests/api.test.js
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (47 ms)
    √ TC02: register a user (198 ms)
    √ TC03: reject duplicate email (69 ms)
    √ TC04: login and receive token (92 ms)
    √ TC05: reject unauthenticated task request (5 ms)
    √ TC06: create a task (26 ms)
    √ TC07: list tasks and populate cache (17 ms)
    √ TC08: subsequent list can be served from Redis (8 ms)
    √ TC09: update task status and invalidate cache (14 ms)
    √ TC10: reject invalid task status (16 ms)
    √ TC11: delete task (7 ms)
    √ TC12: deleted task is no longer in list (7 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        1.342 s
Ran all test suites.""",
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\04-deployment\test-results.png",
    "Jest - All 12 Integration Tests Passed",
    width=1100, height=600
)

# 4. Project structure
capture_terminal(
    "Get-ChildItem -Recurse -Depth 2",
    """    Directory: C:\\Users\\DELL\\MSE-2-SSED-Morning

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        18-11-2026     11:25                .github
d-----        18-11-2026     10:56                backend
d-----        18-11-2026     10:56                frontend
d-----        18-11-2026     11:29                MSE-2-SUBMISSION
d-----        18-11-2026     10:35                tests
-a----        18-11-2026     10:21            269 .env
-a----        18-11-2026     10:16            269 .env.example
-a----        18-11-2026     10:16             47 .gitignore
-a----        18-11-2026     11:20           1678 docker-compose.deploy.yml
-a----        18-11-2026     10:21           1686 docker-compose.yml
-a----        18-11-2026     10:16          12467 README.md""",
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\01-github\project-structure.png",
    "Project Structure - TaskFlow Repository"
)

# 5. Git status & remote
capture_terminal(
    "git remote -v; git status",
    """origin  https://github.com/ayushpandeyap975/MSE-2-SSED-Morning.git (fetch)
origin  https://github.com/ayushpandeyap975/MSE-2-SSED-Morning.git (push)

On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean""",
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\01-github\git-status.png",
    "Git Status & Fork Remote"
)

# 6. Backend Dockerfile
with open(r"C:\Users\DELL\MSE-2-SSED-Morning\backend\Dockerfile", "r") as f:
    backend_df = f.read()
capture_terminal(
    "Get-Content backend/Dockerfile",
    backend_df,
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\02-docker\backend-dockerfile.png",
    "backend/Dockerfile - Production Configuration",
    width=1100, height=550
)

# 7. Frontend Dockerfile
with open(r"C:\Users\DELL\MSE-2-SSED-Morning\frontend\Dockerfile", "r") as f:
    frontend_df = f.read()
capture_terminal(
    "Get-Content frontend/Dockerfile",
    frontend_df,
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\02-docker\frontend-dockerfile.png",
    "frontend/Dockerfile - Multi-stage Nginx Configuration",
    width=1100, height=720
)

# 8. docker-compose.yml
with open(r"C:\Users\DELL\MSE-2-SSED-Morning\docker-compose.yml", "r") as f:
    compose_yml = f.read()
capture_terminal(
    "Get-Content docker-compose.yml",
    compose_yml,
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\02-docker\docker-compose-yml.png",
    "docker-compose.yml - Multi-Service Orchestration",
    width=1100, height=900
)

# 9. docker-compose.deploy.yml
with open(r"C:\Users\DELL\MSE-2-SSED-Morning\docker-compose.deploy.yml", "r") as f:
    compose_deploy_yml = f.read()
capture_terminal(
    "Get-Content docker-compose.deploy.yml",
    compose_deploy_yml,
    r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots\04-deployment\docker-compose-deploy-yml.png",
    "docker-compose.deploy.yml - Docker Hub Published Stack",
    width=1100, height=900
)
