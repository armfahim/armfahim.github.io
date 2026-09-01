# -*- coding: utf-8 -*-
"""Generate a privacy-cleaned CV PDF for A.R.M. Fahim, styled to match the portfolio."""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle

# ---- palette (matches portfolio) ----
INK     = HexColor("#12151d")
BODY    = HexColor("#333a49")
DIM     = HexColor("#6b7488")
BRAND   = HexColor("#6366f1")
ACCENT  = HexColor("#0e9bb0")
LINE    = HexColor("#e2e6f0")

# Output next to the site's assets, resolved relative to this script
# (tools/make_cv.py -> ../assets/A.R.M.-Fahim-CV.pdf), so it works from any cwd.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(_ROOT, "assets", "A.R.M.-Fahim-CV.pdf")

styles = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=21, leading=23,
                            textColor=INK, spaceAfter=1),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10.5, leading=12,
                            textColor=BRAND, spaceAfter=4),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.5, leading=11,
                              textColor=DIM),
    "summary": ParagraphStyle("summary", fontName="Helvetica", fontSize=8.8, leading=11.6,
                              textColor=BODY, spaceBefore=1),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=12,
                         textColor=INK, spaceBefore=2, spaceAfter=1),
    "job": ParagraphStyle("job", fontName="Helvetica-Bold", fontSize=9.8, leading=12,
                          textColor=INK),
    "org": ParagraphStyle("org", fontName="Helvetica-Bold", fontSize=9, leading=11,
                          textColor=ACCENT, spaceAfter=0),
    "date": ParagraphStyle("date", fontName="Helvetica", fontSize=8, leading=11,
                           textColor=DIM, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.5, leading=11,
                             textColor=BODY, leftIndent=10, bulletIndent=0, spaceAfter=0.5),
    "proj": ParagraphStyle("proj", fontName="Helvetica-Bold", fontSize=9, leading=11,
                           textColor=INK),
    "projrole": ParagraphStyle("projrole", fontName="Helvetica-Oblique", fontSize=8,
                               leading=10, textColor=ACCENT),
    "tech": ParagraphStyle("tech", fontName="Helvetica", fontSize=8, leading=10.5,
                           textColor=DIM),
    "skillcat": ParagraphStyle("skillcat", fontName="Helvetica-Bold", fontSize=8.5,
                               leading=11, textColor=INK),
    "skillval": ParagraphStyle("skillval", fontName="Helvetica", fontSize=8.5, leading=11,
                               textColor=BODY),
}


def section(title):
    return [
        Spacer(1, 2),
        Paragraph(title.upper(), ParagraphStyle("st", parent=styles["h2"], textColor=BRAND)),
        HRFlowable(width="100%", thickness=1.1, color=BRAND, spaceBefore=1, spaceAfter=3),
    ]


def job_header(title, org, date):
    t = Table(
        [[Paragraph(title, styles["job"]), Paragraph(date, styles["date"])]],
        colWidths=[118 * mm, 47 * mm],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [t, Paragraph(org, styles["org"])]


def bullets(items):
    return [Paragraph("• " + b, styles["bullet"]) for b in items]


def skill_row(cat, val):
    t = Table(
        [[Paragraph(cat, styles["skillcat"]), Paragraph(val, styles["skillval"])]],
        colWidths=[34 * mm, 131 * mm],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t


def project_cell(title, role, tech):
    return [
        Paragraph(title, styles["proj"]),
        Paragraph(role, styles["projrole"]),
        Paragraph("<font color='#6b7488'>Tech:</font> " + tech, styles["tech"]),
    ]


def projects_grid(items):
    rows = []
    for i in range(0, len(items), 2):
        left = project_cell(*items[i])
        right = project_cell(*items[i + 1]) if i + 1 < len(items) else []
        rows.append([left, right])
    t = Table(rows, colWidths=[82 * mm, 83 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


story = []

# ---- Header ----
story.append(Paragraph("A.R.M. Fahim", styles["name"]))
story.append(Paragraph("SOFTWARE ENGINEER &nbsp;·&nbsp; JAVA &amp; SPRING BOOT", styles["role"]))
contact = (
    'Dhaka, Bangladesh &nbsp;&nbsp;|&nbsp;&nbsp; '
    '<a href="mailto:armfahim4010@gmail.com"><font color="#6366f1">armfahim4010@gmail.com</font></a> '
    '&nbsp;&nbsp;|&nbsp;&nbsp; '
    '<a href="https://www.linkedin.com/in/a-r-m-fahim-9b5006122/"><font color="#6366f1">LinkedIn</font></a> '
    '&nbsp;&nbsp;|&nbsp;&nbsp; '
    '<a href="https://armfahim.github.io"><font color="#6366f1">armfahim.github.io</font></a>'
)
story.append(Paragraph(contact, styles["contact"]))
story.append(Spacer(1, 3))
story.append(HRFlowable(width="100%", thickness=1.4, color=LINE, spaceBefore=3, spaceAfter=2))

# ---- Summary ----
story += section("Summary")
story.append(Paragraph(
    "Software Engineer with 6+ years building reliable, scalable backend systems in Java and Spring Boot. "
    "Experienced across healthcare, enterprise, and data-driven platforms — designing RESTful APIs, "
    "optimizing database performance, and delivering clean, maintainable, object-oriented code. "
    "Committed to hard work, effective under pressure, and focused on building enduring relationships in software engineering.",
    styles["summary"]))

# ---- Skills ----
story += section("Skills")
story.append(skill_row("Backend", "Java, Spring Boot, Spring Data JPA, Spring MVC, Spring Security &amp; JWT, Hibernate, RESTful APIs, Java EE / EJB"))
story.append(skill_row("Databases", "SQL, MSSQL Server, PostgreSQL, Query Optimization"))
story.append(skill_row("Frontend", "Angular, HTML, CSS, Bootstrap"))
story.append(skill_row("Tools &amp; Practices", "JasperReports, Maven, Apache Tomcat, Selenium, Jsoup, Grafana, Redash, Agile &amp; Scrum"))
story.append(skill_row("Languages", "Bangla (Native), English (Professional)"))

# ---- Experience ----
story += section("Professional Experience")

story += job_header("Software Engineer", "United Hospital Limited", "Jun 2025 – Present")
story += bullets([
    "Develop and maintain Hospital Management System modules using Java, Spring Boot, and SQL.",
    "Design and implement scalable RESTful APIs for clinical and operational workflows.",
    "Optimize database queries and enhance system performance for high-concurrency usage.",
    "Debug and resolve production issues, ensuring system stability and minimal downtime.",
    "Awarded Certification of Appreciation for outstanding contribution.",
])
story.append(Spacer(1, 2.5))

story += job_header("Software Engineer", "Ethics Advance Technology Limited", "Mar 2023 – May 2025")
story += bullets([
    "Built applications with Java 17, Spring Boot, Spring Data JPA, Spring MVC, and SQL.",
    "Developed and optimized high-performance APIs following architectural standards.",
    "Wrote clean, maintainable, object-oriented code and enhanced existing applications.",
    "Designed and developed reports using JasperReports (templates and subreports).",
    "Wrote and optimized complex SQL queries for efficient data retrieval and reporting.",
])
story.append(Spacer(1, 2.5))

story += job_header("Software Engineer", "One Direction Companies Ltd.", "Nov 2021 – Feb 2023")
story += bullets([
    "Developed applications using Java EE, Spring Boot, Spring Data JPA, SQL, and Angular.",
    "Built RESTful web services and integrated the Angular frontend with backend APIs.",
    "Designed responsive user interfaces following Angular best practices.",
    "Integrated JasperReports with Java and rendered reports in the Angular frontend.",
    "Deployed Java and Angular projects on Apache Tomcat.",
])
story.append(Spacer(1, 2.5))

story += job_header("Jr. Software Developer", "Naztech Inc Ltd.", "Jan 2020 – Oct 2021")
story += bullets([
    "Worked with Java, Enterprise Java Beans (EJB), and Java EE; hands-on with Spring and Spring Boot.",
    "Used JPA and Hibernate; delivered code across testing and implementation in an agile environment.",
    "Built mail templating with Mustache &amp; FreeTemplateMaker.",
    "Implemented web scraping using Selenium, Jsoup, and HtmlUnit; built Grafana &amp; Redash dashboards.",
])

# ---- Projects ----
story += section("Key Projects")
story.append(projects_grid([
    ("Hospital Management System", "Software Engineer",
     "Java EE 1.8, Spring Boot 3, Spring Data JPA, Angular, RESTful APIs, JasperReports, Maven, SQL"),
    ("Job Harvester &amp; Talent-Array", "Backend Developer",
     "Java EE 1.8, Spring Boot 3, JPA, MSSQL Server, Selenium, Jsoup, HtmlUnit"),
    ("Institutional Web Portal (IWP)", "Backend Developer",
     "Java EE 1.8, Spring Boot, JPA, MSSQL, RESTful APIs"),
    ("Land Management System", "Software Engineer",
     "Spring Boot 3, Angular 11, Spring Security &amp; JWT, JPA, PostgreSQL, Maven, RESTful APIs"),
]))

# ---- Education ----
story += section("Education")
story += job_header("BSc in Computer Science &amp; Software Engineering",
                    "American International University – Bangladesh (AIUB)", "2015 – 2019")

story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceAfter=2))
story.append(Paragraph("References available upon request.",
                       ParagraphStyle("ref", fontName="Helvetica-Oblique", fontSize=8.5,
                                      textColor=DIM, alignment=1)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(DIM)
    canvas.drawString(18 * mm, 10 * mm, "A.R.M. Fahim — Software Engineer")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "armfahim.github.io")
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=16 * mm, rightMargin=16 * mm,
    topMargin=12 * mm, bottomMargin=13 * mm,
    title="A.R.M. Fahim - CV", author="A.R.M. Fahim",
    subject="Curriculum Vitae",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF written:", OUT)
