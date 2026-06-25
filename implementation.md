# Jira Data Sync Platform

A Flask-based Jira Data Synchronization platform that syncs Jira Cloud data into a local SQLite database. This project serves as the foundation for a future Jira MCP AI Agent.

---

# Features

## Current Features

* Project Sync
* Issue Sync
* Comment Sync
* History (Changelog) Sync
* SQLite Persistence
* Incremental Issue Sync
* Sync Metadata Tracking
* ADF (Atlassian Document Format) Parsing
* REST APIs for manual synchronization

---

# Tech Stack

* Python 3.12+
* Flask
* Flask-SQLAlchemy
* SQLite
* Jira Cloud REST API
* python-dotenv

---

# Project Structure

```text
jira-mcp-app/

├── app.py
├── requirements.txt
├── .env

├── database/
│   ├── db.py
│   └── jira_mcp.db

├── models/
│   ├── project.py
│   ├── issue.py
│   ├── comment.py
│   ├── history.py
│   └── sync_metadata.py

├── services/
│   ├── jira_client.py
│   ├── project_sync.py
│   ├── issue_sync.py
│   ├── comment_sync.py
│   └── history_sync.py

└── utils/
    └── adf_parser.py
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone <repository-url>

cd jira-mcp-app
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install flask
pip install flask-sqlalchemy
pip install python-dotenv
pip install requests
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
JIRA_BASE_URL=https://your-company.atlassian.net

JIRA_EMAIL=your-email@example.com

JIRA_API_TOKEN=your-api-token
```

Example:

```env
JIRA_BASE_URL=https://company.atlassian.net

JIRA_EMAIL=test@gmail.com

JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxx
```

---

# Running Application

Start Flask Server:

```bash
python app.py
```

Expected Output:

```text
* Running on http://127.0.0.1:5000
```

---

# Database

SQLite database file:

```text
database/jira_mcp.db
```

---

# API Endpoints

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

### Response

```json
{
  "status": "running",
  "service": "Jira Data Sync"
}
```

---

# Project Sync

Synchronizes Jira projects.

### Request

```http
GET /sync/projects
```

### Postman

Method:

```text
GET
```

URL:

```text
http://localhost:5000/sync/projects
```

### Response

```json
{
  "success": true,
  "inserted": 1,
  "updated": 0
}
```

---

# Issue Sync

Synchronizes Jira issues.

Supports:

* Full Sync
* Incremental Sync

### Request

```http
GET /sync/issues
```

### Postman

Method:

```text
GET
```

URL:

```text
http://localhost:5000/sync/issues
```

### Response

```json
{
  "success": true,
  "total_issues": 10,
  "inserted": 10,
  "updated": 0
}
```

---

# Comment Sync

Synchronizes Jira issue comments.

### Request

```http
GET /sync/comments
```

### Postman

Method:

```text
GET
```

URL:

```text
http://localhost:5000/sync/comments
```

### Response

```json
{
  "success": true,
  "total_comments": 5,
  "inserted": 5,
  "updated": 0
}
```

---

# History Sync

Synchronizes Jira issue changelog/history.

### Request

```http
GET /sync/history
```

### Postman

Method:

```text
GET
```

URL:

```text
http://localhost:5000/sync/history
```

### Response

```json
{
  "success": true,
  "total_histories": 20,
  "inserted": 20,
  "updated": 0
}
```

---

# Sync All

Runs all synchronization processes sequentially.

Flow:

```text
Projects
    ↓
Issues
    ↓
Comments
    ↓
History
```

### Request

```http
GET /sync/all
```

### Postman

Method:

```text
GET
```

URL:

```text
http://localhost:5000/sync/all
```

### Sample Response

```json
{
  "project_sync": {
    "success": true
  },
  "issue_sync": {
    "success": true
  },
  "comment_sync": {
    "success": true
  },
  "history_sync": {
    "success": true
  }
}
```

---

# Database Tables

## jira_projects

Stores Jira projects.

## jira_issues

Stores Jira issues.

## jira_comments

Stores Jira comments.

## jira_issue_history

Stores issue changelog/history.

## sync_metadata

Stores synchronization cursors.

Example:

```text
issue_sync
comment_sync
history_sync
```

Used for incremental synchronization.

---

# Current Limitations

* No pagination yet
* Attachments sync not implemented
* Worklogs sync not implemented
* Incremental Comment Sync under development
* Incremental History Sync under development

---

# Future Roadmap

## Phase 2

* Pagination
* Incremental Sync Stabilization
* Enhanced Sync Metadata

## Phase 3

* Attachments Sync
* Worklogs Sync
* Changelog Enhancements

## Phase 4

* LangChain Integration
* MCP Server
* Tool Calling
* Conversation Memory

## Phase 5

* Jira MCP AI Agent
* Natural Language Jira Operations
* AI Querying SQLite Knowledge Base
* Jira Analytics Dashboard

---

# Author

Darshan A R

Jira Data Sync Platform → Foundation for Jira MCP AI Agent.
