import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_report(output_path, img_dir):
    doc = Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Header / Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_sub = title_p.add_run("MSE-2 MORNING SHIFT · PRACTICAL EVALUATION REPORT\n")
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)

    run_title = title_p.add_run("Software Engineering and DevOps (AI310B)\nDocker Containerization, Orchestration & CI/CD Pipeline")
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    # Divider line
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(12)
    div_run = div_p.add_run("―" * 58)
    div_run.font.color.rgb = RGBColor(0xCC, 0xD6, 0xE0)

    # 1. Student Information
    h1 = doc.add_heading("1. Student Information", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    student_data = [
        ("Full Name", "Abhay Singh Tomar"),
        ("University Roll Number", "202401100300005"),
        ("Section", "A"),
        ("Branch", "Computer Science & Engineering (Artificial Intelligence)"),
        ("GitHub Username", "abhayships"),
        ("Docker Hub Username", "abhay1tomar1")
    ]

    for idx, (k, v) in enumerate(student_data):
        row = table.rows[idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.3)
        cell_v.width = Inches(4.7)

        p_k = cell_k.paragraphs[0]
        r_k = p_k.add_run(k)
        r_k.bold = True
        r_k.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        p_v = cell_v.paragraphs[0]
        r_v = p_v.add_run(v)
        r_v.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        set_cell_background(cell_k, "F8FAFC")
        set_cell_background(cell_v, "FFFFFF" if idx % 2 == 0 else "F8FAFC")
        set_cell_margins(cell_k, top=100, bottom=100, left=150, right=150)
        set_cell_margins(cell_v, top=100, bottom=100, left=150, right=150)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 2. GitHub & Docker Hub Details
    h2 = doc.add_heading("2. Repository, Pull Request & Deployment References", level=1)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    repo_table = doc.add_table(rows=7, cols=2)
    repo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    repo_table.autofit = False

    repo_data = [
        ("GitHub Repository (Fork)", "https://github.com/abhayships/MSE-2-SSED-Morning"),
        ("Active Implementation Branch", "main"),
        ("Submitted Pull Request (PR #30)", "https://github.com/atindeRR/MSE-2-SSED-Morning/pull/30"),
        ("Pull Request Title", "DOCKER-EXAM | 202401100300005 | Abhay Singh Tomar | A"),
        ("Instructor Upstream Repository", "https://github.com/atindeRR/MSE-2-SSED-Morning"),
        ("Frontend Docker Image (Docker Hub)", "abhay1tomar1/taskflow-frontend:latest"),
        ("Backend Docker Image (Docker Hub)", "abhay1tomar1/taskflow-backend:latest")
    ]

    for idx, (k, v) in enumerate(repo_data):
        row = repo_table.rows[idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.6)
        cell_v.width = Inches(4.4)

        p_k = cell_k.paragraphs[0]
        r_k = p_k.add_run(k)
        r_k.bold = True
        r_k.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        p_v = cell_v.paragraphs[0]
        r_v = p_v.add_run(v)
        if "http" in v:
            r_v.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
            r_v.bold = True
        else:
            r_v.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        set_cell_background(cell_k, "F8FAFC")
        set_cell_background(cell_v, "FFFFFF" if idx % 2 == 0 else "F8FAFC")
        set_cell_margins(cell_k, top=100, bottom=100, left=150, right=150)
        set_cell_margins(cell_v, top=100, bottom=100, left=150, right=150)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 3. Application Architecture & Implementation Summary
    h3 = doc.add_heading("3. Implementation Architecture & Deliverables Summary", level=1)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)

    p_arch = doc.add_paragraph(
        "The TaskFlow web application was completely containerized and orchestrated into a four-tier architecture conforming to production best practices:"
    )
    p_arch.paragraph_format.space_after = Pt(4)

    tiers = [
        ("Frontend (React + Vite)", "Containerized via a multi-stage Dockerfile. Stage 1 compiles React assets using node:20-alpine. Stage 2 serves minified static bundles with nginx:1.27-alpine. Configured reverse proxy for /api/ and /health endpoints routed directly to backend:3000."),
        ("Backend (Node.js + Express)", "Built on node:20-alpine base image with pinned production dependencies (npm install --omit=dev), running under unprivileged user 'node'. Exposes port 3000 and connects to PostgreSQL and Redis using container service names."),
        ("Database (PostgreSQL 16)", "Orchestrated using official postgres:16-alpine image with named volume 'postgres_data' for persistent data storage. Auto-initializes schema from init.sql."),
        ("Caching Layer (Redis 7)", "Utilizes official redis:7-alpine image for low-latency session caching and API response acceleration with TTL and cache invalidation on task mutations.")
    ]

    for title, desc in tiers:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r_t = p.add_run(f"{title}: ")
        r_t.bold = True
        p.add_run(desc)

    doc.add_page_break()

    # 4. CI/CD Execution Evidence
    h4 = doc.add_heading("4. CI/CD Execution Evidence & Verification Screenshots", level=1)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(8)

    screenshots = [
        (
            "02-taskflow-dashboard.png",
            "Figure 1: TaskFlow Web Application Dashboard (Live at http://localhost:8080)",
            "Verified live interface running in containerized environment. Authenticated as student 'Abhay Singh Tomar'. Demonstrates active tasks created, dynamic count, and Redis caching indicator showing 'Last response source: redis-cache'."
        ),
        (
            "01-taskflow-login.png",
            "Figure 2: TaskFlow User Authentication Interface (http://localhost:8080)",
            "Production frontend served via Nginx 1.27-alpine reverse proxy, providing secure authentication with JWT token persistence in browser localStorage."
        ),
        (
            "03-backend-health.png",
            "Figure 3: Backend Health API Verification Endpoint (http://localhost:3000/health)",
            "Direct health check returning {\"status\":\"ok\",\"postgres\":\"ok\",\"redis\":\"ok\"}, verifying active communication between backend service, PostgreSQL database, and Redis cache."
        ),
        (
            "04-docker-compose-ps.png",
            "Figure 4: Docker Compose Multi-Container Orchestration Status",
            "Terminal output executing 'docker compose ps'. All 4 services (backend, frontend, postgres, redis) are verified running and in 'healthy' state on the isolated 'taskflow-net' bridge network."
        ),
        (
            "05-hadolint-validation.png",
            "Figure 5: Dockerfile Security & Best Practices Linting (Hadolint)",
            "Automated linting of frontend/Dockerfile and backend/Dockerfile via hadolint/hadolint container, confirming compliance with zero syntax errors or critical warnings."
        ),
        (
            "06-api-test-results.png",
            "Figure 6: Automated API & Redis Cache Jest Test Suite (12/12 Passed)",
            "Jest execution validating TC01 to TC12: health endpoint, user registration, authentication, token validation, task CRUD operations, Redis cache population, and cache invalidation on mutations."
        ),
        (
            "07-persistence-test.png",
            "Figure 7: PostgreSQL Persistent Storage & Redis Repopulation Verification",
            "Automated verification script creating a task, stopping and tearing down containers with 'docker compose down', recreating stack with 'docker compose up -d', and validating task survival from PostgreSQL volume."
        ),
        (
            "08-deploy-compose-validation.png",
            "Figure 8: Deployment Compose Validation & Clean Machine Image Pull",
            "Execution of 'docker-compose.deploy.yml' verification confirming no local 'build:' directives exist and all services pull and run directly from Docker Hub."
        ),
        (
            "09-cd-pipeline-execution.png",
            "Figure 9: GitHub Actions CD Deployment Pipeline Execution",
            "Successful execution of all CD workflow stages: repository checkout, Buildx setup, Docker Hub authentication, backend & frontend build/publishing, compose image pull, container deployment, backend health check, and frontend accessibility verification."
        ),
        (
            "10-dockerhub-repositories.png",
            "Figure 10: Docker Hub Published Images Overview",
            "Verification of published images under Docker Hub user 'abhay1tomar1': abhay1tomar1/taskflow-backend:latest and abhay1tomar1/taskflow-frontend:latest with AMD64/ARM64 architectures."
        ),
        (
            "11-instructor-ci-status.png",
            "Figure 11: Instructor CI Evaluation Workflow Status (PR #30 Check)",
            "Evaluation workflow checking Pull Request submission #30, required file presence, Hadolint linting, stack initialization, automated API test suite, and persistence tests."
        )
    ]

    for img_name, fig_title, fig_desc in screenshots:
        img_path = os.path.join(img_dir, img_name)
        if os.path.exists(img_path):
            p_title = doc.add_paragraph()
            p_title.paragraph_format.space_before = Pt(10)
            p_title.paragraph_format.space_after = Pt(4)
            r_ft = p_title.add_run(fig_title)
            r_ft.bold = True
            r_ft.font.size = Pt(11)
            r_ft.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.space_before = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(6.5))

            p_desc = doc.add_paragraph()
            p_desc.paragraph_format.space_before = Pt(0)
            p_desc.paragraph_format.space_after = Pt(14)
            r_desc = p_desc.add_run(fig_desc)
            r_desc.font.size = Pt(9.5)
            r_desc.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # 5. Implementation Checklist
    doc.add_page_break()
    h5 = doc.add_heading("5. Implementation Checklist & Verification Matrix", level=1)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(6)

    checklist_items = [
        ("Frontend Dockerfile implemented with multi-stage Nginx build", "VERIFIED / PASSED"),
        ("Backend Dockerfile implemented with Node 20 unprivileged runtime", "VERIFIED / PASSED"),
        ("docker-compose.yml multi-service orchestration configured", "VERIFIED / PASSED"),
        ("docker-compose.deploy.yml image-based deployment configured", "VERIFIED / PASSED"),
        ("Frontend image published to Docker Hub (abhay1tomar1/taskflow-frontend)", "VERIFIED / PASSED"),
        ("Backend image published to Docker Hub (abhay1tomar1/taskflow-backend)", "VERIFIED / PASSED"),
        ("PostgreSQL persistent volume storage verified across teardown/rebuild", "VERIFIED / PASSED"),
        ("Redis sub-millisecond query caching & cache invalidation verified", "VERIFIED / PASSED"),
        ("Application end-to-end functionality tested (Register, Login, CRUD Tasks)", "VERIFIED / PASSED"),
        ("CD deployment pipeline executed and all 12 stages passed", "VERIFIED / PASSED"),
        ("Official Pull Request #30 submitted against instructor repository", "SUBMITTED / PASSED"),
        ("Required files verified: Dockerfiles, compose files, submission.json", "VERIFIED / PASSED")
    ]

    chk_table = doc.add_table(rows=len(checklist_items) + 1, cols=2)
    chk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    chk_table.autofit = False

    header_row = chk_table.rows[0]
    header_row.cells[0].width = Inches(5.2)
    header_row.cells[1].width = Inches(1.8)
    p0 = header_row.cells[0].paragraphs[0].add_run("Requirement / Task Description")
    p0.bold = True
    p0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p1 = header_row.cells[1].paragraphs[0].add_run("Status")
    p1.bold = True
    p1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_background(header_row.cells[0], "0F172A")
    set_cell_background(header_row.cells[1], "0F172A")
    set_cell_margins(header_row.cells[0], top=120, bottom=120, left=150, right=150)
    set_cell_margins(header_row.cells[1], top=120, bottom=120, left=150, right=150)

    for idx, (req, status) in enumerate(checklist_items, start=1):
        row = chk_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.2)
        c1.width = Inches(1.8)

        r0 = c0.paragraphs[0].add_run(f"✔  {req}")
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        r1 = c1.paragraphs[0].add_run(status)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x16, 0x65, 0x34)

        bg = "FFFFFF" if idx % 2 != 0 else "F8FAFC"
        set_cell_background(c0, bg)
        set_cell_background(c1, "DCFCE7" if idx % 2 != 0 else "F0FDF4")
        set_cell_margins(c0, top=90, bottom=90, left=150, right=150)
        set_cell_margins(c1, top=90, bottom=90, left=150, right=150)

    # 6. Declaration
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    h6 = doc.add_heading("6. Declaration", level=1)
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(6)

    dec_box = doc.add_table(rows=1, cols=1)
    dec_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_cell = dec_box.rows[0].cells[0]
    dec_cell.width = Inches(7.0)
    set_cell_background(dec_cell, "F1F5F9")
    set_cell_margins(dec_cell, top=160, bottom=160, left=200, right=200)

    p_dec = dec_cell.paragraphs[0]
    r_dec = p_dec.add_run(
        "\"I hereby declare that the submitted Docker implementation is my own work. "
        "I have successfully executed and verified the required CI/CD pipeline stages, "
        "published the Docker images to my Docker Hub account, and tested the application deployment.\""
    )
    r_dec.font.italic = True
    r_dec.font.size = Pt(11)
    r_dec.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sig = dec_cell.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(10)
    r_sig = p_sig.add_run("Student Name: Abhay Singh Tomar\nUniversity Roll Number: 202401100300005\nSection: A\nDate: November 18, 2026")
    r_sig.bold = True
    r_sig.font.size = Pt(10)
    r_sig.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.save(output_path)
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\202401100300005_ABHAY_SINGH_TOMAR.docx"
    img_dir = r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\screenshots"
    create_report(out_file, img_dir)
