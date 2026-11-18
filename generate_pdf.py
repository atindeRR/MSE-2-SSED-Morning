import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def create_submission_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER
    )
    sec_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=8,
        spaceAfter=5
    )
    sub_heading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )
    code_success = ParagraphStyle(
        'CodeSuccess',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#047857')
    )
    declaration_style = ParagraphStyle(
        'Declaration',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1E293B')
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("MSE-2 Morning Shift Practical Examination", title_style))
    elements.append(Paragraph("Software Engineering and DevOps (AI310B) — Docker & CI/CD Deployment Documentation", subtitle_style))
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=6))

    # 1. Student Information
    elements.append(Paragraph("1. Student Information", sec_heading))
    student_data = [
        [Paragraph("Full Name", body_bold), Paragraph("Yuvraj Patel", body_style)],
        [Paragraph("University Roll Number", body_bold), Paragraph("2400291520289", body_style)],
        [Paragraph("Section", body_bold), Paragraph("D", body_style)],
        [Paragraph("Branch", body_bold), Paragraph("CSE AI", body_style)],
        [Paragraph("GitHub Username", body_bold), Paragraph("YUVRAJPATEL18", body_style)],
    ]
    t1 = Table(student_data, colWidths=[160, 380])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 6))

    # 2. GitHub Submission Details
    elements.append(Paragraph("2. GitHub Submission Details", sec_heading))
    repo_data = [
        [Paragraph("GitHub Repository URL (Personal Fork)", body_bold), Paragraph("https://github.com/YUVRAJPATEL18/MSE-2-SSED-Morning", body_style)],
        [Paragraph("GitHub Branch Used for Implementation", body_bold), Paragraph("main", body_style)],
        [Paragraph("Base Repository", body_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Morning", body_style)],
        [Paragraph("Commit Hash", body_bold), Paragraph("390617f", body_style)],
    ]
    t2 = Table(repo_data, colWidths=[160, 380])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 6))

    # 3. Docker Hub Details
    elements.append(Paragraph("3. Docker Hub Details", sec_heading))
    docker_data = [
        [Paragraph("Docker Hub Username", body_bold), Paragraph("yuvraj180", body_style)],
        [Paragraph("Frontend Docker Image URL", body_bold), Paragraph("https://hub.docker.com/r/yuvraj180/taskflow-frontend", body_style)],
        [Paragraph("Backend Docker Image URL", body_bold), Paragraph("https://hub.docker.com/r/yuvraj180/taskflow-backend", body_style)],
    ]
    t3 = Table(docker_data, colWidths=[160, 380])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 6))

    # 4. CI/CD Execution Evidence Table
    elements.append(Paragraph("4. CI/CD Execution Evidence", sec_heading))
    elements.append(Paragraph("Execution stages verified through the automated CI/CD pipeline:", body_style))
    elements.append(Spacer(1, 3))

    stage_summary = [
        [Paragraph("Stage", body_bold), Paragraph("Pipeline Action / Verification Command", body_bold), Paragraph("Status", body_bold)],
        [Paragraph("• GitHub Actions workflow execution", body_style), Paragraph("Docker Practical - Publish and Verify (cd.yml on main)", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Docker Hub authentication", body_style), Paragraph("docker/login-action@v3 using DOCKERHUB_TOKEN", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Backend Docker image build & publishing", body_style), Paragraph("docker/build-push-action@v6 -> yuvraj180/taskflow-backend:latest", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Frontend Docker image build & publishing", body_style), Paragraph("docker/build-push-action@v6 -> yuvraj180/taskflow-frontend:latest", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Docker Compose image pull", body_style), Paragraph("docker compose -f docker-compose.deploy.yml pull", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Application deployment", body_style), Paragraph("docker compose -f docker-compose.deploy.yml up -d", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Backend health check", body_style), Paragraph("curl --fail http://localhost:3000/health (status: ok)", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Frontend accessibility verification", body_style), Paragraph("curl --fail http://localhost:8080/ (HTTP 200 OK)", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Final successful CI/CD pipeline status", body_style), Paragraph("Workflow run completed successfully", body_style), Paragraph("✔ SUCCESS", code_success)],
        [Paragraph("• Automated API & Redis test suite", body_style), Paragraph("Jest runner: 12 of 12 tests passed (TC01 - TC12)", body_style), Paragraph("✔ SUCCESS", code_success)],
    ]
    t4 = Table(stage_summary, colWidths=[150, 290, 100])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    elements.append(t4)
    elements.append(Spacer(1, 6))

    # PAGE BREAK: GitHub Actions Screenshots
    elements.append(PageBreak())
    elements.append(Paragraph("Figure 1: GitHub Actions Job Execution Breakdown", sub_heading))
    elements.append(Spacer(1, 4))
    if os.path.exists("job_steps.png"):
        elements.append(Image("job_steps.png", width=530, height=365))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Figure 2: Pipeline Run Overview & Status", sub_heading))
    elements.append(Spacer(1, 4))
    if os.path.exists("workflow_run.png"):
        elements.append(Image("workflow_run.png", width=530, height=275))

    # PAGE BREAK: Terminal Screenshot Evidence
    elements.append(PageBreak())
    elements.append(Paragraph("Figure 3: Terminal Execution — Docker Compose, Health Checks & API Tests", sub_heading))
    elements.append(Spacer(1, 6))
    if os.path.exists("terminal_screenshot.png"):
        elements.append(Image("terminal_screenshot.png", width=530, height=540))

    # PAGE BREAK: Actions History & Declaration
    elements.append(PageBreak())
    elements.append(Paragraph("Figure 4: GitHub Actions Workflow Execution History", sub_heading))
    elements.append(Spacer(1, 4))
    if os.path.exists("actions_summary.png"):
        elements.append(Image("actions_summary.png", width=530, height=265))
    elements.append(Spacer(1, 14))

    # 5. Declaration
    elements.append(Paragraph("5. Declaration", sec_heading))
    declaration_box = [
        Paragraph(
            '"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed '
            'and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, '
            'and tested the application deployment."',
            declaration_style
        ),
        Spacer(1, 10),
        Paragraph("<b>Student Signature:</b> Yuvraj Patel &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Roll Number:</b> 2400291520289 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> November 18, 2026", body_style)
    ]
    t5 = Table([[declaration_box]], colWidths=[540])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3B82F6')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t5)

    # Build Document
    doc.build(elements)
    print(f"PDF successfully built at {output_filename}")

if __name__ == '__main__':
    target = os.path.abspath("2400291520289_YUVRAJ_PATEL.pdf")
    create_submission_pdf(target)
