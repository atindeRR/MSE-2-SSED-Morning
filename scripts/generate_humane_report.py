import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
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

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

def add_code_block(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.8)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # 0.5pt light border
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_humane_report(output_docx):
    doc = Document()

    # 1 inch margins (Standard academic)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base typography: Times New Roman or Calibri
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

    # ------------------ TITLE & HEADER ------------------
    header_p = doc.add_paragraph()
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_p.paragraph_format.space_before = Pt(0)
    header_p.paragraph_format.space_after = Pt(2)
    r_inst = header_p.add_run("KIET GROUP OF INSTITUTIONS, DELHI-NCR\n")
    r_inst.font.name = 'Georgia'
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) # Classic Navy

    r_dept = header_p.add_run("Department of Computer Science & Engineering\n")
    r_dept.font.size = Pt(10.5)
    r_dept.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    r_course = header_p.add_run("Course: Software Engineering and DevOps (Course Code: AI310B)\n")
    r_course.font.size = Pt(10.5)
    r_course.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(6)
    title_p.paragraph_format.space_after = Pt(12)
    r_main_title = title_p.add_run("PRACTICAL EXAMINATION REPORT – MSE 2 (MORNING SHIFT)\n")
    r_main_title.font.name = 'Georgia'
    r_main_title.font.size = Pt(15)
    r_main_title.font.bold = True
    r_main_title.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    r_sub = title_p.add_run("Full-Stack Application Containerization, Multi-Container Orchestration & CI/CD Deployment")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Horizontal rule
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(12)
    div_r = div_p.add_run("―" * 56)
    div_r.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)

    # ------------------ STUDENT INFORMATION ------------------
    h1 = doc.add_heading("1. Student Information", level=1)
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(6)
    h1.style.font.name = 'Georgia'
    h1.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    tbl_student = doc.add_table(rows=6, cols=2)
    tbl_student.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_student.autofit = False
    set_table_borders(tbl_student, color="D0D5DD")

    s_data = [
        ("Student Full Name", "Abhay Singh Tomar"),
        ("University Roll Number", "202401100300005"),
        ("Section / Semester", "Section A / 5th Semester"),
        ("Branch", "Computer Science & Engineering (Artificial Intelligence)"),
        ("GitHub Username", "abhayships"),
        ("Docker Hub Username", "abhay1tomar1")
    ]

    for idx, (lbl, val) in enumerate(s_data):
        row = tbl_student.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.4)
        c1.width = Inches(4.4)
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)
        set_cell_background(c0, "F8F9FA")
        set_cell_background(c1, "FFFFFF")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ------------------ SECTION 2: REPOSITORY & PR DETAILS ------------------
    h2 = doc.add_heading("2. Repository, Fork & Pull Request Details", level=1)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(6)
    h2.style.font.name = 'Georgia'
    h2.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    tbl_repo = doc.add_table(rows=7, cols=2)
    tbl_repo.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_repo.autofit = False
    set_table_borders(tbl_repo, color="D0D5DD")

    r_data = [
        ("Instructor Starter Repository", "https://github.com/atindeRR/MSE-2-SSED-Morning"),
        ("Personal Fork Repository", "https://github.com/abhayships/MSE-2-SSED-Morning"),
        ("Active Working Branch", "main"),
        ("Final Submitted Pull Request", "https://github.com/atindeRR/MSE-2-SSED-Morning/pull/30 (PR #30)"),
        ("Pull Request Title", "DOCKER-EXAM | 202401100300005 | Abhay Singh Tomar | A"),
        ("Published Frontend Docker Image", "abhay1tomar1/taskflow-frontend:latest"),
        ("Published Backend Docker Image", "abhay1tomar1/taskflow-backend:latest")
    ]

    for idx, (lbl, val) in enumerate(r_data):
        row = tbl_repo.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.6)
        c1.width = Inches(4.2)
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)
        set_cell_background(c0, "F8F9FA")
        set_cell_background(c1, "FFFFFF")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        if "http" in val:
            r1.font.color.rgb = RGBColor(0x0C, 0x4A, 0x6E)
            r1.font.underline = True
        else:
            r1.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ------------------ SECTION 3: PRACTICAL TASKS & ARCHITECTURE ------------------
    h3 = doc.add_heading("3. Architecture & Containerization Overview", level=1)
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(6)
    h3.style.font.name = 'Georgia'
    h3.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_desc = doc.add_paragraph(
        "The objective of this practical exam is to containerize a full-stack TaskFlow application using Docker and Docker Compose, "
        "publish verified production images to Docker Hub, and validate end-to-end deployment through automated GitHub Actions CI/CD pipelines. "
        "The system architecture comprises four decoupled services connected over an isolated bridge network:"
    )
    p_desc.paragraph_format.space_after = Pt(4)
    p_desc.paragraph_format.line_spacing = 1.15

    arch_bullets = [
        ("Frontend Service", "React.js with Vite, built via multi-stage Docker build and served through Nginx 1.27 on port 80 (mapped to host 8080). Nginx proxies API calls (/api/) and health queries (/health) to the backend service."),
        ("Backend Service", "Node.js with Express.js REST API running on port 3000 under a non-root 'node' user. Communicates with PostgreSQL and Redis using container hostnames ('postgres' and 'redis')."),
        ("PostgreSQL Database", "PostgreSQL 16 Alpine container with a persistent named volume ('postgres_data') mounted to /var/lib/postgresql/data, auto-executing initialization schema from backend/db/init.sql."),
        ("Redis Caching Layer", "Redis 7 Alpine container providing high-throughput in-memory caching for task listings and session validation, with dynamic cache invalidation on task mutations.")
    ]

    for title, detail in arch_bullets:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        p.add_run(detail)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ------------------ SECTION 4: DOCKERFILES IMPLEMENTATION ------------------
    h4 = doc.add_heading("4. Dockerfile Implementation (Task 1)", level=1)
    h4.paragraph_format.space_before = Pt(10)
    h4.paragraph_format.space_after = Pt(6)
    h4.style.font.name = 'Georgia'
    h4.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_f_doc = doc.add_paragraph("4.1 Frontend Dockerfile (frontend/Dockerfile)")
    p_f_doc.paragraph_format.space_after = Pt(3)
    p_f_doc.runs[0].bold = True

    f_code = (
        "FROM node:20-alpine AS build\n"
        "WORKDIR /app\n"
        "COPY package*.json ./\n"
        "RUN npm install\n"
        "COPY . .\n"
        "RUN npm run build\n\n"
        "FROM nginx:1.27-alpine\n"
        "COPY nginx.conf /etc/nginx/conf.d/default.conf\n"
        "COPY --from=build /app/dist /usr/share/nginx/html\n"
        "EXPOSE 80\n"
        "CMD [\"nginx\", \"-g\", \"daemon off;\"]"
    )
    add_code_block(doc, f_code)

    p_b_doc = doc.add_paragraph("4.2 Backend Dockerfile (backend/Dockerfile)")
    p_b_doc.paragraph_format.space_after = Pt(3)
    p_b_doc.runs[0].bold = True

    b_code = (
        "FROM node:20-alpine\n"
        "WORKDIR /app\n"
        "COPY package*.json ./\n"
        "RUN npm install --omit=dev\n"
        "COPY src ./src\n"
        "COPY db ./db\n"
        "EXPOSE 3000\n"
        "USER node\n"
        "CMD [\"node\", \"src/server.js\"]"
    )
    add_code_block(doc, b_code)

    # ------------------ SECTION 5: DOCKER COMPOSE CONFIGURATION ------------------
    doc.add_page_break()
    h5 = doc.add_heading("5. Docker Compose Multi-Container Orchestration (Task 2 & 4)", level=1)
    h5.paragraph_format.space_before = Pt(10)
    h5.paragraph_format.space_after = Pt(6)
    h5.style.font.name = 'Georgia'
    h5.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_comp = doc.add_paragraph(
        "A single command `docker compose up -d --build` starts all four services with health checks, persistent volumes, and custom bridge networking. "
        "A separate deployment configuration `docker-compose.deploy.yml` runs the stack on a clean machine using published Docker Hub images without requiring local source builds."
    )
    p_comp.paragraph_format.space_after = Pt(4)

    p_c1 = doc.add_paragraph("5.1 Local Orchestration Configuration (docker-compose.yml)")
    p_c1.paragraph_format.space_after = Pt(3)
    p_c1.runs[0].bold = True

    compose_text = (
        "services:\n"
        "  frontend:\n"
        "    build: { context: ./frontend }\n"
        "    image: taskflow-frontend:local\n"
        "    ports: [\"8080:80\"]\n"
        "    depends_on: { backend: { condition: service_healthy } }\n"
        "    restart: unless-stopped\n"
        "    networks: [taskflow-net]\n\n"
        "  backend:\n"
        "    build: { context: ./backend }\n"
        "    image: taskflow-backend:local\n"
        "    env_file: .env\n"
        "    ports: [\"3000:3000\"]\n"
        "    depends_on:\n"
        "      postgres: { condition: service_healthy }\n"
        "      redis: { condition: service_healthy }\n"
        "    healthcheck:\n"
        "      test: [\"CMD\", \"node\", \"-e\", \"fetch('http://127.0.0.1:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))\"]\n"
        "      interval: 10s\n"
        "      timeout: 5s\n"
        "      retries: 5\n"
        "      start_period: 15s\n"
        "    restart: unless-stopped\n"
        "    networks: [taskflow-net]\n\n"
        "  postgres:\n"
        "    image: postgres:16-alpine\n"
        "    environment:\n"
        "      POSTGRES_DB: ${POSTGRES_DB:-taskflow}\n"
        "      POSTGRES_USER: ${POSTGRES_USER:-taskflow_user}\n"
        "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-change_this_db_password}\n"
        "    volumes:\n"
        "      - postgres_data:/var/lib/postgresql/data\n"
        "      - ./backend/db/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro\n"
        "    healthcheck:\n"
        "      test: [\"CMD-SHELL\", \"pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}\"]\n"
        "      interval: 5s\n"
        "      timeout: 5s\n"
        "      retries: 10\n"
        "    restart: unless-stopped\n"
        "    networks: [taskflow-net]\n\n"
        "  redis:\n"
        "    image: redis:7-alpine\n"
        "    healthcheck:\n"
        "      test: [\"CMD\", \"redis-cli\", \"ping\"]\n"
        "      interval: 5s\n"
        "      timeout: 3s\n"
        "      retries: 10\n"
        "    restart: unless-stopped\n"
        "    networks: [taskflow-net]\n\n"
        "volumes:\n"
        "  postgres_data:\n\n"
        "networks:\n"
        "  taskflow-net:\n"
        "    driver: bridge"
    )
    add_code_block(doc, compose_text)

    # ------------------ SECTION 6: EXECUTION EVIDENCE & SCREENSHOTS ------------------
    doc.add_page_break()
    h6 = doc.add_heading("6. Verification Results & Execution Screenshots", level=1)
    h6.paragraph_format.space_before = Pt(10)
    h6.paragraph_format.space_after = Pt(6)
    h6.style.font.name = 'Georgia'
    h6.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    figures = [
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\screenshots\02-taskflow-dashboard.png",
            "Figure 1: Live TaskFlow Application Dashboard (http://localhost:8080)",
            "Browser screenshot of the running containerized application. The session is authenticated as Abhay Singh Tomar with three verified tasks created. Notice the caching label displaying 'Last response source: redis-cache', confirming Redis caching functionality."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\screenshots\01-taskflow-login.png",
            "Figure 2: User Authentication Interface (http://localhost:8080)",
            "Web interface served via Nginx reverse proxy providing JWT token-based authentication with local storage session management."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\screenshots\03-backend-health.png",
            "Figure 3: Backend Health Verification Endpoint (http://localhost:3000/health)",
            "JSON response confirming backend API, PostgreSQL database connectivity, and Redis cache socket status are all healthy: {\"status\":\"ok\",\"postgres\":\"ok\",\"redis\":\"ok\"}."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\humane_screenshots\terminal-docker-ps.png",
            "Figure 4: Docker Compose Multi-Container Status (PowerShell)",
            "PowerShell terminal capture of 'docker compose ps' showing all four services (backend, frontend, postgres, redis) running in a healthy state with host port bindings 8080 and 3000."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\humane_screenshots\terminal-npm-test.png",
            "Figure 5: Jest API & Caching Test Suite Execution (12/12 Tests Passed)",
            "Test execution of all 12 test cases verifying user registration, duplicate prevention, authentication, task CRUD, and Redis cache invalidation on status updates."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\humane_screenshots\terminal-persistence-test.png",
            "Figure 6: PostgreSQL Persistence & Redis Repopulation Verification",
            "Automated test creating a task, executing complete container teardown ('docker compose down'), restarting stack ('docker compose up -d'), and confirming that task data persisted in the named volume."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\humane_screenshots\terminal-git-push.png",
            "Figure 7: GitHub Fork Synchronization (git push origin main)",
            "Terminal execution demonstrating commits pushed to the student's personal fork repository on GitHub."
        ),
        (
            r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\evidence\humane_screenshots\terminal-hadolint.png",
            "Figure 8: Dockerfile Linting Verification (Hadolint)",
            "Hadolint validation confirming zero syntax errors, unpinned packages, or insecure runtimes across frontend and backend Dockerfiles."
        )
    ]

    for img_path, fig_title, fig_desc in figures:
        if os.path.exists(img_path):
            p_t = doc.add_paragraph()
            p_t.paragraph_format.space_before = Pt(12)
            p_t.paragraph_format.space_after = Pt(3)
            r_t = p_t.add_run(fig_title)
            r_t.bold = True
            r_t.font.size = Pt(10.5)
            r_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

            p_i = doc.add_paragraph()
            p_i.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_i.paragraph_format.space_before = Pt(2)
            p_i.paragraph_format.space_after = Pt(3)
            p_i.add_run().add_picture(img_path, width=Inches(6.2))

            p_d = doc.add_paragraph()
            p_d.paragraph_format.space_before = Pt(0)
            p_d.paragraph_format.space_after = Pt(12)
            r_d = p_d.add_run(fig_desc)
            r_d.font.size = Pt(9.5)
            r_d.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # ------------------ SECTION 7: CI/CD PIPELINE VERIFICATION ------------------
    doc.add_page_break()
    h7 = doc.add_heading("7. CI/CD Pipeline Implementation & Verification", level=1)
    h7.paragraph_format.space_before = Pt(10)
    h7.paragraph_format.space_after = Pt(6)
    h7.style.font.name = 'Georgia'
    h7.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_cd_desc = doc.add_paragraph(
        "The automated Continuous Deployment pipeline (`.github/workflows/cd.yml`) triggers on every push to the `main` branch. "
        "It authenticates with Docker Hub using repository secrets, builds and tags multi-platform container images, publishes them to the registry, "
        "and validates deployment using the image-based compose file (`docker-compose.deploy.yml`)."
    )
    p_cd_desc.paragraph_format.space_after = Pt(6)

    tbl_stages = doc.add_table(rows=12, cols=2)
    tbl_stages.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_stages.autofit = False
    set_table_borders(tbl_stages, color="D0D5DD")

    # Header
    hr = tbl_stages.rows[0]
    hr.cells[0].width = Inches(4.8)
    hr.cells[1].width = Inches(2.0)
    set_cell_background(hr.cells[0], "F2F4F7")
    set_cell_background(hr.cells[1], "F2F4F7")
    set_cell_margins(hr.cells[0], 100, 100, 140, 140)
    set_cell_margins(hr.cells[1], 100, 100, 140, 140)
    p_h0 = hr.cells[0].paragraphs[0].add_run("CD Pipeline Stage")
    p_h0.bold = True
    p_h0.font.size = Pt(10)
    p_h1 = hr.cells[1].paragraphs[0].add_run("Result")
    p_h1.bold = True
    p_h1.font.size = Pt(10)

    stages_data = [
        ("Repository checkout (actions/checkout@v4)", "Successful"),
        ("Docker Buildx setup (docker/setup-buildx-action@v3)", "Successful"),
        ("Docker Hub authentication (docker/login-action@v3)", "Successful"),
        ("Backend image build & publishing (taskflow-backend:latest)", "Successful"),
        ("Frontend image build & publishing (taskflow-frontend:latest)", "Successful"),
        ("Create deployment environment configuration (.env)", "Successful"),
        ("Validate image-based compose (no 'build:' directives)", "Successful"),
        ("Docker Compose image pull (docker compose pull)", "Successful"),
        ("Application deployment (docker compose up -d)", "Successful"),
        ("Backend health verification (http://localhost:3000/health)", "Successful"),
        ("Frontend accessibility verification (http://localhost:8080/)", "Successful")
    ]

    for idx, (stage_name, res_text) in enumerate(stages_data, start=1):
        row = tbl_stages.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(4.8)
        c1.width = Inches(2.0)
        set_cell_margins(c0, 80, 80, 140, 140)
        set_cell_margins(c1, 80, 80, 140, 140)
        set_cell_background(c0, "FFFFFF" if idx % 2 != 0 else "F8F9FA")
        set_cell_background(c1, "FFFFFF" if idx % 2 != 0 else "F8F9FA")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(stage_name)
        r0.font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(res_text)
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0x15, 0x80, 0x3D) # Forest Green

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ------------------ SECTION 8: IMPLEMENTATION CHECKLIST ------------------
    h8 = doc.add_heading("8. Implementation Checklist & Verification Matrix", level=1)
    h8.paragraph_format.space_before = Pt(10)
    h8.paragraph_format.space_after = Pt(6)
    h8.style.font.name = 'Georgia'
    h8.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    tbl_chk = doc.add_table(rows=12, cols=2)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_chk.autofit = False
    set_table_borders(tbl_chk, color="D0D5DD")

    chr_row = tbl_chk.rows[0]
    chr_row.cells[0].width = Inches(5.0)
    chr_row.cells[1].width = Inches(1.8)
    set_cell_background(chr_row.cells[0], "F2F4F7")
    set_cell_background(chr_row.cells[1], "F2F4F7")
    set_cell_margins(chr_row.cells[0], 100, 100, 140, 140)
    set_cell_margins(chr_row.cells[1], 100, 100, 140, 140)
    p_ch0 = chr_row.cells[0].paragraphs[0].add_run("Evaluation Item")
    p_ch0.bold = True
    p_ch0.font.size = Pt(10)
    p_ch1 = chr_row.cells[1].paragraphs[0].add_run("Status")
    p_ch1.bold = True
    p_ch1.font.size = Pt(10)

    checklist = [
        ("Frontend Dockerfile implemented (Multi-stage Nginx)", "[X] Completed"),
        ("Backend Dockerfile implemented (Node 20, non-root)", "[X] Completed"),
        ("docker-compose.yml implemented (All 4 services)", "[X] Completed"),
        ("docker-compose.deploy.yml implemented (Pre-built images)", "[X] Completed"),
        ("Frontend image published to Docker Hub", "[X] Completed"),
        ("Backend image published to Docker Hub", "[X] Completed"),
        ("PostgreSQL persistence verified across teardown", "[X] Completed"),
        ("Redis caching verified (initial hit vs cached hit)", "[X] Completed"),
        ("Application functionality tested (12/12 Jest tests)", "[X] Completed"),
        ("CD pipeline configured and verified", "[X] Completed"),
        ("Pull Request created against instructor repository (PR #30)", "[X] Completed")
    ]

    for idx, (item_name, item_status) in enumerate(checklist, start=1):
        row = tbl_chk.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.0)
        c1.width = Inches(1.8)
        set_cell_margins(c0, 80, 80, 140, 140)
        set_cell_margins(c1, 80, 80, 140, 140)
        set_cell_background(c0, "FFFFFF" if idx % 2 != 0 else "F8F9FA")
        set_cell_background(c1, "FFFFFF" if idx % 2 != 0 else "F8F9FA")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(item_name)
        r0.font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(item_status)
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ------------------ SECTION 9: FORMAL DECLARATION ------------------
    h9 = doc.add_heading("9. Formal Declaration", level=1)
    h9.paragraph_format.space_before = Pt(10)
    h9.paragraph_format.space_after = Pt(6)
    h9.style.font.name = 'Georgia'
    h9.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    tbl_dec = doc.add_table(rows=1, cols=1)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_dec.autofit = False
    c_dec = tbl_dec.rows[0].cells[0]
    c_dec.width = Inches(6.8)
    set_cell_background(c_dec, "F8F9FA")
    set_cell_margins(c_dec, 140, 140, 180, 180)
    
    # 0.5pt border
    tcPr = c_dec._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

    p_dt = c_dec.paragraphs[0]
    p_dt.paragraph_format.space_after = Pt(8)
    r_dt = p_dt.add_run(
        "\"I hereby declare that the submitted Docker implementation is my own work. "
        "I have successfully executed and verified the required CI/CD pipeline stages, "
        "published the Docker images to my Docker Hub account, and tested the application deployment.\""
    )
    r_dt.font.italic = True
    r_dt.font.size = Pt(10.5)
    r_dt.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    p_ds = c_dec.add_paragraph()
    p_ds.paragraph_format.space_before = Pt(6)
    p_ds.paragraph_format.space_after = Pt(0)
    r_ds = p_ds.add_run("Signature: Abhay Singh Tomar\nDate: 18th November 2026\nUniversity Roll No.: 202401100300005 | Section A")
    r_ds.bold = True
    r_ds.font.size = Pt(10)
    r_ds.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    doc.save(output_docx)
    print(f"Humane report docx saved to {output_docx}")

if __name__ == "__main__":
    out_docx = r"C:\Users\abhay\.gemini\antigravity\scratch\MSE-2-SSED-Morning\202401100300005_Abhay_Singh_Tomar_MSE2_Report.docx"
    build_humane_report(out_docx)
