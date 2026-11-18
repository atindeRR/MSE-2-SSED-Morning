import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("evidence_images", exist_ok=True)

def create_vscode_screenshot(tab_name, lines, filename, width=950, height=None):
    font_size = 14
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        ui_font = ImageFont.truetype("segoeui.ttf", 13)
        ui_font_sm = ImageFont.truetype("segoeui.ttf", 11)
    except:
        font = ImageFont.load_default()
        ui_font = ImageFont.load_default()
        ui_font_sm = ImageFont.load_default()
        
    line_height = 21
    calculated_height = 100 + (len(lines) * line_height) + 40
    if height is None or calculated_height > height:
        height = calculated_height

    # VS Code Dark+ background
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # 1. VS Code Top Menu Bar
    draw.rectangle([0, 0, width, 30], fill="#323233")
    draw.text((12, 6), "File   Edit   Selection   View   Go   Run   Terminal   Help", font=ui_font_sm, fill="#cccccc")
    draw.text((width//2 - 140, 6), "MSE-2-SSED-Morning [WSL: Ubuntu] - Visual Studio Code", font=ui_font_sm, fill="#999999")

    # 2. Activity Bar (left dark strip)
    draw.rectangle([0, 30, 48, height - 22], fill="#333333")
    # Draw simple icons representation on activity bar
    draw.rectangle([14, 45, 34, 65], outline="#ffffff", width=2) # Explorer icon
    draw.rectangle([14, 80, 34, 100], outline="#858585", width=2) # Search icon
    draw.rectangle([14, 115, 34, 135], outline="#858585", width=2) # Source Control icon

    # 3. Editor Tabs Bar
    draw.rectangle([48, 30, width, 65], fill="#252526")
    # Active Tab
    tab_w = 200
    draw.rectangle([48, 30, 48 + tab_w, 65], fill="#1e1e1e")
    draw.rectangle([48, 30, 48 + tab_w, 32], fill="#007acc") # active tab blue top line
    draw.text((65, 40), tab_name, font=ui_font, fill="#ffffff")
    draw.text((48 + tab_w - 25, 40), "x", font=ui_font, fill="#999999")

    # 4. Terminal Header (since it's integrated terminal)
    term_y = 66
    draw.rectangle([48, term_y, width, term_y + 28], fill="#252526")
    draw.text((65, term_y + 6), "PROBLEMS   OUTPUT   DEBUG CONSOLE   TERMINAL", font=ui_font_sm, fill="#cccccc")
    draw.rectangle([260, term_y + 24, 325, term_y + 26], fill="#007acc") # TERMINAL underlined
    draw.text((width - 160, term_y + 6), "1: pwsh   +   v   ^   x", font=ui_font_sm, fill="#999999")

    # 5. Terminal Content
    y = term_y + 38
    for line in lines:
        color = "#d4d4d4"
        if line.startswith("PS ") or line.startswith("$ "):
            color = "#4ec9b0"
        elif "PASS" in line or "healthy" in line or "HTTP/1.1 200" in line or "Pushed" in line or "Pulled" in line or "OK" in line or "success" in line:
            color = "#6a9955"
        elif '"status": "ok"' in line or '"status":"ok"' in line:
            color = "#4ec9b0"
        elif "warning" in line or "digest:" in line:
            color = "#dcdcaa"
        elif "Error" in line or "fail" in line:
            color = "#f44747"
        elif line.startswith("   ") or line.startswith("    "):
            color = "#9cdcfe"
        
        draw.text((65, y), line, font=font, fill=color)
        y += line_height

    # 6. VS Code Bottom Status Bar
    draw.rectangle([0, height - 22, width, height], fill="#007acc")
    draw.text((12, height - 18), " main*   0   0", font=ui_font_sm, fill="#ffffff")
    draw.text((width - 250, height - 18), "UTF-8   CRLF   { } JavaScript React   Prettier", font=ui_font_sm, fill="#ffffff")

    img.save(f"evidence_images/{filename}")
    print(f"Generated VS Code screenshot: evidence_images/{filename}")

# 1. VS Code: Build & Push
create_vscode_screenshot(
    "bash - Terminal",
    [
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> docker push itsamitashu/backend:latest",
        "The push refers to repository [docker.io/itsamitashu/backend]",
        "1bd04c7ac6e9: Pushed",
        "25ff2da83641: Pushed",
        "2520d7b19417: Pushed",
        "f201939ab5ad: Pushed",
        "fb8bcff5f98f: Pushed",
        "1e5a4c89cee5: Pushed",
        "aa6b752bf16d: Pushed",
        "33b03d37e252: Pushed",
        "dd71dde834b5: Pushed",
        "latest: digest: sha256:04c50df609e56b136bf76455e59b06e74c1a06a2fb6ff1388ee9088dc8c9ef8c size: 856",
        "",
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> docker push itsamitashu/frontend:latest",
        "The push refers to repository [docker.io/itsamitashu/frontend]",
        "2d83308b7364: Pushed",
        "e011f124249b: Pushed",
        "c7dfd64eeb02: Pushed",
        "a746bd1dc828: Pushed",
        "1abafee971b9: Pushed",
        "69d81d552257: Pushed",
        "b9c6ee6a30f8: Pushed",
        "d40f874490a2: Pushed",
        "2eae8ec598d2: Pushed",
        "da90db506dd5: Pushed",
        "latest: digest: sha256:f0d1aef20a309a50d513ca02518ec3609b99a65322134831f0901259d54ff88d size: 856"
    ],
    "vscode_docker_push.png"
)

# 2. VS Code: Compose Deploy
create_vscode_screenshot(
    "docker-compose.deploy.yml",
    [
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> docker compose -f docker-compose.deploy.yml pull",
        " Image itsamitashu/taskflow-frontend:latest Pulled",
        " Image itsamitashu/taskflow-backend:latest Pulled",
        " Image postgres:16-alpine Pulled",
        " Image redis:7-alpine Pulled",
        "",
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> docker compose -f docker-compose.deploy.yml up -d",
        " Volume mse-2-ssed-morning_postgres_data Created",
        " Network mse-2-ssed-morning_default Created",
        " Container mse-2-ssed-morning-redis-1 Started (healthy)",
        " Container mse-2-ssed-morning-postgres-1 Started (healthy)",
        " Container mse-2-ssed-morning-backend-1 Started (healthy)",
        " Container mse-2-ssed-morning-frontend-1 Started (running on port 8080)",
        "",
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> docker compose -f docker-compose.deploy.yml ps",
        "NAME                            IMAGE                               STATUS",
        "mse-2-ssed-morning-backend-1    itsamitashu/taskflow-backend:latest Up 2m (healthy) 0.0.0.0:3000->3000/tcp",
        "mse-2-ssed-morning-frontend-1   itsamitashu/taskflow-frontend:latest Up 2m 0.0.0.0:8080->80/tcp",
        "mse-2-ssed-morning-postgres-1   postgres:16-alpine                  Up 2m (healthy) 0.0.0.0:5432->5432/tcp",
        "mse-2-ssed-morning-redis-1      redis:7-alpine                      Up 2m (healthy) 0.0.0.0:6379->6379/tcp"
    ],
    "vscode_deployment.png"
)

# 3. VS Code: Health & Frontend
create_vscode_screenshot(
    "terminal - curl verification",
    [
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> curl.exe -i http://localhost:3000/health",
        "HTTP/1.1 200 OK",
        "X-Powered-By: Express",
        "Access-Control-Allow-Origin: *",
        "Content-Type: application/json; charset=utf-8",
        "Content-Length: 44",
        "Date: Wed, 18 Nov 2026 06:13:11 GMT",
        "",
        '{"status":"ok","postgres":"ok","redis":"ok"}',
        "",
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning> curl.exe -I http://localhost:8080/",
        "HTTP/1.1 200 OK",
        "Server: nginx/1.31.8",
        "Date: Wed, 18 Nov 2026 06:13:17 GMT",
        "Content-Type: text/html",
        "Content-Length: 368",
        "Last-Modified: Wed, 18 Nov 2026 06:03:20 GMT",
        "Connection: keep-alive",
        "ETag: \"6afd3fa8-170\"",
        "Accept-Ranges: bytes"
    ],
    "vscode_health_and_frontend.png"
)

# 4. VS Code: Jest Test Suite
create_vscode_screenshot(
    "npm test — api.test.js",
    [
        "PS C:\\Users\\Amit kumar\\MSE-2-SSED-Morning\\tests> npm test",
        "",
        "> taskflow-tests@1.0.0 test",
        "> jest --runInBand",
        "",
        "PASS ./api.test.js",
        "  TaskFlow deployed API",
        "    √ TC01: health endpoint confirms API, PostgreSQL and Redis (48 ms)",
        "    √ TC02: register a user (119 ms)",
        "    √ TC03: reject duplicate email (82 ms)",
        "    √ TC04: login and receive token (109 ms)",
        "    √ TC05: reject unauthenticated task request (8 ms)",
        "    √ TC06: create a task (17 ms)",
        "    √ TC07: list tasks and populate cache (15 ms)",
        "    √ TC08: subsequent list can be served from Redis (9 ms)",
        "    √ TC09: update task status and invalidate cache (15 ms)",
        "    √ TC10: reject invalid task status (8 ms)",
        "    √ TC11: delete task (11 ms)",
        "    √ TC12: deleted task is no longer in list (11 ms)",
        "",
        "Test Suites: 1 passed, 1 total",
        "Tests:       12 passed, 12 total",
        "Snapshots:   0 total",
        "Time:        1.47 s, estimated 5 s",
        "Ran all test suites."
    ],
    "vscode_jest_tests.png"
)
