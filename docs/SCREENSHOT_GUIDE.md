# Screenshot Capture Plan

## Working method

- Project root for every local command: **`D:\DEVOPS\mse2`**.
- Save actual PNG screenshots in **`evidence/screenshots/`**.
- Screenshot collection is user-managed. Implementation and routine verification
  can continue through verified phases; pause only for necessary account details
  or external confirmation.
- Use a fresh PowerShell terminal or press **Ctrl+L** before an evidence command.
  Enlarge the panel so the command and its important result remain readable.
- In VS Code, enable word wrap with **Alt+Z** when displaying long Docker lines.
- Capture using **Win+Shift+S**. Include the command/directory or browser URL and
  the relevant result. Keep the original image; do not fabricate or edit success
  indicators into it.
- Do not display `.env` contents, passwords, access tokens, JWTs, or registry
  authentication files. GitHub secret names and masked login logs are sufficient.
- Use `docker compose config --quiet` for validation without printing resolved
  environment secrets.
- Compose commands below become applicable after their respective Compose files
  have been implemented. Docker Hub usernames and run/PR URLs must be replaced
  with actual verified values when those phases are reached.

On this computer, Oracle Database occupies host port 8080. The final local
frontend mapping will therefore use **8081**, while CI continues to use its
source-defined host port **8080**. Follow the actual port shown by Compose when
capturing local browser and HTTP evidence.

**Evidence status:** this file is a capture plan. No required screenshot has
been marked captured or verified by creating this document.

## Required implementation screenshots

### 01 - Project structure
- Open: VS Code Explorer at the project root, after both Compose files exist.
- Command: none; expand `frontend`, `backend`, `.github/workflows`, and `docs`.
- Visible: both Dockerfiles, both Compose files, Nginx configuration, and source
  directories. Keep sensitive file contents closed.
- Proves: required containerization files are in the submitted project.
- Caption: **Screenshot 1. TaskFlow repository structure and Docker deliverables.**
- PDF section: 8, Repository Structure.
- Save as: `01-project-structure.png`.

### 02 - Frontend Dockerfile
- Open: `frontend/Dockerfile` in VS Code, with word wrap if necessary.
- Command: none.
- Visible: complete build stage, dependency installation, Vite build, Nginx
  runtime stage, port, health check, and startup command.
- Proves: the React production build is served by a separate Nginx runtime.
- Caption: **Screenshot 2. Multi-stage React/Vite frontend Dockerfile.**
- PDF section: 9, Frontend Dockerization.
- Save as: `02-frontend-dockerfile.png`.

### 03 - Backend Dockerfile
- Open: `backend/Dockerfile` in VS Code.
- Command: none.
- Visible: Node base, production dependencies, source copy, non-root user,
  actual port, existing health probe, and startup command.
- Proves: the existing Express application has a production runtime image.
- Caption: **Screenshot 3. Node.js/Express backend Dockerfile.**
- PDF section: 10, Backend Dockerization.
- Save as: `03-backend-dockerfile.png`.

### 04 - Four-service Compose configuration
- Open: `docker-compose.yml` in VS Code.
- Command: none; use two readable captures if the entire file does not fit.
- Visible: `frontend`, `backend`, `postgres`, and `redis`, plus dependencies,
  environment-variable references, network, and PostgreSQL volume.
- Proves: all four services are orchestrated with internal service-name routing.
- Caption: **Screenshot 4. Four-service Docker Compose configuration.**
- PDF section: 11, Docker Compose Implementation.
- Save as: `04-compose-services.png` and, if needed, `04b-compose-storage.png`.

### 05 - Successful application image builds
- Open: clean PowerShell terminals at the project root at the build checkpoints.
- Commands: `docker build --progress=plain -t taskflow-frontend:local ./frontend`
  and, at the backend phase, `docker build --progress=plain -t taskflow-backend:local ./backend`.
- Visible: successful build steps, final image name, and final `DONE` results.
- Proves: both application images build successfully from the submitted files.
- Caption: **Screenshot 5a. Successful frontend image build.** / **Screenshot
  5b. Successful backend image build.**
- PDF section: 9/10, Dockerization; summarize in 16, Testing and Results.
- Save as: `05a-frontend-build.png` and `05b-backend-build.png`.

### 06 - All four services running
- Open: clean PowerShell after Compose startup and health verification.
- Command: `docker compose ps`.
- Visible: all four service rows, their running/healthy status, and host ports.
- Proves: the complete local Compose stack is running.
- Caption: **Screenshot 6. All four TaskFlow containers running and healthy.**
- PDF section: 12, Container Verification.
- Save as: `06-compose-ps.png`.

### 07 - PostgreSQL readiness
- Open: clean PowerShell with the stack running.
- Command: `docker compose exec -T postgres sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'`.
- Visible: the actual `accepting connections` result.
- Proves: PostgreSQL is accepting connections with the configured database/user.
- Caption: **Screenshot 7. PostgreSQL connection-readiness verification.**
- PDF section: 12, Container Verification.
- Save as: `07-postgres-health.png`.

### 08 - Redis readiness
- Open: clean PowerShell with the stack running.
- Command: `docker compose exec -T redis redis-cli ping`.
- Visible: `PONG`.
- Proves: Redis is responding to commands. Application caching is additionally
  verified through repeated task reads, not by PING alone.
- Caption: **Screenshot 8. Redis responds successfully to PING.**
- PDF section: 12, Container Verification.
- Save as: `08-redis-health.png`.

### 09 - Working browser application
- Open: `http://localhost:8080/` after full-stack verification.
- Command: none; register/login, create a task, change its status, and refresh.
- Visible: TaskFlow, a real saved task, the browser address, and optionally the
  `redis-cache` response-source indicator after repeated refreshes.
- Proves: browser-to-Nginx-to-API communication and real application functionality.
- Caption: **Screenshot 9. TaskFlow running through the containerized frontend.**
- PDF section: 16, Testing and Results.
- Save as: `09-application-browser.png`.

### 10 - Existing backend health endpoint
- Open: clean PowerShell or `http://localhost:3000/health` in a browser.
- Command: `curl.exe --fail --silent --show-error http://localhost:3000/health`.
- Visible: actual JSON with `status`, `postgres`, and `redis` equal to `ok`.
- Proves: the API can query PostgreSQL and communicate with Redis.
- Caption: **Screenshot 10. Backend health confirms PostgreSQL and Redis connectivity.**
- PDF section: 12, Container Verification.
- Save as: `10-backend-health.png`.

### 11 - Published frontend repository
- Open: `https://hub.docker.com/r/<DOCKERHUB_USERNAME>/frontend/tags`.
- Command: none; refresh after the real push succeeds.
- Visible: personal repository name, `latest` tag, and digest/publication details.
- Proves: the frontend image exists in the user's Docker Hub repository.
- Caption: **Screenshot 11. Frontend image published on Docker Hub.**
- PDF section: 13, Docker Hub Image Publishing.
- Save as: `11-dockerhub-frontend.png`.

### 12 - Published backend repository
- Open: `https://hub.docker.com/r/<DOCKERHUB_USERNAME>/backend/tags`.
- Command: none; refresh after the real push succeeds.
- Visible: personal repository name, `latest` tag, and digest/publication details.
- Proves: the backend image exists in the user's Docker Hub repository.
- Caption: **Screenshot 12. Backend image published on Docker Hub.**
- PDF section: 13, Docker Hub Image Publishing.
- Save as: `12-dockerhub-backend.png`.

### 13 - Image-only deployment Compose
- Open: `docker-compose.deploy.yml` in VS Code.
- Command: none; capture the full file in readable parts if necessary.
- Visible: published frontend/backend image references, official database/cache
  images, health checks, and persistent storage. There must be no build directives.
- Proves: deployment uses prebuilt registry images rather than local builds.
- Caption: **Screenshot 13. Published-image deployment Compose configuration.**
- PDF section: 14, Published Image Deployment.
- Save as: `13-deploy-compose.png` and, if needed, `13b-deploy-storage.png`.

### 14 - Deployment from published images
- Open: clean PowerShell after the image-only deployment checkpoint.
- Commands: `docker compose -f docker-compose.deploy.yml pull`,
  `docker compose -f docker-compose.deploy.yml up -d`, then
  `docker compose -f docker-compose.deploy.yml ps`.
- Visible: successful pulls and all four running/healthy services. Capture the
  pull and final status separately if needed, and verify both HTTP URLs afterward.
- Proves: published images can be pulled and used for a working deployment.
- Caption: **Screenshot 14. Successful deployment using Docker Hub images.**
- PDF section: 14, Published Image Deployment.
- Save as: `14a-deployment-pull.png` and `14b-deployment-status.png`.

## Required GitHub Actions screenshots

Use your fork's Actions page:
https://github.com/adidev001/MSE-2-SSED-Morning/actions

For CD, open the actual run of **Docker Practical - Publish and Verify** for the
submitted commit. Capture the run URL and final status. Use expanded successful
step logs for detailed evidence. Final step labels must match the implemented
workflow; health/accessibility verification will be made explicit in Phase 8.

### 15 - Required repository secrets
- Open: Repository -> Settings -> Secrets and variables -> Actions.
- Command: none.
- Visible: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, and `POSTGRES_PASSWORD`
  names. Do not open value-entry forms while capturing.
- Proves: the required secret names are configured without exposing credentials.
- Caption: **Screenshot 15. Required GitHub Actions repository secrets configured.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `15-github-secrets.png`.

### 16 - CI/CD backend build and publication
- Open: actual successful CD run -> expand **Build and push backend**.
- Command: none; inspect actual step logs.
- Visible: green step status, backend image export/push completion, and image
  digest/tag information when available.
- Proves: GitHub Actions built and published the backend image.
- Caption: **Screenshot 16. Successful backend image build and publishing in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `16-actions-backend-build-push.png`.

### 17 - CI/CD frontend build and publication
- Open: same successful CD run -> expand **Build and push frontend**.
- Command: none; inspect actual step logs.
- Visible: green step status, frontend image export/push completion, and image
  digest/tag information when available.
- Proves: GitHub Actions built and published the frontend image.
- Caption: **Screenshot 17. Successful frontend image build and publishing in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `17-actions-frontend-build-push.png`.

### 18 - Deployment and verification stages
- Open: same CD run's job step list.
- Command: none.
- Visible: successful published-image pull, application deployment, backend
  health, frontend accessibility, and API test stages.
- Proves: the publication stages connect to actual deployment and testing.
- Caption: **Screenshot 18. GitHub Actions deployment and verification stages.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `18-actions-deployment-stages.png`.

### 19 - Complete successful workflow
- Open: CD run summary for the final submitted commit.
- Command: none.
- Visible: workflow name, commit/branch, run URL, green job, and final **Success**
  status. The required stages must not be failed or skipped.
- Proves: the complete CD workflow passed for the recorded commit.
- Caption: **Screenshot 19. Complete successful TaskFlow CD workflow execution.**
- PDF section: 15, GitHub Actions CI/CD; summarize in 16, Testing and Results.
- Save as: `19-actions-success.png`.

### 20 - Final pull request
- Open: the actual PR, after its instructor target has been confirmed.
- Command: none.
- Visible: PR URL, required title, correct base/head repositories, student
  details, image links, implementation checklist, and CD run link.
- Proves: the final implementation was submitted through the correct PR.
- Caption: **Screenshot 20. Final Docker practical submission pull request.**
- PDF section: 17, GitHub Pull Request.
- Save as: `20-final-pull-request.png`.

### 21 - Instructor CI evaluation (if available)
- Open: the final PR's Checks page and instructor evaluation run.
- Command: none; inspect the actual evaluation results and logs.
- Visible: actual status, evaluated commit, API/cache tests, and persistence
  verification. Record a failure accurately rather than presenting it as success.
- Proves: the instructor-controlled evaluation result for the submission.
- Caption: **Screenshot 21. Instructor CI evaluation result for the submitted commit.**
- PDF section: 16, Testing and Results, and 17, GitHub Pull Request.
- Save as: `21-instructor-ci.png`. If unavailable, explicitly document that fact.

## Additional detailed CI/CD evidence requested

Capture the following in the CI/CD PDF section alongside screenshots 16-19 so
authentication, pull, deployment, and individual HTTP checks are readable.

### 22 - Docker Hub authentication in CI/CD
- Open: successful CD run -> expand **Login to Docker Hub**.
- Command: none; inspect the masked action logs.
- Visible: green login step and actual successful login output when present.
- Proves: the runner authenticated to Docker Hub successfully.
- Caption: **Screenshot 22. Successful Docker Hub authentication with masked credentials.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `22-actions-dockerhub-login.png`.

### 23 - Docker Compose image pull in CI/CD
- Open: successful CD run -> expand **Pull published images**.
- Command executed by the workflow: `docker compose -f docker-compose.deploy.yml pull`.
- Visible: successful pull results for application and infrastructure images.
- Proves: the runner downloaded published images for deployment.
- Caption: **Screenshot 23. Successful Docker Compose image pull in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `23-actions-image-pull.png`.

### 24 - Application deployment in CI/CD
- Open: successful CD run -> expand **Deploy using Docker Hub images**.
- Command executed by the workflow: `docker compose -f docker-compose.deploy.yml up -d`.
- Visible: actual service creation/startup results and green deployment step.
- Proves: the runner started the application using the image-only Compose file.
- Caption: **Screenshot 24. Successful application deployment in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `24-actions-application-deployment.png`.

### 25 - Backend health in CI/CD
- Open: successful CD run -> expand its backend-health verification step.
- HTTP request performed by the workflow: `curl --fail --silent http://localhost:3000/health`.
- Visible: actual health JSON confirming `status`, `postgres`, and `redis` as
  `ok`, with the successful step result.
- Proves: the deployed backend reaches PostgreSQL and Redis on the runner.
- Caption: **Screenshot 25. Successful backend health verification in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `25-actions-backend-health.png`.

### 26 - Frontend accessibility in CI/CD
- Open: successful CD run -> expand its frontend-accessibility verification step.
- HTTP request performed by the workflow: `curl --fail --silent http://localhost:8080/`.
- Visible: actual successful HTTP verification output and green step status.
- Proves: the deployed Nginx frontend responds on the runner's host port 8080.
- Caption: **Screenshot 26. Successful frontend accessibility verification in GitHub Actions.**
- PDF section: 15, GitHub Actions CI/CD.
- Save as: `26-actions-frontend-accessibility.png`.

## Additional functionality evidence

Collect a screenshot of the browser's `redis-cache` indicator after repeated
task reads and a before/after screenshot of a saved task across container
recreation. These support Redis caching and PostgreSQL persistence claims;
healthy containers alone do not prove those application behaviors.

## Final PDF order

1. Cover Page
2. Student Information
3. Project Abstract
4. Problem Statement
5. Project Objectives
6. Technology Stack
7. System Architecture
8. Repository Structure
9. Frontend Dockerization
10. Backend Dockerization
11. Docker Compose Implementation
12. Container Verification
13. Docker Hub Image Publishing
14. Published Image Deployment
15. GitHub Actions CI/CD
16. Testing and Results
17. GitHub Pull Request
18. Screenshots and Evidence (evidence index and any additional captures)
19. Conclusion
20. Declaration

Place each actual screenshot beside its technical explanation in the relevant
section, with its number, descriptive heading, caption, and verified result.
Include real fork/image/run/PR URLs and the actual final workflow status.

The final filename must be **`ROLL_NUMBER_STUDENT_NAME.pdf`**, using the student's
confirmed roll number and name. Generate the final PDF only after the required
evidence and results have been collected.
