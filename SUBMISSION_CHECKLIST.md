# Morning-shift submission checklist

## Identity

- Name: Manu Garg
- Roll number: 2400291520149
- Section: CSE-AI-C
- Branch: CSE (Artificial Intelligence)
- GitHub / Docker Hub username: mg8273
- Personal fork: https://github.com/mg8273/MSE-2-SSED-Morning
- Submission branch: main

## Files to include in your fork

- frontend/Dockerfile and frontend/.dockerignore
- backend/Dockerfile and backend/.dockerignore
- frontend/package-lock.json and backend/package-lock.json
- frontend/nginx.conf (production proxy configuration)
- docker-compose.yml (four services built locally)
- docker-compose.deploy.yml (published images; no build directives)
- .env.example with placeholders only; .env must remain untracked
- .github/workflows/cd.yml, provided CI, submission.json, supporting scripts
- PDF documentation and evidence screenshots

## Required remote steps

- [x] Both public Docker Hub repositories contain the submitted images.
- [x] Published images can be pulled and deployed without local builds.
- [x] Latest main-branch CD run passes all required stages.
- [x] Latest implementation is committed and pushed to the personal fork.
- [ ] Final pull request is created against the instructor's actual repository.
- [ ] PDF is attached/linked in the PR and uploaded to Moodle.

## Mandatory PDF

Filename: `2400291520149_Manu_Garg.pdf`

Include full name, university roll number, section, branch, GitHub username,
fork URL, implementation branch, Docker Hub username and image URLs:

- https://hub.docker.com/r/mg8273/frontend
- https://hub.docker.com/r/mg8273/backend

Include readable genuine screenshots covering ALL of:

1. GitHub Actions workflow execution and final success status.
2. Docker Hub authentication stage (never reveal credentials).
3. Backend image build AND publishing.
4. Frontend image build AND publishing.
5. Docker Compose image pull.
6. Application deployment.
7. Backend health check.
8. Frontend accessibility verification.
9. Instructor CI evaluation results, if available.

Additional useful evidence: Docker Hub image/tag pages, all four containers
healthy, registration/login/task operations, Redis cache hit, and PostgreSQL
persistence after down/up. Local screenshots do not replace CI/CD screenshots.

Required declaration (include only when accurate and after reviewing the work):

> I hereby declare that the submitted Docker implementation is my own work.
> I have successfully executed and verified the required CI/CD pipeline stages,
> published the Docker images to my Docker Hub account, and tested the
> application deployment.

## Pull request

Title: `DOCKER-EXAM | 2400291520149 | Manu Garg | CSE-AI-C`

Use `PULL_REQUEST_SUBMISSION.md` for the body. Fill the successful workflow URL,
final status and PDF link using actual results. Do not mark unfinished steps
complete. The paper has a repository-name inconsistency; the actual fork parent
is `atindeRR/MSE-2-SSED-Morning`, main.

The paper requires Moodle submission. This workspace has no Moodle connection;
the final PDF must also be uploaded there by you.
