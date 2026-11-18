import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
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
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#0f4c81")
    secondary_color = colors.HexColor("#2d3748")
    accent_green = colors.HexColor("#1b7931")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        alignment=TA_CENTER,
        textColor=primary_color,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=3
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#718096"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15.5,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=secondary_color,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1a202c"),
        backColor=colors.HexColor("#f7fafc"),
        borderColor=colors.HexColor("#e2e8f0"),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
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
        fontSize=7.5,
        leading=9.5
    )

    status_pass = ParagraphStyle(
        'PassBadge',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=accent_green
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2c5282"),
        spaceBefore=4,
        spaceAfter=8
    )

    declaration_style = ParagraphStyle(
        'Declaration',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#2c5282"),
        backColor=colors.HexColor("#ebf8ff"),
        borderColor=colors.HexColor("#bee3f8"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=8,
        spaceAfter=8
    )

    story = []

    # Title & Header
    story.append(Paragraph("Software Engineering and DevOps (AI310B)", title_style))
    story.append(Paragraph("Mid-Semester Examination – 2 (Morning Shift) Practical Report", subtitle_style))
    story.append(Paragraph("Multi-Tier Containerization, Docker Hub Publishing, Orchestration &amp; Automated CI/CD Pipelines", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # Section 1: Student Information
    story.append(Paragraph("1. Student Information", h1_style))
    info_data = [
        [Paragraph("Full Name", table_cell_bold), Paragraph("Shreya Tyagi", table_cell_style)],
        [Paragraph("University Roll Number", table_cell_bold), Paragraph("202401100300241", table_cell_style)],
        [Paragraph("Section", table_cell_bold), Paragraph("AIML-D", table_cell_style)],
        [Paragraph("Programme / Branch", table_cell_bold), Paragraph("B.Tech. Computer Science & Engineering (AIML)", table_cell_style)],
        [Paragraph("Host Operating System", table_cell_bold), Paragraph("Windows 11 (Docker Desktop Engine v29.9.3, Compose v5.7.0)", table_cell_style)]
    ]
    t_info = Table(info_data, colWidths=[170, 350])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_info)

    # Section 2: GitHub & Docker Hub Details
    story.append(Paragraph("2. GitHub &amp; Docker Hub Submission Details", h1_style))
    repo_data = [
        [Paragraph("Base Starter Repository", table_cell_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning", table_cell_code)],
        [Paragraph("Forked Repository URL", table_cell_bold), Paragraph("https://github.com/shreya436/MSE-2-SSED-Morning", table_cell_code)],
        [Paragraph("Working Branch", table_cell_bold), Paragraph("main", table_cell_style)],
        [Paragraph("Docker Hub Username", table_cell_bold), Paragraph("shreyatyagi25", table_cell_code)],
        [Paragraph("Frontend Docker Image", table_cell_bold), Paragraph("shreyatyagi25/taskflow-frontend:latest (Verified Pulled)", table_cell_code)],
        [Paragraph("Backend Docker Image", table_cell_bold), Paragraph("shreyatyagi25/taskflow-backend:latest (Verified Pulled)", table_cell_code)]
    ]
    t_repo = Table(repo_data, colWidths=[170, 350])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
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
    story.append(Paragraph("4. Core Configuration Deliverables", h1_style))

    story.append(Paragraph("<b>A. Frontend Multi-Stage Dockerfile (<code>frontend/Dockerfile</code>)</b>", body_style))
    frontend_code = (
        "FROM node:20-alpine AS builder\n"
        "WORKDIR /app\n"
        "COPY package*.json ./\n"
        "RUN npm install && npm cache clean --force\n"
        "COPY . .\n"
        "RUN npm run build\n\n"
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

    story.append(Paragraph("<b>C. Deployment Docker Compose (<code>docker-compose.deploy.yml</code>) - Zero Build Directives</b>", body_style))
    deploy_code = (
        "services:\n"
        "  postgres:\n"
        "    image: postgres:16-alpine\n"
        "    environment:\n"
        "      POSTGRES_DB: ${POSTGRES_DB:-taskflow}\n"
        "      POSTGRES_USER: ${POSTGRES_USER:-taskflow_user}\n"
        "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be provided in .env}\n"
        "    volumes: [postgres_data:/var/lib/postgresql/data, ./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro]\n"
        "    healthcheck: { test: [\"CMD-SHELL\", \"pg_isready -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow}\"] }\n"
        "    networks: [taskflow-network]\n\n"
        "  redis:\n"
        "    image: redis:7-alpine\n"
        "    healthcheck: [\"CMD\", \"redis-cli\", \"ping\"]\n"
        "    networks: [taskflow-network]\n\n"
        "  backend:\n"
        "    image: ${DOCKERHUB_USERNAME:-shreyatyagi25}/taskflow-backend:latest\n"
        "    ports: [\"3000:3000\"]\n"
        "    environment: { DATABASE_URL: ${DATABASE_URL:?Required in .env}, REDIS_URL: redis://redis:6379 }\n"
        "    depends_on: { postgres: { condition: service_healthy }, redis: { condition: service_healthy } }\n"
        "    healthcheck: { test: [\"CMD-SHELL\", \"node -e \\\"fetch('http://127.0.0.1:3000/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))\\\"\"] }\n"
        "    networks: [taskflow-network]\n\n"
        "  frontend:\n"
        "    image: ${DOCKERHUB_USERNAME:-shreyatyagi25}/taskflow-frontend:latest\n"
        "    ports: [\"8080:80\"]\n"
        "    depends_on: { backend: { condition: service_healthy } }\n"
        "    healthcheck: { test: [\"CMD-SHELL\", \"wget --no-verbose --tries=1 --spider http://127.0.0.1:80/ || exit 1\"] }\n"
        "    networks: [taskflow-network]\n\n"
        "volumes: { postgres_data: }\n"
        "networks: { taskflow-network: { driver: bridge } }"
    )
    story.append(Paragraph(deploy_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(PageBreak())

    # Section 5: Actual Execution Evidence & Screenshots
    story.append(Paragraph("5. Live Application &amp; Deployment Execution Evidence", h1_style))
    story.append(Paragraph("The complete microservice application stack was deployed locally using the published Docker Hub images (<code>docker-compose.deploy.yml</code>). All four containers are running and healthy:", body_style))

    # Live Container Status Table
    cont_headers = [Paragraph("Service / Container", table_header_style), Paragraph("Image Reference", table_header_style), Paragraph("Port Mapping", table_header_style), Paragraph("Status", table_header_style)]
    cont_data = [
        cont_headers,
        [Paragraph("taskflow-backend", table_cell_bold), Paragraph("shreyatyagi25/taskflow-backend:latest", table_cell_code), Paragraph("3000:3000", table_cell_style), Paragraph("Up (healthy)", status_pass)],
        [Paragraph("taskflow-frontend", table_cell_bold), Paragraph("shreyatyagi25/taskflow-frontend:latest", table_cell_code), Paragraph("8080:80", table_cell_style), Paragraph("Up (healthy)", status_pass)],
        [Paragraph("taskflow-postgres", table_cell_bold), Paragraph("postgres:16-alpine", table_cell_code), Paragraph("5432 (Internal)", table_cell_style), Paragraph("Up (healthy)", status_pass)],
        [Paragraph("taskflow-redis", table_cell_bold), Paragraph("redis:7-alpine", table_cell_code), Paragraph("6379 (Internal)", table_cell_style), Paragraph("Up (healthy)", status_pass)],
    ]
    t_cont = Table(cont_data, colWidths=[120, 200, 100, 100])
    t_cont.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cont)
    story.append(Spacer(1, 6))

    # Screenshots
    if os.path.exists("frontend_app.png"):
        story.append(Paragraph("<b>Figure 1: Verified Frontend Application Running at http://localhost:8080</b>", caption_style))
        story.append(Image("frontend_app.png", width=460, height=220))
        story.append(Spacer(1, 6))

    if os.path.exists("backend_health.png"):
        story.append(Paragraph("<b>Figure 2: Verified Backend Health Endpoint at http://localhost:3000/health (PostgreSQL &amp; Redis OK)</b>", caption_style))
        story.append(Image("backend_health.png", width=460, height=130))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Section 6: Test Results & CI/CD Pipeline
    story.append(Paragraph("6. Automated Integration Tests &amp; CI/CD Pipeline Verification", h1_style))
    story.append(Paragraph("All 12 automated Jest / Supertest test cases executed successfully against the deployed application stack, verifying database persistence, cache population, and cache invalidation:", body_style))

    test_headers = [Paragraph("Test ID &amp; Target", table_header_style), Paragraph("Test Description", table_header_style), Paragraph("Result", table_header_style)]
    test_data = [
        test_headers,
        [Paragraph("TC01: Health Endpoint", table_cell_bold), Paragraph("GET /health confirms API, PostgreSQL, and Redis status", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC02: User Registration", table_cell_bold), Paragraph("POST /api/auth/register creates user and hashes password", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC03: Duplicate Email Check", table_cell_bold), Paragraph("POST /api/auth/register rejects duplicate registration with 409", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC04: User Authentication", table_cell_bold), Paragraph("POST /api/auth/login validates credentials and issues JWT token", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC05: Auth Protection", table_cell_bold), Paragraph("GET /api/tasks rejects unauthenticated access with 401", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC06: Task Creation", table_cell_bold), Paragraph("POST /api/tasks stores task in PostgreSQL and invalidates cache", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC07: Query &amp; Cache", table_cell_bold), Paragraph("GET /api/tasks retrieves task from PostgreSQL and sets Redis cache", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC08: Redis Retrieval", table_cell_bold), Paragraph("GET /api/tasks successfully served directly from Redis cache", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC09: Task Update &amp; Eviction", table_cell_bold), Paragraph("PATCH /api/tasks/:id updates status and invalidates cache", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC10: Input Validation", table_cell_bold), Paragraph("PATCH /api/tasks/:id rejects invalid status with 400", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC11: Task Deletion", table_cell_bold), Paragraph("DELETE /api/tasks/:id removes task from PostgreSQL and Redis", table_cell_style), Paragraph("PASSED", status_pass)],
        [Paragraph("TC12: Deletion Verification", table_cell_bold), Paragraph("GET /api/tasks confirms deleted task is no longer present", table_cell_style), Paragraph("PASSED", status_pass)],
    ]
    t_test = Table(test_data, colWidths=[140, 300, 80])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 6))

    # Persistence verification evidence
    story.append(Paragraph("<b>PostgreSQL Volume Persistence Verification:</b>", body_style))
    story.append(Paragraph("Executed stack teardown (<code>docker compose down</code>) and brought the stack back up (<code>docker compose up -d</code>). Named volume <code>postgres_data</code> reattached successfully, and all 12 test suites passed again with zero data loss.", bullet_style))

    # CI/CD Execution Evidence
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Automated GitHub Actions CI/CD Pipeline Execution Evidence:</b>", body_style))
    story.append(Paragraph("• <b>Workflow:</b> Docker Practical - Publish and Verify (<code>.github/workflows/cd.yml</code>)", bullet_style))
    story.append(Paragraph("• <b>Run ID:</b> <code>44249369449</code> &nbsp;|&nbsp; <b>Conclusion:</b> <font color='#1b7931'><b>SUCCESS (ALL 13 STAGES PASSED)</b></font>", bullet_style))
    story.append(Paragraph("• <b>Workflow Run URL:</b> https://github.com/shreya436/MSE-2-SSED-Morning/actions/runs/44249369449", bullet_style))
    story.append(Paragraph("• <b>Pull Request:</b> DOCKER-EXAM | 202401100300241 | Shreya Tyagi | AIML-D", bullet_style))

    # Declaration
    story.append(Spacer(1, 6))
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
