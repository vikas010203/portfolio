import json
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
CONTACT_LOG_PATH = BASE_DIR / "contact_messages.json"


def load_contact_messages():
    if not CONTACT_LOG_PATH.exists():
        return []
    try:
        with CONTACT_LOG_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_contact_messages(messages):
    with CONTACT_LOG_PATH.open("w", encoding="utf-8") as fh:
        json.dump(messages, fh, indent=2)


app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

PROFILE = {
    "name": "Vikas Marothia",
    "title": "Software Development Engineer",
    "location": "Panchkula, India",
    "phone": "+91 8529766054",
    "email": "vikasmarothia37@gmail.com",
    "github": "https://github.com/vikas010203",
    "linkedin": "https://www.linkedin.com/in/vikas-marothia",
    "summary": "Backend-focused SDE with 2+ years building scalable, fault-tolerant systems for a US-based enterprise SaaS platform. Owns features end-to-end — API design through deployment and production support — with a track record of measurable performance and reliability gains.",
    "skills": {
        "Languages": ["Python", "JavaScript", "SQL"],
        "Frameworks": ["Flask", "FastAPI", "Django", "REST API Design", "Microservices"],
        "Databases": ["PostgreSQL", "MongoDB", "MySQL", "Indexing", "Query Optimization", "Schema Design"],
        "Cloud & Infra": ["AWS Lambda", "S3", "CloudWatch", "EventBridge", "Serverless", "CI/CD"],
        "Integrations": ["QuickBooks Desktop", "Sage Intacct", "NetSuite", "Gemini", "IronSight"],
        "Data Engineering": ["Pandas", "NumPy", "ETL Pipelines", "Data Validation"],
        "Tools": ["Git", "Jira", "Postman", "Agile/Scrum", "Code Reviews", "On-call Ops"],
    },
    "experience": [
        {
            "role": "Software Development Engineer",
            "company": "Bursys Infotech India Pvt. Ltd.",
            "period": "Aug 2024 – Present",
            "highlight": "FieldEquip — multi-tenant enterprise SaaS serving 50+ clients across oil & gas, manufacturing, and logistics.",
            "points": [
                "Owned end-to-end delivery of high-performance REST APIs (Flask, FastAPI) handling 10K+ daily requests across web and mobile.",
                "Built 5 enterprise integrations (QuickBooks Desktop, Sage Intacct, NetSuite, Gemini, IronSight), eliminating manual data reconciliation for US customers.",
                "Architected event-driven serverless pipelines (Lambda, EventBridge, S3), cutting infra costs 15% while auto-scaling for 3x traffic spikes.",
                "Optimized PostgreSQL/MongoDB via indexing and schema redesign — +20% query throughput and -35% p95 latency.",
                "Engineered ETL pipelines (Python/Pandas) processing 100K+ records/day, improving downstream data reliability 40%.",
                "Automated reporting workflows, cutting manual effort 30% and turning decision turnaround from 3 days to same-day.",
                "Led root-cause analysis on production incidents, driving system uptime to 99.5%+.",
            ],
        },
        {
            "role": "Process Analyst",
            "company": "eClerx Services Ltd.",
            "period": "Dec 2023 – Apr 2024",
            "highlight": "Resolved 200+ technical escalations for US/UK clients with 98%+ SLA compliance; top performer.",
            "points": [
                "Resolved 200+ technical escalations for US/UK clients with 98%+ SLA compliance; top performer.",
                "Identified 5 recurring issue patterns, cutting average ticket resolution time 15%.",
            ],
        },
        {
            "role": "Software Engineering Intern",
            "company": "ThinkNext Technologies Pvt. Ltd.",
            "period": "Feb 2022 – Aug 2022",
            "highlight": "Built reusable Django modules and REST endpoints; shipped 3 production-ready features in an Agile team.",
            "points": [
                "Built reusable Django modules and REST endpoints; shipped 3 production-ready features in an Agile team.",
            ],
        },
    ],
    "projects": [
        {
            "name": "FieldEquip",
            "stack": ["Flask", "FastAPI", "PostgreSQL", "MongoDB", "AWS Lambda"],
            "description": "Multi-tenant enterprise SaaS built for industries including oil & gas, manufacturing, and logistics.",
            "details": [
                "Core contributor to scalable APIs and enterprise integrations across ERP and platform workflows.",
                "Built automated data pipelines across industry verticals to reduce reconciliation effort and improve operational visibility.",
            ],
        },
        {
            "name": "Automated Reporting Engine",
            "stack": ["Python", "Pandas", "AWS S3"],
            "description": "End-to-end pipeline automating CSV ingestion and cleaning to accelerate reporting operations.",
            "details": [
                "Automated CSV ingestion and cleaning, reducing manual effort 30% and enabling same-day decision support.",
            ],
        },
    ],
    "education": [
        {
            "degree": "B.Tech, Computer Science & Engineering",
            "school": "Chandigarh Engineering College, Mohali",
            "period": "2018 – 2022",
            "meta": "CGPA: 7.6/10",
        }
    ],
    "certifications": [
        "Python & Django Development — ThinkNext Technologies",
        "Full Stack Development — Coding Blocks",
    ],
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=PROFILE["skills"],
        experience=PROFILE["experience"],
        projects=PROFILE["projects"],
        education=PROFILE["education"],
        certifications=PROFILE["certifications"],
    )


@app.route("/resume")
def resume_download():
    return send_from_directory(str(BASE_DIR / "static" / "resume"), "Vikas_Marothia_Resume.pdf", as_attachment=True)


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, subject, message]):
        flash("Please fill in all fields before submitting the form.", "error")
        return redirect(url_for("home", _anchor="contact"))

    payload = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }

    messages = load_contact_messages()
    messages.insert(0, payload)
    save_contact_messages(messages[:50])

    smtp_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", "587"))
    username = os.getenv("MAIL_USERNAME", "")
    password = os.getenv("MAIL_PASSWORD", "")
    mail_to = os.getenv("MAIL_TO", username or "vikasmarothia37@gmail.com")

    email_message = EmailMessage()
    email_message["Subject"] = f"Portfolio Inquiry: {subject}"
    email_message["From"] = username or "noreply@localhost"
    email_message["To"] = mail_to
    email_message.set_content(
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    try:
        if username and password:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(email_message)
            flash("Your message has been sent successfully. Thank you for reaching out.", "success")
        else:
            print("MAIL credentials are not set. Contact form submission captured in server logs:")
            print(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
            flash(
                "Your message has been captured locally because live mail credentials have not been configured yet. Add MAIL_USERNAME and MAIL_PASSWORD to enable email delivery.",
                "warning",
            )
    except Exception as exc:  # pragma: no cover - operational runtime handling
        app.logger.exception("Failed to send portfolio message")
        flash(f"There was a problem sending your message: {exc}", "error")

    return redirect(url_for("home", _anchor="contact"))


@app.route("/admin")
def admin_dashboard():
    messages = load_contact_messages()
    return render_template("admin.html", messages=messages)


@app.route("/admin/clear")
def clear_messages():
    save_contact_messages([])
    flash("Contact log cleared.", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
