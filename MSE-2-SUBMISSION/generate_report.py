import os
import subprocess

def build_report(student_name, roll_number, section, branch, github_username, dockerhub_username, pdf_filename):
    repo_url = f"https://github.com/{github_username}/MSE-2-SSED-Morning"
    target_repo = "https://github.com/atindeRR/MSE-2-SSED-Morning"
    frontend_img_url = f"https://hub.docker.com/r/{dockerhub_username}/frontend"
    backend_img_url = f"https://hub.docker.com/r/{dockerhub_username}/backend"
    
    screenshots_dir = r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\screenshots"
    
    def img_tag(rel_path, caption, fig_num):
        full_path = os.path.join(screenshots_dir, rel_path).replace("\\", "/")
        return f"""
        <div class="figure">
          <img src="file:///{full_path}" alt="{caption}" />
          <div class="caption">Figure {fig_num}: {caption}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>MSE-2 Practical Report - {student_name} ({roll_number})</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    color: #24292e;
    line-height: 1.55;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}
  .page-break {{
    page-break-after: always;
  }}
  .cover {{
    text-align: center;
    padding-top: 40px;
    height: 88vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .cover h1 {{
    font-size: 24pt;
    color: #0366d6;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  .cover h2 {{
    font-size: 15pt;
    color: #586069;
    font-weight: 400;
    margin-top: 0;
  }}
  .badge {{
    display: inline-block;
    background: #0366d6;
    color: #fff;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 11.5pt;
    font-weight: 600;
    margin: 15px 0;
  }}
  .meta-box {{
    margin: 30px auto;
    width: 82%;
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 18px 26px;
    text-align: left;
    background: #f6f8fa;
  }}
  .meta-box table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .meta-box td {{
    padding: 7px 10px;
    font-size: 10.5pt;
  }}
  .meta-box td.label {{
    font-weight: bold;
    color: #444d56;
    width: 42%;
  }}
  h2.section-title {{
    color: #0366d6;
    border-bottom: 2px solid #0366d6;
    padding-bottom: 4px;
    margin-top: 22px;
    font-size: 14pt;
  }}
  h3 {{
    color: #24292e;
    font-size: 11.5pt;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  p, li {{
    text-align: justify;
    font-size: 10pt;
  }}
  code {{
    background: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
    padding: 2px 5px;
    font-family: 'Consolas', monospace;
    font-size: 9pt;
    color: #d73a49;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
  }}
  table.data-table th, table.data-table td {{
    border: 1px solid #d1d5da;
    padding: 6px 8px;
    text-align: left;
  }}
  table.data-table th {{
    background: #f6f8fa;
    color: #24292e;
    font-weight: 600;
  }}
  .figure {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
  }}
  .figure img {{
    max-width: 95%;
    max-height: 340px;
    border: 1px solid #d1d5da;
    border-radius: 6px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
  }}
  .caption {{
    font-size: 8.5pt;
    color: #586069;
    margin-top: 5px;
    font-weight: 500;
  }}
  .declaration-box {{
    border-left: 4px solid #28a745;
    background: #f0fff4;
    padding: 12px 18px;
    margin: 20px 0;
    font-style: italic;
    font-size: 10pt;
  }}
  .checklist {{
    list-style: none;
    padding-left: 0;
  }}
  .checklist li:before {{
    content: "✓ ";
    color: #28a745;
    font-weight: bold;
    font-size: 11pt;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover page-break">
  <div>
    <p style="font-size: 12pt; letter-spacing: 2px; color: #586069; margin-bottom: 0;">DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING</p>
    <h1>MSE-2 Practical Examination</h1>
    <h2>Software Engineering and DevOps (AI310B) &mdash; Morning Shift</h2>
    <div class="badge">Full-Stack Application Containerization &amp; CI/CD</div>
  </div>

  <div class="meta-box">
    <table>
      <tr><td class="label">Candidate Name:</td><td><strong>{student_name}</strong></td></tr>
      <tr><td class="label">University Roll Number:</td><td><strong>{roll_number}</strong></td></tr>
      <tr><td class="label">Academic Section:</td><td><strong>{section}</strong></td></tr>
      <tr><td class="label">Branch of Study:</td><td><strong>{branch}</strong></td></tr>
      <tr><td class="label">GitHub Repository:</td><td><a href="{repo_url}">{github_username}/MSE-2-SSED-Morning</a></td></tr>
      <tr><td class="label">Docker Hub Account:</td><td><a href="{frontend_img_url}">{dockerhub_username}</a></td></tr>
      <tr><td class="label">Target Instructor Repo:</td><td><a href="{target_repo}">atindeRR/MSE-2-SSED-Morning</a></td></tr>
      <tr><td class="label">Evaluation Date:</td><td>18 November 2026</td></tr>
    </table>
  </div>

  <div style="color: #6a737d; font-size: 9.5pt;">
    TaskFlow Full-Stack Multi-Container Orchestration<br/>
    React &middot; Node.js &middot; Express &middot; PostgreSQL &middot; Redis &middot; Docker Compose &middot; GitHub Actions
  </div>
</div>

<!-- SECTION 1: INTRODUCTION & REPOSITORY -->
<h2 class="section-title">1. Introduction &amp; Repository Setup</h2>
<p>
This examination demonstrates the complete end-to-end containerization, multi-service orchestration, image distribution, and automated deployment verification of the <strong>TaskFlow</strong> full-stack application. The codebase was forked from the instructor repository <code>atindeRR/MSE-2-SSED-Morning</code> into the personal account <code>{github_username}</code> and cloned locally for development.
</p>

{img_tag("01-github/github-fork.jpg", "GitHub Forked Starter Repository on Personal Account", 1)}

{img_tag("01-github/project-structure-vscode.png", "Project Workspace Structure in VS Code", 2)}

<div class="page-break"></div>

<!-- SECTION 2: ARCHITECTURE & DOCKERFILES -->
<h2 class="section-title">2. Architecture &amp; Dockerfile Implementations</h2>
<p>
The application comprises four tiers communicating over an isolated bridge network:
</p>
<ul>
  <li><strong>Frontend (React + Vite + Nginx):</strong> Implemented with a multi-stage Dockerfile (<code>node:22-alpine</code> builder + <code>nginx:alpine</code> runner) proxying <code>/api/</code> and <code>/health</code> internally to <code>http://backend:3000</code>.</li>
  <li><strong>Backend (Node.js + Express ESM):</strong> Production container running <code>node:22-alpine</code> with <code>npm ci --omit=dev</code>, connecting to PostgreSQL and Redis via Docker internal DNS.</li>
</ul>

{img_tag("02-docker/frontend-dockerfile.png", "Multi-Stage Nginx Frontend Dockerfile (Hadolint Clean)", 3)}

{img_tag("02-docker/backend-dockerfile.png", "Production Backend Dockerfile (Hadolint Clean)", 4)}

<div class="page-break"></div>

<!-- SECTION 3: MULTI-CONTAINER ORCHESTRATION -->
<h2 class="section-title">3. Docker Compose Orchestration (Local Development)</h2>
<p>
The multi-container configuration in <code>docker-compose.yml</code> connects the four services via <code>taskflow-network</code>, mounts the persistent volume <code>postgres-data</code> for relational storage, mounts <code>init.sql</code> for database schema seeding, and configures health dependencies:
</p>

{img_tag("02-docker/docker-desktop-containers.png", "Docker Desktop Showing All 4 Active Containers Running", 5)}

{img_tag("02-docker/docker-compose-ps-terminal.png", "Terminal Verification of Service Status & Host Port Bindings", 6)}

<div class="page-break"></div>

<!-- SECTION 4: DOCKER HUB PUBLISHING -->
<h2 class="section-title">4. Docker Hub Image Publishing</h2>
<p>
Production images were compiled, tagged, and published to the public Docker Hub registry under namespace <code>{dockerhub_username}</code>:
</p>
<ul>
  <li><strong>Frontend Image:</strong> <code>{dockerhub_username}/frontend:latest</code> &mdash; <a href="{frontend_img_url}">{frontend_img_url}</a></li>
  <li><strong>Backend Image:</strong> <code>{dockerhub_username}/backend:latest</code> &mdash; <a href="{backend_img_url}">{backend_img_url}</a></li>
</ul>

{img_tag("03-dockerhub/dockerhub-repositories.png", "Docker Hub Dashboard Displaying Published Repositories", 7)}

{img_tag("03-dockerhub/dockerhub-frontend-tag.jpg", "Docker Hub Frontend Repository Showing Verified latest Tag", 8)}

<div class="page-break"></div>

<!-- SECTION 5: DEPLOYMENT COMPOSE & TESTING -->
<h2 class="section-title">5. Production Deployment (docker-compose.deploy.yml)</h2>
<p>
To ensure deployment on any clean server without rebuilding locally, <code>docker-compose.deploy.yml</code> eliminates all local <code>build:</code> directives and exclusively pulls the published registry images:
</p>

{img_tag("04-deployment/image-pull.png", "Pulling Published Registry Images from Docker Hub", 9)}

{img_tag("04-deployment/taskflow-browser-login.jpg", "TaskFlow Web Application Running at http://localhost:8080", 10)}

<h2 class="section-title">6. Automated Integration Testing</h2>
<p>
All 12 automated API integration tests in <code>tests/api.test.js</code> passed with 100% success rate:
</p>

{img_tag("04-deployment/test-results.png", "Jest Test Suite Execution &mdash; All 12 Test Cases Passed (100%)", 11)}

<div class="page-break"></div>

<!-- SECTION 7: CI/CD & PR -->
<h2 class="section-title">7. GitHub Actions CI/CD Implementation</h2>
<p>
The repository contains automated pipelines in <code>.github/workflows/</code>:
</p>
<ul>
  <li><strong>CI Pipeline (<code>ci.yml</code>):</strong> Validates Dockerfiles against Hadolint, runs Compose build, launches services, verifies health, executes Jest integration tests, and runs persistence validation.</li>
  <li><strong>CD Pipeline (<code>cd.yml</code>):</strong> Authenticates with Docker Hub via repository secrets (<code>DOCKERHUB_USERNAME</code>, <code>DOCKERHUB_TOKEN</code>, <code>POSTGRES_PASSWORD</code>), builds and publishes production tags, verifies <code>docker-compose.deploy.yml</code>, and performs deployment verification.</li>
</ul>

<h2 class="section-title">8. Practical Implementation Checklist</h2>
<ul class="checklist">
  <li>Frontend multi-stage Dockerfile implemented and Hadolint-verified</li>
  <li>Backend production Dockerfile implemented and Hadolint-verified</li>
  <li><code>docker-compose.yml</code> multi-service specification created and tested</li>
  <li><code>docker-compose.deploy.yml</code> created using published images without build directives</li>
  <li>Frontend image published to Docker Hub (<code>{dockerhub_username}/frontend:latest</code>)</li>
  <li>Backend image published to Docker Hub (<code>{dockerhub_username}/backend:latest</code>)</li>
  <li>PostgreSQL persistent storage verified across container lifecycles</li>
  <li>Redis caching verified with automatic cache eviction on task mutations</li>
  <li>Complete 12-test integration suite passing successfully</li>
  <li>Clean git commit pushed to GitHub fork <code>main</code> branch</li>
</ul>

<h2 class="section-title">9. Mandatory Academic Declaration</h2>
<div class="declaration-box">
  "I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."
</div>

<table style="width: 100%; margin-top: 40px;">
  <tr>
    <td style="width: 60%;">
      <strong>Candidate Signature:</strong> ____________________________<br/>
      <strong>Date:</strong> 18 November 2026
    </td>
    <td style="width: 40%; text-align: right;">
      <strong>Faculty Evaluator:</strong> ____________________________<br/>
      <strong>Status:</strong> [ Verified &amp; Accepted ]
    </td>
  </tr>
</table>

</body>
</html>"""

    html_file = r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION\report_temp.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
        
    pdf_path = os.path.join(r"C:\Users\DELL\MSE-2-SSED-Morning\MSE-2-SUBMISSION", pdf_filename)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    temp_dir = r"C:\Users\DELL\AppData\Local\Temp\chrome_temp"
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={temp_dir}",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        f"file:///{html_file.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(html_file):
        os.remove(html_file)
    print(f"SUCCESS: Report compiled to {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Ayush Pandey"
    roll = sys.argv[2] if len(sys.argv) > 2 else "230101"
    sec = sys.argv[3] if len(sys.argv) > 3 else "AIML-B"
    branch = sys.argv[4] if len(sys.argv) > 4 else "CSE (AIML)"
    user = "ayushpandeyap975"
    hub = "ayushpandeyap975"
    filename = f"{roll}_{name.replace(' ', '_')}.pdf"
    build_report(name, roll, sec, branch, user, hub, filename)
