# Jira Data Sync Platform

## Prerequisites

* Python 3.12+
* Jira Cloud Account
* Jira API Token

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>

cd jira-mcp-app
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install flask
pip install flask-sqlalchemy
pip install requests
pip install python-dotenv
```

---

## Environment Configuration

Create a `.env` file in the project root.

```env
JIRA_BASE_URL=https://your-company.atlassian.net

JIRA_EMAIL=your-email@example.com

JIRA_API_TOKEN=your-jira-api-token
```

Example:

```env
JIRA_BASE_URL=https://company.atlassian.net

JIRA_EMAIL=test@gmail.com

JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxx
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

Expected Output:

```text
* Running on http://127.0.0.1:5000
```

Application URL:

```text
http://localhost:5000
```

---

# Postman API Testing

Base URL:

```text
http://localhost:5000
```

---

## Health Check

### Request

```http
GET /
```

### URL

```text
http://localhost:5000/
```

---

## Project Sync

### Request

```http
GET /sync/projects
```

### URL

```text
http://localhost:5000/sync/projects
```

---

## Issue Sync

### Request

```http
GET /sync/issues
```

### URL

```text
http://localhost:5000/sync/issues
```

---

## Comment Sync

### Request

```http
GET /sync/comments
```

### URL

```text
http://localhost:5000/sync/comments
```

---

## History Sync

### Request

```http
GET /sync/history
```

### URL

```text
http://localhost:5000/sync/history
```

---

## Sync All

Runs Project Sync → Issue Sync → Comment Sync → History Sync.

### Request

```http
GET /sync/all
```

### URL

```text
http://localhost:5000/sync/all
```

---

## Recommended Testing Order

1. Health Check

```text
GET /
```

2. Project Sync

```text
GET /sync/projects
```

3. Issue Sync

```text
GET /sync/issues
```

4. Comment Sync

```text
GET /sync/comments
```

5. History Sync

```text
GET /sync/history
```

6. Full Synchronization

```text
GET /sync/all
```
