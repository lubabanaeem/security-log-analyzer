# Security Log Analyzer (Django)

A web-based Security Log Analyzer built with **Python** and **Django** that allows users to upload log files, detect suspicious login activity, store analysis results in a database, and view the findings through a simple dashboard.

---

## Features
## Features

- User authentication (Login/Logout)
- Upload `.log` and `.txt` log files
- Parse security logs
- Detect suspicious IP addresses
- Brute-force attack detection using configurable thresholds
- Store analysis results in SQLite database
- Dashboard with summary statistics
- Search and filter alerts
- Interactive charts and visualizations
- Export reports as PDF 
- Django Admin panel for database management


---

## Tech Stack

- Python
- Django
- SQLite
- HTML
- Bootstrap 5

---

## Project Structure

```
log_analyzer_web/
│
├── analyzer/
│   ├── detector.py
│   ├── log_parser.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── migrations/
│
├── media/
├── core/
├── manage.py
└── db.sqlite3
```

---

## Detection Logic

The analyzer:

1. Reads uploaded log files.
2. Extracts failed login attempts.
3. Counts failed attempts for each IP.
4. Records the first time an IP appears.
5. Compares failed attempts against a threshold.
6. Classifies activity as:
   - **HIGH** → Suspicious / Possible brute-force attack
   - **NORMAL** → Normal activity

---

## Database Models

### UploadedLogs
Stores uploaded log files and upload timestamps.

### Alerts
Stores:
- IP address
- Severity
- Alert message
- Creation time

### DetectedIp
Stores suspicious IP addresses including:
- IP address
- Failed attempt count
- First seen date
- First seen time

### ReportHistory
Stores report metadata:
- Upload reference
- Report generation time
- Total alerts

---

## Dashboard

The dashboard displays:

- Total alerts
- High severity alerts
- Suspicious IP count
- Latest uploaded file
- Alert details
- Suspicious IP details
- Report summary

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/security-log-analyzer.git
cd security-log-analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Example Workflow

1. Upload a `.log` or `.txt` file.
2. The file is validated.
3. Logs are parsed.
4. Failed login attempts are analyzed.
5. Alerts and suspicious IPs are stored in the database.
6. Results are displayed on the dashboard.

---

## Future Improvements

- Email notifications for high-severity alerts
- Real-time log monitoring
- Support for additional log formats
- Configurable detection rules through the UI
- REST API for external integrations

---

## Author

**Lubaba Naeem**

Software Engineering Student

---

## License

This project is for educational and portfolio purposes.
