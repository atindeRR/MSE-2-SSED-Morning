import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def get_scaled_image(path, target_width=500, max_height=260):
    from PIL import Image as PILImage
    if not os.path.exists(path):
        return None
    with PILImage.open(path) as img:
        orig_w, orig_h = img.size
    aspect = orig_h / orig_w
    target_height = target_width * aspect
    if target_height > max_height:
        target_height = max_height
        target_width = target_height / aspect
    return RLImage(path, width=target_width, height=target_height)

def generate_pdf(output_filename="202401100400030_Amit_Kumar.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
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
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#4a5568'),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2d3748'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2d3748')
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Italic'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#4a5568'),
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=8
    )

    elements = []

    # Title
    elements.append(Paragraph("MSE-2 MORNING SHIFT EXAMINATION REPORT", title_style))
    elements.append(Paragraph("Software Engineering and DevOps (AI310B) — Docker Practical Examination", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2b6cb0'), spaceAfter=10))

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
    t1 = Table(student_data, colWidths=[170, 360])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 6))

    # 2. GitHub Submission Details
    elements.append(Paragraph("2. GitHub Submission Details", h1_style))
    github_data = [
        [Paragraph("<b>Repository URL (Personal Fork):</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Morning", body_style)],
        [Paragraph("<b>Upstream Instructor Repository:</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning", body_style)],
        [Paragraph("<b>Branch Used for Implementation:</b>", body_style), Paragraph("main", body_style)],
        [Paragraph("<b>Pull Request URL:</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning/pull/195", body_style)],
        [Paragraph("<b>Pull Request Title:</b>", body_style), Paragraph("DOCKER-EXAM | 202401100400030 | Amit Kumar | A", body_style)]
    ]
    t2 = Table(github_data, colWidths=[170, 360])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 6))

    # 3. Docker Hub Details
    elements.append(Paragraph("3. Docker Hub Image Details", h1_style))
    docker_data = [
        [Paragraph("<b>Docker Hub Profile:</b>", body_style), Paragraph("https://hub.docker.com/u/itsamitashu", body_style)],
        [Paragraph("<b>Frontend Image (General):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/frontend", body_style)],
        [Paragraph("<b>Backend Image (General):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/backend", body_style)],
        [Paragraph("<b>Frontend Image (TaskFlow):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-frontend", body_style)],
        [Paragraph("<b>Backend Image (TaskFlow):</b>", body_style), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-backend", body_style)],
    ]
    t3 = Table(docker_data, colWidths=[170, 360])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 6))

    # 4. CI/CD Pipeline Summary Table
    elements.append(Paragraph("4. Automated CI/CD Pipeline Status", h1_style))
    cicd_data = [
        [Paragraph("<b>Workflow Name:</b>", body_style), Paragraph("Docker Practical - Publish and Verify (cd.yml)", body_style)],
        [Paragraph("<b>Run URL:</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Morning/actions/runs/44252226243", body_style)],
        [Paragraph("<b>Execution Outcome:</b>", body_style), Paragraph("<font color='#276749'><b>COMPLETED [SUCCESS]</b></font> (Duration: 1m 21s)", body_style)],
        [Paragraph("<b>Verified Stages:</b>", body_style), Paragraph("Checkout, Docker Buildx, Docker Hub Login, Backend Build & Push, Frontend Build & Push, Deploy Compose Validation, Pull Images, Deploy Containers, Verify Health (HTTP 200), Jest API Tests (12/12 Passed)", body_style)],
    ]
    t_cicd = Table(cicd_data, colWidths=[170, 360])
    t_cicd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff4')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c6f6d5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t_cicd)
    elements.append(Spacer(1, 10))

    # PAGE 2: Evidence Screenshots 1 & 2
    elements.append(PageBreak())
    elements.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots", h1_style))
    elements.append(Paragraph("Below are the verified execution captures covering all examination requirements:", body_style))
    elements.append(Spacer(1, 6))

    # Screenshot 1: GitHub Actions Workflow Run Success
    elements.append(Paragraph("Evidence 1: GitHub Actions Workflow Execution & Final Status [SUCCESS]", h2_style))
    img_wf = get_scaled_image("evidence_images/browser_workflow_run.png", target_width=500, max_height=240)
    if img_wf:
        elements.append(img_wf)
        elements.append(Paragraph("Figure 1: GitHub Actions CD Pipeline (Run #44252226243) showing all stages completed successfully.", caption_style))

    # Screenshot 2: GitHub Repository Secrets
    elements.append(Paragraph("Evidence 2: Docker Hub Authentication & Repository Secrets Configuration", h2_style))
    img_sec = get_scaled_image("evidence_images/browser_secrets.png", target_width=500, max_height=210)
    if img_sec:
        elements.append(img_sec)
        elements.append(Paragraph("Figure 2: Verified GitHub Actions secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, POSTGRES_PASSWORD.", caption_style))

    # PAGE 3: Evidence Screenshots 3 & 4 (VS Code Integrated Terminal)
    elements.append(PageBreak())
    elements.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", h1_style))

    # Screenshot 3: VS Code Docker Hub Push
    elements.append(Paragraph("Evidence 3: Backend & Frontend Docker Image Build and Publishing (VS Code Terminal)", h2_style))
    img_push = get_scaled_image("evidence_images/vscode_docker_push.png", target_width=500, max_height=240)
    if img_push:
        elements.append(img_push)
        elements.append(Paragraph("Figure 3: VS Code integrated terminal executing Docker push for itsamitashu/backend:latest and itsamitashu/frontend:latest.", caption_style))

    # Screenshot 4: VS Code Deployment using Published Images
    elements.append(Paragraph("Evidence 4: Docker Compose Image Pull & Container Deployment (VS Code Terminal)", h2_style))
    img_dep = get_scaled_image("evidence_images/vscode_deployment.png", target_width=500, max_height=230)
    if img_dep:
        elements.append(img_dep)
        elements.append(Paragraph("Figure 4: VS Code terminal deploying docker-compose.deploy.yml with published images and verifying healthy container status.", caption_style))

    # PAGE 4: Evidence Screenshots 5 & 6 (VS Code Integrated Terminal)
    elements.append(PageBreak())
    elements.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", h1_style))

    # Screenshot 5: VS Code Health & Accessibility Verification
    elements.append(Paragraph("Evidence 5: Backend Health Check & Frontend Accessibility Verification (VS Code Terminal)", h2_style))
    img_hc = get_scaled_image("evidence_images/vscode_health_and_frontend.png", target_width=500, max_height=220)
    if img_hc:
        elements.append(img_hc)
        elements.append(Paragraph("Figure 5: VS Code terminal curl execution confirming Backend status 'ok' on port 3000 and Frontend HTTP 200 OK on port 8080.", caption_style))

    # Screenshot 6: VS Code Jest API Tests
    elements.append(Paragraph("Evidence 6: Automated API & Redis Caching Test Suite (VS Code Terminal)", h2_style))
    img_test = get_scaled_image("evidence_images/vscode_jest_tests.png", target_width=500, max_height=230)
    if img_test:
        elements.append(img_test)
        elements.append(Paragraph("Figure 6: VS Code terminal running Jest test suite confirming 12/12 passed tests for API, Redis, and PostgreSQL.", caption_style))

    # PAGE 5: Pull Request & Declaration
    elements.append(PageBreak())
    elements.append(Paragraph("6. Pull Request Submission & Mandatory Declaration", h1_style))

    # Screenshot 7: Pull Request Page
    elements.append(Paragraph("Evidence 7: Submitted Pull Request on Instructor Repository (#195)", h2_style))
    img_pr = get_scaled_image("evidence_images/browser_pull_request.png", target_width=500, max_height=240)
    if img_pr:
        elements.append(img_pr)
        elements.append(Paragraph("Figure 7: Pull Request #195 created on atindeRR/MSE-2-SSED-Morning with required title and details.", caption_style))
    elements.append(Spacer(1, 8))

    # Implementation Checklist
    elements.append(Paragraph("Implementation Verification Checklist", h2_style))
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
        [Paragraph("[X] Pull Request #195 submitted against instructor repository with required title format", body_style)],
    ]
    t_check = Table(checklist_data, colWidths=[530])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_check)
    elements.append(Spacer(1, 10))

    # Declaration
    elements.append(Paragraph("Mandatory Student Declaration", h2_style))
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
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(t_dec)

    doc.build(elements)
    print(f"PDF successfully generated at: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_pdf()
