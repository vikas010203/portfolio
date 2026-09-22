# Vikas Marothia | Portfolio

A professional portfolio website built with Flask for a backend-focused software engineer profile. The site showcases experience, projects, skills, certifications, and a contact workflow for recruiters and clients.

## Overview
This portfolio includes:
- A modern, responsive landing page
- Experience and project highlights
- Resume download section
- Contact form with local logging and optional email delivery
- Admin dashboard to view and clear contact submissions

## Tech Stack
- Python
- Flask
- HTML/CSS/JavaScript
- JSON-based message storage

## Prerequisites
Before running the project, ensure you have:
- Python 3.10 or newer
- pip
- A virtual environment tool such as venv

## Getting Started
Clone the project and navigate to the project directory:

```bash
git clone <repository-url>
cd portfolio
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

The app will be available at:

```text
http://127.0.0.1:5000
```

## Configuration
The application supports optional email configuration for the contact form. These environment variables can be set before running the app:

```bash
export SECRET_KEY="your-secret-key"
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-app-password"
export MAIL_TO="recipient@example.com"
```

On Windows PowerShell:

```powershell
$env:SECRET_KEY = "your-secret-key"
$env:MAIL_SERVER = "smtp.gmail.com"
$env:MAIL_PORT = "587"
$env:MAIL_USERNAME = "your-email@gmail.com"
$env:MAIL_PASSWORD = "your-app-password"
$env:MAIL_TO = "recipient@example.com"
```

If email credentials are not configured, the contact form still works locally and stores messages in a JSON file.

## Deployment
This project is ready to be deployed on platforms such as:
- Render
- Railway
- PythonAnywhere
- Heroku
- Any standard Python hosting platform

## Notes
Using absolute local paths like `E:\Python Workspace\...` is not portable and should be avoided in project documentation. This README uses repository-relative instructions so it can work on any machine.
