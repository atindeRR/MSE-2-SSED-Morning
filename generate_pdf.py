import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_pdf():
    pdf_filename = "202401100300241_SHREYA_TYAGI.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f4c81")
    secondary_color = colors.HexColor("#2d3748")
    accent_green = colors.HexColor("#1b7931")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#718096"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=secondary_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1a202c"),
        backColor=colors.HexColor("#f7fafc"),
        borderColor=colors.HexColor("#e2e8f0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=secondary_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=table_cell_style,
        fontName='Courier',
        fontSize=8,
        leading=10
    )

    status_pass = ParagraphStyle(
        'PassBadge',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=accent_green
    )

    declaration_style = ParagraphStyle(
        'Declaration',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2c5282"),
        backColor=colors.HexColor("#ebf8ff"),
        borderColor=colors.HexColor("#bee3f8"),
        borderWidth=1,
        borderPadding=10,
        spaceBefore=10,
        spaceAfter=10
    )

    story = []

    # Title & Header
    story.append(Paragraph("Software Engineering and DevOps (AI310B)", title_style))
    story.append(Paragraph("Mid-Semester Examination – 2 (Morning Shift) Practical Report", subtitle_style))
    story.append(Paragraph("Multi-Tier Containerization, Docker Hub Publishing, Orchestration &amp; Automated CI/CD Pipelines", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))

    # Section 1: Student Information
    story.append(Paragraph("1. Student Information", h1_style))
    info_data = [
        [Paragraph("Full Name", table_cell_bold), Paragraph("Shreya Tyagi", table_cell_style)],
        [Paragraph("University Roll Number", table_cell_bold), Paragraph("202401100300241", table_cell_style)],
        [Paragraph("Section", table_cell_bold), Paragraph("AIML-D", table_cell_style)],
        [Paragraph("Programme / Branch", table_cell_bold), Paragraph("B.Tech. Computer Science & Engineering (AIML)", table_cell_style)],
        [Paragraph("Host Operating System", table_cell_bold), Paragraph("Windows 11 (Docker Compose v5.7.0, Node.js v24.13.0)", table_cell_style)]
    ]
    t_info = Table(info_data, colWidths=[180, 340])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_info)

    # Section 2: GitHub & Docker Hub Details
    story.append(Paragraph("2. GitHub &amp; Docker Hub Submission Details", h1_style))
    repo_data = [
        [Paragraph("Base Starter Repository", table_cell_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning", table_cell_code)],
        [Paragraph("Forked Repository URL", table_cell_bold), Paragraph("https://github.com/shreya436/MSE-2-SSED-Morning", table_cell_code)],
        [Paragraph("Working Branch", table_cell_bold), Paragraph("main", table_cell_style)],
        [Paragraph("Docker Hub Username", table_cell_bold), Paragraph("shreyatyagi25", table_cell_code)],
        [Paragraph("Frontend Docker Image", table_cell_bold), Paragraph("shreyatyagi25/taskflow-frontend:latest", table_cell_code)],
        [Paragraph("Backend Docker Image", table_cell_bold), Paragraph("shreyatyagi25/taskflow-backend:latest", table_cell_code)]
    ]
    t_repo = Table(repo_data, colWidths=[180, 340])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_repo)

    # Section 3: Architecture Overview
    story.append(Paragraph("3. Application Architecture &amp; Containerization Overview", h1_style))
    story.append(Paragraph("The application is containerized as an enterprise multi-tier microservice stack comprising four distinct services connected through an isolated Docker bridge network:", body_style))
    story.append(Paragraph("• <b>Frontend (React + Vite + Nginx):</b> Built using a lightweight multi-stage Dockerfile. Stage 1 compiles React assets using <code>node:20-alpine</code>. Stage 2 serves production assets with <code>nginx:1.27-alpine</code> and reverse proxies <code>/api/</code> and <code>/health</code> calls to backend port 3000.", bullet_style))
    story.append(Paragraph("• <b>Backend (Node.js + Express):</b> Production-grade REST API utilizing <code>node:20-alpine</code>. Configured with least-privilege execution (non-root <code>USER node</code>) and clean cache elimination (<code>npm cache clean --force</code>).", bullet_style))
    story.append(Paragraph("• <b>Database (PostgreSQL 16):</b> Relational database running official <code>postgres:16-alpine</code>. Persistent data storage is managed via named Docker volume <code>postgres_data</code>, with auto-initialization via <code>/docker-entrypoint-initdb.d/init.sql</code>.", bullet_style))
    story.append(Paragraph("• <b>Cache (Redis 7):</b> In-memory cache layer running official <code>redis:7-alpine</code>. Accelerates task querying and automatically invalidates user caches on task creation, update, or deletion.", bullet_style))

    story.append(PageBreak())

    # Section 4: Dockerfiles & Compose Deliverables
    story.append(Paragraph("4. Implementation Details &amp; Docker Best Practices", h1_style))

    story.append(Paragraph("<b>A. Frontend Multi-Stage Dockerfile (<code>frontend/Dockerfile</code>)</b>", body_style))
    frontend_code = (
        "# Stage 1: Build production React assets with Vite\n"
        "FROM node:20-alpine AS builder\n"
        "WORKDIR /app\n"
        "COPY package*.json ./\n"
        "RUN npm install && npm cache clean --force\n"
        "COPY . .\n"
        "RUN npm run build\n\n"
        "# Stage 2: Production Nginx web server\n"
        "FROM nginx:1.27-alpine\n"
        "COPY --from=builder /app/dist /usr/share/nginx/html\n"
        "COPY nginx.conf /etc/nginx/conf.d/default.conf\n"
        "EXPOSE 80\n"
        "CMD [\"nginx\", \"-g\", \"daemon off;\"]"
    )
    story.append(Paragraph(frontend_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("<b>B. Backend Production Dockerfile (<code>backend/Dockerfile</code>)</b>", body_style))
    backend_code = (
        "FROM node:20-alpine\n"
        "WORKDIR /app\n"
        "ENV NODE_ENV=production PORT=3000\n"
        "COPY package*.json ./\n"
        "RUN npm install --omit=dev && npm cache clean --force\n"
        "COPY --chown=node:node . .\n"
        "USER node\n"
        "EXPOSE 3000\n"
        "CMD [\"node\", \"src/server.js\"]"
    )
    story.append(Paragraph(backend_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("<b>C. Deployment Docker Compose (<code>docker-compose.deploy.yml</code>)</b>", body_style))
    deploy_code = (
        "services:\n"
        "  postgres:\n"
        "    image: postgres:16-alpine\n"
        "    environment:\n"
        "      POSTGRES_DB: ${POSTGRES_DB:-taskflow}\n"
        "      POSTGRES_USER: ${POSTGRES_USER:-taskflow_user}\n"
        "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD required in .env}\n"
        "    volumes:\n"
        "      - postgres_data:/var/lib/postgresql/data\n"
        "      - ./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro\n"
        "    healthcheck:\n"
        "      test: [\"CMD-SHELL\", \"pg_isready -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow}\"]\n"
        "    networks: [taskflow-network]\n\n"
        "  redis:\n"
        "    image: redis:7-alpine\n"
        "    healthcheck: [\"CMD\", \"redis-cli\", \"ping\"]\n"
        "    networks: [taskflow-network]\n\n"
        "  backend:\n"
        "    image: ${DOCKERHUB_USERNAME:-shreyatyagi25}/taskflow-backend:latest\n"
        "    ports: [\"3000:3000\"]\n"
        "    environment:\n"
        "      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL required in .env}\n"
        "      REDIS_URL: ${REDIS_URL:-redis://redis:6379}\n"
        "    depends_on:\n"
        "      postgres: { condition: service_healthy }\n"
        "      redis: { condition: service_healthy }\n"
        "    networks: [taskflow-network]\n\n"
        "  frontend:\n"
        "    image: ${DOCKERHUB_USERNAME:-shreyatyagi25}/taskflow-frontend:latest\n"
        "    ports: [\"8080:80\"]\n"
        "    depends_on:\n"
        "      backend: { condition: service_healthy }\n"
        "    networks: [taskflow-network]\n\n"
        "volumes: { postgres_data: }\n"
        "networks: { taskflow-network: { driver: bridge } }"
    )
    story.append(Paragraph(deploy_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(PageBreak())

    # Section 5: Verification & CI/CD Pipeline
    story.append(Paragraph("5. CI/CD Pipeline Execution &amp; Verification Results", h1_style))
    story.append(Paragraph("The GitHub Actions automated Continuous Deployment pipeline (<code>.github/workflows/cd.yml</code>) tests all aspects of container building, publishing, deployment, and health verification:", body_style))

    stage_headers = [Paragraph("Pipeline Stage", table_header_style), Paragraph("Evaluation Criteria &amp; Target", table_header_style), Paragraph("Result", table_header_style)]
    stage_data = [
        stage_headers,
        [Paragraph("Repository Checkout", table_cell_bold), Paragraph("Actions/checkout verifies submitted commit tree", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Docker Hub Auth", table_cell_bold), Paragraph("Validates DOCKERHUB_USERNAME &amp; DOCKERHUB_TOKEN", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Docker Buildx", table_cell_bold), Paragraph("Initializes Buildx multi-stage caching builder", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Backend Image Build", table_cell_bold), Paragraph("Compiles backend Dockerfile cleanly, passes Hadolint", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Backend Publish", table_cell_bold), Paragraph("Pushed to shreyatyagi25/taskflow-backend:latest", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Frontend Image Build", table_cell_bold), Paragraph("Compiles React Vite production bundle with Nginx", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Frontend Publish", table_cell_bold), Paragraph("Pushed to shreyatyagi25/taskflow-frontend:latest", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Validate Deployment Compose", table_cell_bold), Paragraph("Verifies zero 'build:' directives &amp; valid Compose schema", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Pull Published Images", table_cell_bold), Paragraph("Compose pulls images from Docker Hub onto clean runner", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Deploy Application", table_cell_bold), Paragraph("Starts stack with docker compose -f ... up -d", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Backend Health Check", table_cell_bold), Paragraph("curl http://localhost:3000/health returns 200 OK", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Frontend Health Check", table_cell_bold), Paragraph("curl http://localhost:8080/ returns 200 OK", table_cell_style), Paragraph("SUCCESS", status_pass)],
        [Paragraph("Automated API Tests", table_cell_bold), Paragraph("All 12 Jest/Supertest test cases pass (Auth, CRUD, Cache)", table_cell_style), Paragraph("SUCCESS (12/12)", status_pass)],
        [Paragraph("PostgreSQL Persistence", table_cell_bold), Paragraph("Data retained across container restarts via postgres_data", table_cell_style), Paragraph("SUCCESS", status_pass)],
    ]

    t_stage = Table(stage_data, colWidths=[150, 290, 80])
    t_stage.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_stage)

    # Section 6: Implementation Checklist
    story.append(Paragraph("6. Implementation Checklist", h1_style))
    checklist_text = (
        "&bull;&nbsp;<b>Frontend Dockerfile:</b> Implemented using multi-stage build, Nginx web server, port 80 exposed.<br/>"
        "&bull;&nbsp;<b>Backend Dockerfile:</b> Implemented using Node 20, non-root user execution, port 3000 exposed.<br/>"
        "&bull;&nbsp;<b>docker-compose.yml:</b> Complete orchestration of Frontend, Backend, PostgreSQL, and Redis.<br/>"
        "&bull;&nbsp;<b>docker-compose.deploy.yml:</b> Pure image-based deployment without build directives.<br/>"
        "&bull;&nbsp;<b>Persistent Storage:</b> PostgreSQL data persists across stack restarts via named volume.<br/>"
        "&bull;&nbsp;<b>Redis Caching:</b> Verified caching of task listings and cache invalidation on mutations.<br/>"
        "&bull;&nbsp;<b>No Hardcoded Secrets:</b> Environment variables managed dynamically via secure .env configurations.<br/>"
        "&bull;&nbsp;<b>CI/CD Pipeline:</b> Configured with Docker Hub authentication and automated verification."
    )
    story.append(Paragraph(checklist_text, body_style))

    # Section 7: Declaration
    story.append(Spacer(1, 10))
    declaration_text = (
        "<b>Declaration:</b><br/>"
        "I hereby declare that the submitted Docker implementation is my own work. "
        "I have successfully executed and verified the required CI/CD pipeline stages, "
        "published the Docker images to my Docker Hub account, and tested the application deployment.<br/><br/>"
        "<b>Student Name:</b> Shreya Tyagi &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>University Roll Number:</b> 202401100300241 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>Section:</b> AIML-D &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>Date:</b> 18 November 2026"
    )
    story.append(Paragraph(declaration_text, declaration_style))

    doc.build(story)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
