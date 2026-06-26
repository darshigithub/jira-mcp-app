from database.db import db


class JiraComment(db.Model):

    __tablename__ = "jira_comments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    comment_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    issue_id = db.Column(
        db.Integer,
        db.ForeignKey("jira_issues.id"),
        nullable=False
    )

    jira_parent_comment_id = db.Column(
        db.String(50),
        nullable=True
    )

    parent_comment_id = db.Column(
        db.Integer,
        db.ForeignKey("jira_comments.id"),
        nullable=True
    )

    author = db.Column(
        db.String(255)
    )

    body = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.String(100)
    )

    updated_at = db.Column(
        db.String(100)
    )

    jsd_public = db.Column(
        db.Boolean
    )

    # Store any future/custom Jira comment properties
    custom_fields = db.Column(
        db.JSON,
        nullable=True
    )