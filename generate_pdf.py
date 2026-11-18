#!/usr/bin/env python3
"""
PDF Generator for Docker Practical Exam Submission
Student: Vivek Kumar | Roll: 2400291520281 | Section: D | Branch: CSEAI

Usage:
  1. Install reportlab: pip install reportlab
  2. Place your screenshots in a folder (e.g., screenshots/)
  3. Update SCREENSHOTS dict below with actual file paths
  4. Run: python generate_pdf.py
  5. Output: 2400291520281_Vivek_Kumar.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# ─── UPDATE THESE WITH YOUR ACTUAL SCREENSHOT PATHS ────────────────────────
SCREENSHOTS = {
    "Actions workflow run":        "screenshots/01_workflow_run.png",
    "Docker Hub authentication":   "screenshots/02_docker_login.png",
    "Backend build and publish":   "screenshots/03_backend_push.png",
    "Frontend build and publish":  "screenshots/04_frontend_push.png",
    "Compose image pull":          "screenshots/05_compose_pull.png",
    "Application deployment":      "screenshots/06_deployment.png",
    "Backend health check":        "screenshots/07_health_check.png",
    "Frontend accessibility check":"screenshots/08_frontend_check.png",
    "Final pipeline status":       "screenshots/09_pipeline_status.png",
    "Instructor CI results":       "screenshots/10_ci_results.png",
}

STUDENT = {
    "name":     "Vivek Kumar",
    "roll":     "2400291520281",
    "section":  "D",
    "branch":   "CSEAI",
    "github":   "vivvvekk",
    "dockerhub":"vivvvekk",
    "course":   "Software Engineering and DevOps (AI310B)",
    "exam":     "MSE-2 Morning Shift",
    "fork_url": "https://github.com/vivvvekk/MSE-2-SSED-Morning",
    "branch_used": "main",
    "frontend_image": "vivvvekk/taskflow-frontend:latest",
    "backend_image":  "vivvvekk/taskflow-backend:latest",
}

OUTPUT = f"{STUDENT['roll']}_Vivek_Kumar.pdf"
PAGE_W, PAGE_H = A4

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"Docker Exam - {STUDENT['name']}",
        author=STUDENT['name'],
    )
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title2', parent=styles['Title'],
        fontSize=20, spaceAfter=12, textColor=colors.HexColor('#1a1a2e'))
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=14, spaceAfter=8, textColor=colors.HexColor('#16213e'),
        borderPad=4, backColor=colors.HexColor('#e8f4fd'),
        borderColor=colors.HexColor('#2196F3'), borderWidth=1,
        leftIndent=6, borderRadius=4)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
        fontSize=12, spaceAfter=6, textColor=colors.HexColor('#0f3460'))
    body = ParagraphStyle('Body2', parent=styles['Normal'],
        fontSize=10, spaceAfter=4, leading=14)
    caption = ParagraphStyle('Caption', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    placeholder = ParagraphStyle('Placeholder', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER, backColor=colors.HexColor('#f5f5f5'),
        borderColor=colors.HexColor('#cccccc'), borderWidth=1,
        borderPad=20)
    
    story = []
    
    # ── Cover ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Docker Practical Exam", title_style))
    story.append(Paragraph("MSE-2 Morning Shift Submission", styles['Heading2']))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2196F3')))
    story.append(Spacer(1, 0.5*cm))
    
    cover_data = [
        ["Field", "Value"],
        ["Name", STUDENT['name']],
        ["Roll Number", STUDENT['roll']],
        ["Section", STUDENT['section']],
        ["Branch", STUDENT['branch']],
        ["Course", STUDENT['course']],
        ["Exam", STUDENT['exam']],
        ["GitHub Username", STUDENT['github']],
        ["Docker Hub Username", STUDENT['dockerhub']],
    ]
    t = Table(cover_data, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2196F3')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # ── Section 1: Student Information ────────────────────────────────────────
    story.append(Paragraph("1. Student Information", h1))
    story.append(Paragraph(f"<b>Name:</b> {STUDENT['name']}", body))
    story.append(Paragraph(f"<b>Roll Number:</b> {STUDENT['roll']}", body))
    story.append(Paragraph(f"<b>Section:</b> {STUDENT['section']}", body))
    story.append(Paragraph(f"<b>Branch:</b> {STUDENT['branch']}", body))
    story.append(Paragraph(f"<b>GitHub Username:</b> {STUDENT['github']}", body))
    story.append(Spacer(1, 0.5*cm))
    
    # ── Section 2: GitHub Details ─────────────────────────────────────────────
    story.append(Paragraph("2. GitHub Details", h1))
    story.append(Paragraph(f"<b>Fork URL:</b> {STUDENT['fork_url']}", body))
    story.append(Paragraph(f"<b>Branch Used:</b> {STUDENT['branch_used']}", body))
    story.append(Spacer(1, 0.5*cm))
    
    # ── Section 3: Docker Hub Details ─────────────────────────────────────────
    story.append(Paragraph("3. Docker Hub Details", h1))
    story.append(Paragraph(f"<b>Docker Hub Username:</b> {STUDENT['dockerhub']}", body))
    story.append(Paragraph(f"<b>Frontend Image:</b> {STUDENT['frontend_image']}", body))
    story.append(Paragraph(f"<b>Backend Image:</b> {STUDENT['backend_image']}", body))
    story.append(Spacer(1, 0.5*cm))
    
    # ── Section 4: CI/CD Evidence ─────────────────────────────────────────────
    story.append(Paragraph("4. CI/CD Execution Evidence", h1))
    story.append(Paragraph(
        "Each screenshot below documents a stage of the CI/CD pipeline or deployment verification.",
        body))
    story.append(Spacer(1, 0.3*cm))
    
    for idx, (label, path) in enumerate(SCREENSHOTS.items(), 1):
        story.append(Paragraph(f"4.{idx} — {label}", h2))
        if os.path.exists(path):
            try:
                img = Image(path, width=15*cm, height=10*cm, kind='proportional')
                story.append(img)
            except Exception as e:
                story.append(Paragraph(
                    f"[Image at {path} could not be loaded: {e}]", placeholder))
        else:
            story.append(Paragraph(
                f"[ Screenshot placeholder: {label} ]\n"
                f"Place your screenshot at: {path}",
                placeholder))
        story.append(Paragraph(f"Figure {idx}: {label}", caption))
        story.append(Spacer(1, 0.5*cm))
        story.append(PageBreak())
    
    # ── Section 5: Declaration ────────────────────────────────────────────────
    story.append(Paragraph("5. Declaration", h1))
    declaration = (
        "I hereby declare that the submitted Docker implementation is my own work. "
        "I have successfully executed and verified the required CI/CD pipeline stages, "
        "published the Docker images to my Docker Hub account, and tested the application deployment."
    )
    story.append(Paragraph(declaration, body))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"<b>Name:</b> {STUDENT['name']}", body))
    story.append(Paragraph(f"<b>Roll:</b> {STUDENT['roll']}", body))
    story.append(Paragraph(f"<b>Date:</b> 18 November 2026", body))
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width=5*cm, thickness=1, color=colors.black))
    story.append(Paragraph("Signature", caption))
    
    doc.build(story)
    print(f"✅ PDF generated: {OUTPUT}")
    print(f"   Add screenshots to 'screenshots/' folder and re-run to include them.")

if __name__ == "__main__":
    build_pdf()
