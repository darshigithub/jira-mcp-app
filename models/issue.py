from database.db import db


class JiraIssue(db.Model):

    __tablename__ = "jira_issues"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Jira Issue ID
    issue_id = db.Column(
        db.String(100),
        unique=True
    )

    # MCP-1, MCP-2...
    issue_key = db.Column(
        db.String(100),
        unique=True
    )

    summary = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(100)
    )

    assignee = db.Column(
        db.String(255)
    )

    reporter = db.Column(
        db.String(255)
    )

    priority = db.Column(
        db.String(100)
    )

    due_date = db.Column(
        db.String(100)
    )

    start_date = db.Column(
        db.String(100)
    )

    parent_issue_key = db.Column(
        db.String(100)
    )

    labels = db.Column(
        db.Text
    )

    team = db.Column(
        db.String(255)
    )

    issue_type = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.String(100)
    )

    updated_at = db.Column(
        db.String(100)
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "jira_projects.id"
        )
    )

    # -----------------------------
    # NEW COLUMNS
    # -----------------------------

    # Stores all Jira custom fields
    custom_fields = db.Column(
        db.JSON
    )

    # Stores complete Jira issue response
    raw_issue = db.Column(
        db.JSON
    )