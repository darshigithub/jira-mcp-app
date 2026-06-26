from database.db import db


class JiraIssueHistory(db.Model):

    __tablename__ = "jira_issue_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    history_id = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    issue_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "jira_issues.id"
        ),
        nullable=False
    )

    author = db.Column(
        db.String(255)
    )

    # Example:
    # status
    # assignee
    # priority
    # customfield_10421
    field_name = db.Column(
        db.String(255)
    )

    # NEW
    # jira
    # custom
    field_type = db.Column(
        db.String(100)
    )

    old_value = db.Column(
        db.Text
    )

    new_value = db.Column(
        db.Text
    )

    changed_at = db.Column(
        db.String(100)
    )