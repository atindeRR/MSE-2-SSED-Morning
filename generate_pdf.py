import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_paths = [
    r'C:\Users\ASUS\OneDrive\Desktop\2400291520200_RISHABH_SINGH.pdf',
    r'C:\Users\ASUS\Downloads\2400291520200_RISHABH_SINGH.pdf',
    r'C:\Users\ASUS\OneDrive\Desktop\MSE-2-SSED-Morning\2400291520200_RISHABH_SINGH.pdf'
]

styles = getSampleStyleSheet()

primary_color = colors.HexColor('#1E3A8A')
secondary_color = colors.HexColor('#0D9488')
dark_neutral = colors.HexColor('#1F2937')
light_bg = colors.HexColor('#F3F4F6')
success_color = colors.HexColor('#16A34A')

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=primary_color,
    alignment=1,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#4B5563'),
    alignment=1,
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=primary_color,
    spaceBefore=8,
    spaceAfter=5,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=dark_neutral,
    spaceAfter=4
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
    textColor=dark_neutral
)

table_cell_bold = ParagraphStyle(
    'TableCellBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=dark_neutral
)

table_success_style = ParagraphStyle(
    'TableSuccess',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=success_color
)

def build_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    # Title Section
    story.append(Paragraph('MSE-2 Morning Shift: Practical Submission Report', title_style))
    story.append(Paragraph('Software Engineering and DevOps (AI310B) | Multi-Container Orchestration &amp; CI/CD Pipeline', subtitle_style))
    story.append(Spacer(1, 4))

    # 1. Student Information
    story.append(Paragraph('1. Student Information', h1_style))
    student_data = [
        [Paragraph('Field', table_header_style), Paragraph('Details', table_header_style)],
        [Paragraph('Full Name', table_cell_bold), Paragraph('Rishabh Singh', table_cell_style)],
        [Paragraph('University Roll Number', table_cell_bold), Paragraph('2400291520200', table_cell_style)],
        [Paragraph('Branch', table_cell_bold), Paragraph('Computer Science &amp; Engineering (Artificial Intelligence)', table_cell_style)],
        [Paragraph('Section / Shift', table_cell_bold), Paragraph('Section C / Morning Shift', table_cell_style)],
        [Paragraph('GitHub Username', table_cell_bold), Paragraph('Rishabhsingh26', table_cell_style)],
        [Paragraph('Docker Hub Username', table_cell_bold), Paragraph('rishabh26104', table_cell_style)]
    ]
    t_student = Table(student_data, colWidths=[160, 380])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 6))

    # 2. GitHub & Docker Hub Details
    story.append(Paragraph('2. Repository and Deployment Details', h1_style))
    repo_data = [
        [Paragraph('Item', table_header_style), Paragraph('Link / Reference', table_header_style)],
        [Paragraph('Base Starter Repository', table_cell_bold), Paragraph('https://github.com/atindeRR/MSE-2-SSED-Morning', table_cell_style)],
        [Paragraph('Student Fork Repository', table_cell_bold), Paragraph('https://github.com/Rishabhsingh26/MSE-2-SSED-Morning', table_cell_style)],
        [Paragraph('Branch Used', table_cell_bold), Paragraph('main', table_cell_style)],
        [Paragraph('Submitted Pull Request', table_cell_bold), Paragraph('https://github.com/atindeRR/MSE-2-SSED-Morning/pull/5 (PR #5)', table_cell_style)],
        [Paragraph('Pull Request Title', table_cell_bold), Paragraph('DOCKER-EXAM | 2400291520200 | Rishabh Singh | C', table_cell_style)],
        [Paragraph('Frontend Docker Image', table_cell_bold), Paragraph('https://hub.docker.com/r/rishabh26104/taskflow-frontend', table_cell_style)],
        [Paragraph('Backend Docker Image', table_cell_bold), Paragraph('https://hub.docker.com/r/rishabh26104/taskflow-backend', table_cell_style)],
        [Paragraph('Frontend Accessible URL', table_cell_bold), Paragraph('http://localhost:8080/ (Served via Nginx container)', table_cell_style)],
        [Paragraph('Backend Health API URL', table_cell_bold), Paragraph('http://localhost:3000/health (Node.js/Express, Postgres, Redis)', table_cell_style)]
    ]
    t_repo = Table(repo_data, colWidths=[160, 380])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_repo)
    story.append(Spacer(1, 6))

    # 3. CD Pipeline Execution Summary
    story.append(Paragraph('3. GitHub Actions CI/CD Pipeline Verification', h1_style))
    story.append(Paragraph('<b>CD Workflow Run:</b> https://github.com/Rishabhsingh26/MSE-2-SSED-Morning/actions/runs/44240888817<br/><b>Workflow Result:</b> <font color="#16A34A"><b>SUCCESS (All 15 Stages Passed)</b></font>', body_style))

    cd_stages = [
        [Paragraph('CD Pipeline Stage', table_header_style), Paragraph('Execution Result', table_header_style), Paragraph('Verification Details', table_header_style)],
        [Paragraph('1. Repository checkout', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('actions/checkout@v4 checked out fork main branch', table_cell_style)],
        [Paragraph('2. Validate Docker Hub secrets', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Validated DOCKERHUB_USERNAME and DOCKERHUB_TOKEN', table_cell_style)],
        [Paragraph('3. Docker Buildx setup', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('docker/setup-buildx-action@v3 initialized', table_cell_style)],
        [Paragraph('4. Docker Hub authentication', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Authenticated to registry-1.docker.io as rishabh26104', table_cell_style)],
        [Paragraph('5. Backend image build', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Built backend context from node:20-alpine', table_cell_style)],
        [Paragraph('6. Backend image publishing', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Pushed rishabh26104/taskflow-backend:latest to Docker Hub', table_cell_style)],
        [Paragraph('7. Frontend image build', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Multi-stage Vite build + Nginx 1.27 alpine', table_cell_style)],
        [Paragraph('8. Frontend image publishing', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Pushed rishabh26104/taskflow-frontend:latest to Docker Hub', table_cell_style)],
        [Paragraph('9. Compose validation', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Verified docker-compose.deploy.yml has no build: tags', table_cell_style)],
        [Paragraph('10. Docker Compose pull', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Pulled published images from Docker Hub', table_cell_style)],
        [Paragraph('11. Application deployment', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('docker compose -f docker-compose.deploy.yml up -d', table_cell_style)],
        [Paragraph('12. Backend health check', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('curl http://localhost:3000/health returned status ok', table_cell_style)],
        [Paragraph('13. Frontend accessibility', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('curl http://localhost:8080/ returned HTTP 200 OK', table_cell_style)],
        [Paragraph('14. Run API test suite', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('All 12 Jest automated test cases passed (12/12)', table_cell_style)],
        [Paragraph('15. Cleanup deployment', table_cell_bold), Paragraph('SUCCESS', table_success_style), Paragraph('Compose down -v executed cleanly', table_cell_style)]
    ]
    t_cd = Table(cd_stages, colWidths=[150, 75, 315])
    t_cd.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_cd)

    story.append(PageBreak())

    # 4. API & Automated Test Evidence
    story.append(Paragraph('4. Application Test Results &amp; Verification Evidence', h1_style))
    story.append(Paragraph('The full-stack containerized application was verified using automated Jest API test suites executed against the live deployed stack:', body_style))

    test_cases = [
        [Paragraph('Test ID &amp; Description', table_header_style), Paragraph('Component Verified', table_header_style), Paragraph('Status', table_header_style)],
        [Paragraph('TC01: Health endpoint check', table_cell_bold), Paragraph('API, PostgreSQL, Redis all reporting {status: ok}', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC02: Register user', table_cell_bold), Paragraph('User registration with bcrypt password hash in DB', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC03: Reject duplicate email', table_cell_bold), Paragraph('DB uniqueness constraint enforcement (409 Conflict)', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC04: Login and JWT creation', table_cell_bold), Paragraph('JWT token authentication returned', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC05: Reject unauthenticated request', table_cell_bold), Paragraph('Protected route rejects request without token (401)', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC06: Create task', table_cell_bold), Paragraph('Task inserted into PostgreSQL with foreign key', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC07: List tasks and populate cache', table_cell_bold), Paragraph('Queries DB and caches response in Redis', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC08: Subsequent task list from Redis', table_cell_bold), Paragraph('Response served from source: redis-cache', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC09: Update task &amp; cache invalidation', table_cell_bold), Paragraph('Status updated and Redis key cleared', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC10: Reject invalid status', table_cell_bold), Paragraph('Validation check rejects unknown task status', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC11: Delete task', table_cell_bold), Paragraph('Task removed from PostgreSQL', table_cell_style), Paragraph('PASSED', table_success_style)],
        [Paragraph('TC12: Verify task deleted from list', table_cell_bold), Paragraph('Task confirmed deleted from database and cache', table_cell_style), Paragraph('PASSED', table_success_style)]
    ]
    t_tests = Table(test_cases, colWidths=[175, 290, 75])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_tests)
    story.append(Spacer(1, 8))

    # 5. Container Architecture & Docker Specifications
    story.append(Paragraph('5. Docker Architecture &amp; Configuration Specifications', h1_style))

    specs_data = [
        [Paragraph('Service', table_header_style), Paragraph('Base Image', table_header_style), Paragraph('Ports', table_header_style), Paragraph('Key Features &amp; Best Practices', table_header_style)],
        [Paragraph('frontend', table_cell_bold), Paragraph('node:20-alpine / nginx:1.27-alpine', table_cell_style), Paragraph('8080:80', table_cell_style), Paragraph('Multi-stage build, static dist served via Nginx, reverse proxy /api and /health to backend', table_cell_style)],
        [Paragraph('backend', table_cell_bold), Paragraph('node:20-alpine', table_cell_style), Paragraph('3000:3000', table_cell_style), Paragraph('Non-root user (1000:1000), production dependencies only, health check configured', table_cell_style)],
        [Paragraph('postgres', table_cell_bold), Paragraph('postgres:16-alpine', table_cell_style), Paragraph('5432 (int)', table_cell_style), Paragraph('Named volume postgres_data for persistence, automatic init.sql mount, pg_isready healthcheck', table_cell_style)],
        [Paragraph('redis', table_cell_bold), Paragraph('redis:7-alpine', table_cell_style), Paragraph('6379 (int)', table_cell_style), Paragraph('In-memory caching layer, redis-cli ping healthcheck, automatic reconnection pool', table_cell_style)]
    ]
    t_specs = Table(specs_data, colWidths=[65, 130, 65, 280])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_specs)
    story.append(Spacer(1, 8))

    # 6. Implementation Checklist & Verification
    story.append(Paragraph('6. Implementation Checklist', h1_style))
    checklist_text = '''
<b>[x] Frontend Dockerfile implemented:</b> Multi-stage build with Node 20 and Nginx 1.27 Alpine.<br/>
<b>[x] Backend Dockerfile implemented:</b> Node 20 Alpine, non-root user (1000:1000), Hadolint clean.<br/>
<b>[x] docker-compose.yml implemented:</b> Orchestrates frontend, backend, postgres, redis with health checks.<br/>
<b>[x] docker-compose.deploy.yml implemented:</b> Deploys strictly from published Docker Hub images without build directives.<br/>
<b>[x] Frontend image published:</b> rishabh26104/taskflow-frontend:latest on Docker Hub.<br/>
<b>[x] Backend image published:</b> rishabh26104/taskflow-backend:latest on Docker Hub.<br/>
<b>[x] PostgreSQL persistence verified:</b> Named volume postgres_data tested across container restarts.<br/>
<b>[x] Redis caching verified:</b> Cache hits on subsequent GET /api/tasks (source: redis-cache) and cache invalidation on mutations.<br/>
<b>[x] CD pipeline passed:</b> All 15 workflow stages in cd.yml executed with 100% success.<br/>
<b>[x] Final Pull Request created:</b> PR #5 opened on instructor repository with prescribed title format.
'''
    story.append(Paragraph(checklist_text, body_style))
    story.append(Spacer(1, 8))

    # 7. Declaration
    story.append(Paragraph('7. Declaration', h1_style))
    declaration_box = [
        [Paragraph('<i>"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."</i><br/><br/><b>Student Name:</b> Rishabh Singh &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Roll Number:</b> 2400291520200 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> November 18, 2026', body_style)]
    ]
    t_decl = Table(declaration_box, colWidths=[540])
    t_decl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 1, primary_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_decl)

    doc.build(story)
    print('PDF built successfully at:', filename)

for path in pdf_paths:
    build_pdf(path)
