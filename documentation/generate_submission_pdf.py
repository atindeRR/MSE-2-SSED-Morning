from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "documentation" / "evidence"
OUTPUT = ROOT / "202401100300252_SUDEEKSHA_SINGH.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleBlue", parent=styles["Title"], textColor=colors.HexColor("#1f4e79"), fontSize=22, leading=27, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#1f4e79"), fontSize=14, leading=18, spaceBefore=8, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11))
styles.add(ParagraphStyle(name="Evidence", parent=styles["BodyText"], fontSize=9, leading=12, textColor=colors.HexColor("#34495e")))
styles.add(ParagraphStyle(name="CellLabel", parent=styles["Small"], fontName="Helvetica-Bold", textColor=colors.HexColor("#1f4e79")))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d9e2f3"))
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFillColor(colors.HexColor("#5b6573"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 9 * mm, "MSE-2 Morning Shift | Docker Practical Submission")
    canvas.drawRightString(192 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def fit_image(path, max_width=174 * mm, max_height=205 * mm):
    image = Image(str(path))
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    return image


def info_table(rows):
    wrapped_rows = [[Paragraph(str(label), styles["CellLabel"]), Paragraph(str(value), styles["Small"])] for label, value in rows]
    table = Table(wrapped_rows, colWidths=[52 * mm, 116 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf2f8")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1f4e79")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc9d6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


story = [
    Spacer(1, 16 * mm),
    Paragraph("MSE-2 Morning Shift", styles["TitleBlue"]),
    Paragraph("Software Engineering and DevOps (AI310B)", ParagraphStyle(name="Subtitle", parent=styles["Heading2"], alignment=TA_CENTER, textColor=colors.HexColor("#455a64"), spaceAfter=7)),
    Paragraph("Docker Practical Submission Documentation", ParagraphStyle(name="DocTitle", parent=styles["Heading1"], alignment=TA_CENTER, fontSize=18, leading=22, textColor=colors.HexColor("#17202a"), spaceAfter=20)),
    Paragraph("1. Student Information", styles["Section"]),
    info_table([
        ["Full Name", "Sudeeksha Singh"],
        ["University Roll Number", "202401100300252"],
        ["Section", "D"],
        ["Branch", "CSEAI"],
        ["GitHub Username", "Sudeekshasingh-git"],
    ]),
    Spacer(1, 6 * mm),
    Paragraph("2. GitHub Submission Details", styles["Section"]),
    info_table([
        ["Personal Fork", '<link href="https://github.com/Sudeekshasingh-git/MSE-2-SSED-Morning" color="#1565c0">github.com/Sudeekshasingh-git/MSE-2-SSED-Morning</link>'],
        ["Implementation Branch", "main"],
        ["Commit Author", "Sudeeksha Singh &lt;Sudeekshasingh-git@users.noreply.github.com&gt;"],
        ["Verified CD Run", '<link href="https://github.com/Sudeekshasingh-git/MSE-2-SSED-Morning/actions/runs/44244016081" color="#1565c0">Actions run 44244016081 - Success</link>'],
    ]),
    Spacer(1, 6 * mm),
    Paragraph("3. Docker Hub Details", styles["Section"]),
    info_table([
        ["Docker Hub Username", "sudeekshasingh"],
        ["Frontend Image", '<link href="https://hub.docker.com/r/sudeekshasingh/frontend" color="#1565c0">sudeekshasingh/frontend:latest</link>'],
        ["Backend Image", '<link href="https://hub.docker.com/r/sudeekshasingh/backend" color="#1565c0">sudeekshasingh/backend:latest</link>'],
    ]),
    Spacer(1, 6 * mm),
    Paragraph("4. Live Deployment (Render)", styles["Section"]),
    info_table([
        ["Frontend URL", '<link href="https://taskflow-frontend-sudeeksha.onrender.com" color="#1565c0">taskflow-frontend-sudeeksha.onrender.com</link>'],
        ["Backend Health URL", '<link href="https://taskflow-backend-sudeeksha.onrender.com/health" color="#1565c0">taskflow-backend-sudeeksha.onrender.com/health</link>'],
        ["Deployment Status", "Live and verified (HTTP 200); PostgreSQL and Redis connected"],
    ]),
    PageBreak(),
    Paragraph("Docker Hub Image Evidence", styles["TitleBlue"]),
    Paragraph("The public repositories below contain the latest frontend and backend images used by the image-only deployment Compose file.", styles["Evidence"]),
    Spacer(1, 4 * mm),
    fit_image(EVIDENCE / "dockerhub-backend.png", max_height=101 * mm),
    Spacer(1, 4 * mm),
    fit_image(EVIDENCE / "dockerhub-frontend.png", max_height=101 * mm),
    PageBreak(),
    Paragraph("CI/CD Execution Evidence", styles["TitleBlue"]),
    Paragraph("GitHub Actions run 44244016081 completed successfully. The published artifacts and successful job are visible in this workflow summary.", styles["Evidence"]),
    Spacer(1, 4 * mm),
    fit_image(EVIDENCE / "github-actions-success.png", max_height=210 * mm),
    PageBreak(),
    Paragraph("Successful CI/CD Stages", styles["TitleBlue"]),
    Paragraph("The job-stage list confirms Docker Hub authentication, backend and frontend build/publish, image pull, image-based Compose deployment, deployment verification, API tests, and cleanup.", styles["Evidence"]),
    Spacer(1, 4 * mm),
    fit_image(EVIDENCE / "cicd-stages.png", max_height=222 * mm),
    PageBreak(),
    Paragraph("Application Deployment Verification", styles["TitleBlue"]),
    Paragraph("The frontend and backend were also checked locally using the four-service Docker Compose deployment. PostgreSQL and Redis health were reported by the backend health endpoint.", styles["Evidence"]),
    Spacer(1, 4 * mm),
    fit_image(EVIDENCE / "frontend-running.png", max_height=118 * mm),
]

health = EVIDENCE / "backend-health.png"
if health.exists():
    story.extend([Spacer(1, 4 * mm), fit_image(health, max_height=62 * mm)])

story.extend([
    PageBreak(),
    Paragraph("Implementation and Verification Summary", styles["TitleBlue"]),
    Paragraph("Completed items", styles["Section"]),
    info_table([
        ["Dockerfiles", "Frontend multi-stage Node/Vite to Nginx; backend production Node image with non-root runtime and health checks."],
        ["Compose", "Frontend, backend, PostgreSQL and Redis connected by service names on an explicit bridge network."],
        ["Persistence", "Named PostgreSQL and Redis volumes; PostgreSQL data remained available after restart."],
        ["Published deployment", "docker-compose.deploy.yml uses Docker Hub images only and contains no build directives."],
        ["Live deployment", "Deployed on Render using the published multi-arch images; frontend and backend health verified over HTTPS."],
        ["Local tests", "All four containers healthy; backend health OK; frontend HTTP 200; supplied API suite passed 12/12."],
        ["CI/CD", "All publish, pull, deployment, health, accessibility and API test stages passed."],
    ]),
    Spacer(1, 9 * mm),
    Paragraph("Declaration", styles["Section"]),
    Paragraph('"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."', ParagraphStyle(name="Declaration", parent=styles["BodyText"], fontSize=11, leading=16, textColor=colors.HexColor("#263238"), borderColor=colors.HexColor("#9fbad0"), borderWidth=1, borderPadding=10, backColor=colors.HexColor("#f7fbff"))),
    Spacer(1, 18 * mm),
    Paragraph("Sudeeksha Singh", styles["Heading3"]),
    Paragraph("Roll No. 202401100300252 | Section D | CSEAI", styles["BodyText"]),
])

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=17 * mm, bottomMargin=20 * mm, title="MSE-2 Docker Practical Submission - Sudeeksha Singh", author="Sudeeksha Singh")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
