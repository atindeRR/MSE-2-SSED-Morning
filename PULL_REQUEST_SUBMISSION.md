## Student Details

- Name: Manu Garg
- Roll Number: 2400291520149
- Section: CSE-AI-C
- GitHub Username: mg8273
- Docker Hub Username: mg8273

## Docker Hub Images

- Frontend Image: https://hub.docker.com/r/mg8273/frontend (`mg8273/frontend:latest`)
- Backend Image: https://hub.docker.com/r/mg8273/backend (`mg8273/backend:latest`)

## Application Deployment

- Application URL: http://localhost:8080 (local deployment)
- Backend Health URL: http://localhost:3000/health (local deployment)
- GitHub-hosted CD deployment is temporary and cleaned up after verification.

## Implementation Checklist

- [x] Frontend Dockerfile implemented
- [x] Backend Dockerfile implemented
- [x] docker-compose.yml implemented
- [x] docker-compose.deploy.yml implemented
- [x] Frontend image published to Docker Hub
- [x] Backend image published to Docker Hub
- [x] PostgreSQL persistence verified
- [x] Redis caching verified
- [x] Application functionality tested
- [x] CD pipeline passed successfully
- [x] Latest changes committed and pushed

## CI/CD Verification

- CD Workflow Run URL: https://github.com/mg8273/MSE-2-SSED-Morning/actions/runs/44240555155
- Final Workflow Status: success
- Fork CI: https://github.com/mg8273/MSE-2-SSED-Morning/actions/runs/44240512562 (success)
- Local API evaluation: 12/12 supplied tests passed.
- Instructor CI: awaiting approval from a maintainer ([run](https://github.com/atindeRR/MSE-2-SSED-Morning/actions/runs/44241273241)).
- Instructor-controlled CI references two scripts absent from the instructor's
  current main branch; the supplied CI workflow is preserved unchanged.

## Documentation

- PDF: [2400291520149_Manu_Garg.pdf](https://github.com/mg8273/MSE-2-SSED-Morning/blob/main/evidence/2400291520149_Manu_Garg.pdf)
- Genuine CI/CD screenshots and job metadata/logs are included under `evidence/`.
- Both public images provide AMD64 and ARM64 variants. Published-image deployment was also verified on Apple Silicon without local builds.
- Submission checklist: SUBMISSION_CHECKLIST.md

## Declaration

I confirm that the implementation submitted is my own work and that I have tested the containerized application.
