from database.db import db

class JiraProject(db.Model):

    __tablename__ = "jira_projects"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.String(100))

    project_key = db.Column(db.String(50))

    project_name = db.Column(db.String(255))

    issues = db.relationship(
        "JiraIssue",
        backref="project",
        lazy=True
    )