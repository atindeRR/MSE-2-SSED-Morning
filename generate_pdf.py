import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf(output_filename="202401100400030_Amit_Kumar.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4a5568'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2d3748')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1a202c')
    )

    elements = []

    # Title
    elements.append(Paragraph("MSE-2 MORNING SHIFT EXAMINATION REPORT", title_style))
    elements.append(Paragraph("Software Engineering and DevOps (AI310B) — Docker Practical Examination", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2b6cb0'), spaceAfter=12))

    # 1. Student Information
    elements.append(Paragraph("1. Student Information", h1_style))
    student_data = [
        [Paragraph("<b>Full Name:</b>", body_style), Paragraph("Amit Kumar", body_style)],
        [Paragraph("<b>University Roll Number:</b>", body_style), Paragraph("202401100400030", body_style)],
        [Paragraph("<b>Section:</b>", body_style), Paragraph("A", body_style)],
        [Paragraph("<b>Branch:</b>", body_style), Paragraph("CSE AIML", body_style)],
        [Paragraph("<b>Subject:</b>", body_style), Paragraph("Software Engineering and DevOps (AI310B)", body_style)],
        [Paragraph("<b>GitHub Username:</b>", body_style), Paragraph("itsamitashu", body_style)],
        [Paragraph("<b>Docker Hub Username:</b>", body_style), Paragraph("itsamitashu", body_style)]
    ]
    t1 = Table(student_data, colWidths=[180, 350])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 8))

    # 2. GitHub Submission Details
    elements.append(Paragraph("2. GitHub Submission Details", h1_style))
    github_data = [
        [Paragraph("<b>Repository URL (Personal Fork):</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Morning", body_style)],
        [Paragraph("<b>Upstream Instructor Repository:</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning", body_style)],
        [Paragraph("<b>Branch Used for Implementation:</b>", body_style), Paragraph("main", body_style)],
        [Paragraph("<b>Pull Request Title:</b>", body_style), Paragraph("DOCKER-EXAM | 202401100400030 | Amit Kumar | A", body_style)]
    ]
    t2 = Table(github_data, colWidths=[180, 350])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 8))

    # 3. Docker Hub Details
    elements.append(Paragraph("3. Docker Hub Image Details", h1_style))
    docker_data = [
        [Paragraph("<b>Docker Hub Profile:</b>", body_style), Paragraph("https://hub.docker.com/u/itsamitashu", body_style)],
        [Paragraph("<b>Frontend Image (General):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/frontend", body_style)],
        [Paragraph("<b>Backend Image (General):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/backend", body_style)],
        [Paragraph("<b>Frontend Image (TaskFlow):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-frontend", body_style)],
        [Paragraph("<b>Backend Image (TaskFlow):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-backend", body_style)],
    ]
    t3 = Table(docker_data, colWidths=[180, 350])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 8))

    # 4. CI/CD Execution Evidence
    elements.append(Paragraph("4. Automated CI/CD Execution Evidence", h1_style))
    cicd_data = [
        [Paragraph("<b>CD Workflow Name:</b>", body_style), Paragraph("Docker Practical - Publish and Verify", body_style)],
        [Paragraph("<b>Workflow Run URL:</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Morning/actions/runs/44252226243", body_style)],
        [Paragraph("<b>Run ID:</b>", body_style), Paragraph("44252226243", body_style)],
        [Paragraph("<b>Execution Status:</b>", body_style), Paragraph("<font color='#276749'><b>Completed [SUCCESS]</b></font>", body_style)],
        [Paragraph("<b>Validated Secrets:</b>", body_style), Paragraph("DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, POSTGRES_PASSWORD", body_style)],
        [Paragraph("<b>Verified CD Stages:</b>", body_style), Paragraph("Checkout, Docker Buildx, Docker Hub Login, Backend Build & Push, Frontend Build & Push, Deployment Compose Validation, Pull Published Images, Deploy Containers, Verify Health (HTTP 200), API & Redis Jest Tests (12/12 Passed)", body_style)],
    ]
    t_cicd = Table(cicd_data, colWidths=[180, 350])
    t_cicd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff4')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c6f6d5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_cicd)
    elements.append(Spacer(1, 8))

    # Page Break for Technical Evidence
    elements.append(PageBreak())

    # 5. Technical Implementation & Test Results
    elements.append(Paragraph("5. Technical Implementation & Verification Logs", h1_style))

    test_box_text = """
    <b>API Test Suite Results — 12/12 PASSED:</b><br/>
    <font face="Courier" size="7.5">
    PASS  ./api.test.js<br/>
      TaskFlow deployed API<br/>
        √ TC01: health endpoint confirms API, PostgreSQL and Redis (48 ms)<br/>
        √ TC02: register a user (119 ms)<br/>
        √ TC03: reject duplicate email (82 ms)<br/>
        √ TC04: login and receive token (109 ms)<br/>
        √ TC05: reject unauthenticated task request (8 ms)<br/>
        √ TC06: create a task (17 ms)<br/>
        √ TC07: list tasks and populate cache (15 ms)<br/>
        √ TC08: subsequent list can be served from Redis (9 ms)<br/>
        √ TC09: update task status and invalidate cache (15 ms)<br/>
        √ TC10: reject invalid task status (8 ms)<br/>
        √ TC11: delete task (11 ms)<br/>
        √ TC12: deleted task is no longer in list (11 ms)<br/>
    Test Suites: 1 passed, 1 total<br/>
    Tests:       12 passed, 12 total | Time: 1.47 s
    </font>
    """
    t_test = Table([[Paragraph(test_box_text, body_style)]], colWidths=[530])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_test)
    elements.append(Spacer(1, 8))

    hc_box_text = """
    <b>Container Status & Health Verification:</b><br/>
    <font face="Courier" size="7.5">
    NAME                            IMAGE                               STATUS<br/>
    mse-2-ssed-morning-backend-1    itsamitashu/taskflow-backend:latest Up (healthy)<br/>
    mse-2-ssed-morning-frontend-1   itsamitashu/taskflow-frontend:latest Up (port 8080)<br/>
    mse-2-ssed-morning-postgres-1   postgres:16-alpine                  Up (healthy)<br/>
    mse-2-ssed-morning-redis-1      redis:7-alpine                      Up (healthy)<br/>
    <br/>
    $ curl.exe http://localhost:3000/health  ==> {"status":"ok","postgres":"ok","redis":"ok"}<br/>
    $ curl.exe -I http://localhost:8080/      ==> HTTP/1.1 200 OK (nginx/1.31.8)
    </font>
    """
    t_hc = Table([[Paragraph(hc_box_text, body_style)]], colWidths=[530])
    t_hc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_hc)
    elements.append(Spacer(1, 8))

    # 6. Implementation Checklist
    elements.append(Paragraph("6. Implementation Checklist", h1_style))
    checklist_data = [
        [Paragraph("[X] Frontend Dockerfile implemented (React + Vite + Nginx multi-stage build)", body_style)],
        [Paragraph("[X] Backend Dockerfile implemented (Node.js 18 Alpine + Express)", body_style)],
        [Paragraph("[X] docker-compose.yml implemented (frontend, backend, postgres, redis)", body_style)],
        [Paragraph("[X] docker-compose.deploy.yml implemented (pure published images without build directives)", body_style)],
        [Paragraph("[X] Frontend & Backend images published to Docker Hub", body_style)],
        [Paragraph("[X] PostgreSQL persistent storage verified (postgres_data named volume)", body_style)],
        [Paragraph("[X] Redis caching verified through API test suite (cache hit TC08)", body_style)],
        [Paragraph("[X] Hadolint linting verified with 0 errors/warnings", body_style)],
        [Paragraph("[X] GitHub Actions CD pipeline executed and passed all stages (Run #44252226243)", body_style)],
        [Paragraph("[X] Changes committed and pushed to personal GitHub fork", body_style)],
        [Paragraph("[X] Final Pull Request submitted to instructor repository", body_style)],
    ]
    t_check = Table(checklist_data, colWidths=[530])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t_check)
    elements.append(Spacer(1, 10))

    # 7. Declaration
    elements.append(Paragraph("7. Mandatory Student Declaration", h1_style))
    declaration_text = """
    <i>"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."</i>
    <br/><br/>
    <b>Student Signature:</b> Amit Kumar<br/>
    <b>Date:</b> November 18, 2026
    """
    t_dec = Table([[Paragraph(declaration_text, body_style)]], colWidths=[530])
    t_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ebf8ff')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3182ce')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(t_dec)

    doc.build(elements)
    print(f"PDF successfully generated at: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_pdf()
