from database.db import db


class JiraIssue(db.Model):

    __tablename__ = "jira_issues"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    issue_id = db.Column(
        db.String(100)
    )

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

    priority = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.String(100)
    )

    updated_at = db.Column(
        db.String(100)
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("jira_projects.id")
    )