from flask import Blueprint
from models.issue import JiraIssue

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    total = JiraIssue.query.count()

    open_count = JiraIssue.query.filter(
        JiraIssue.status != "Done"
    ).count()

    return {
        "total_issues": total,
        "open_issues": open_count
    }