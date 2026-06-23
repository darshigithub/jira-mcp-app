from flask import Blueprint, jsonify

from services.history_sync import HistorySync
from models.history import JiraIssueHistory
from models.issue import JiraIssue

history_bp = Blueprint(
    "history_bp",
    __name__
)


@history_bp.route(
    "/sync/history",
    methods=["GET"]
)
def sync_history():

    result = HistorySync().sync()

    return jsonify(result)


@history_bp.route(
    "/history",
    methods=["GET"]
)
def get_history():

    history_records = JiraIssueHistory.query.all()

    return jsonify([
        {
            "history_id": h.history_id,
            "issue_id": h.issue_id,
            "author": h.author,
            "field_name": h.field_name,
            "old_value": h.old_value,
            "new_value": h.new_value,
            "changed_at": h.changed_at
        }
        for h in history_records
    ])


@history_bp.route(
    "/issues/<issue_key>/history",
    methods=["GET"]
)
def get_issue_history(issue_key):

    issue = JiraIssue.query.filter_by(
        issue_key=issue_key
    ).first()

    if not issue:

        return jsonify({
            "success": False,
            "message": "Issue not found"
        }), 404

    history_records = JiraIssueHistory.query.filter_by(
        issue_id=issue.id
    ).all()

    return jsonify([
        {
            "history_id": h.history_id,
            "author": h.author,
            "field_name": h.field_name,
            "old_value": h.old_value,
            "new_value": h.new_value,
            "changed_at": h.changed_at
        }
        for h in history_records
    ])