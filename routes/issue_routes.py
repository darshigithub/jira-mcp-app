from flask import Blueprint, jsonify

from models.issue import JiraIssue
from services.issue_sync import IssueSync

issue_bp = Blueprint("issue", __name__)


@issue_bp.route("/issues", methods=["GET"])
def get_issues():

    try:

        issues = JiraIssue.query.all()

        result = []

        for issue in issues:

            result.append({
                "id": issue.issue_id,
                "key": issue.issue_key,
                "summary": issue.summary,
                "status": issue.status,
                "assignee": issue.assignee,
                "priority": issue.priority,
                "project_id": issue.project_id,
                "created_at": issue.created_at,
                "updated_at": issue.updated_at
            })

        return jsonify({
            "success": True,
            "count": len(result),
            "data": result
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@issue_bp.route("/issues/<issue_key>", methods=["GET"])
def get_issue(issue_key):

    try:

        issue = JiraIssue.query.filter_by(
            issue_key=issue_key
        ).first()

        if not issue:

            return jsonify({
                "success": False,
                "message": "Issue not found"
            }), 404

        return jsonify({
            "success": True,
            "data": {
                "id": issue.issue_id,
                "key": issue.issue_key,
                "summary": issue.summary,
                "status": issue.status,
                "assignee": issue.assignee,
                "priority": issue.priority,
                "project_id": issue.project_id,
                "created_at": issue.created_at,
                "updated_at": issue.updated_at
            }
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@issue_bp.route("/sync/issues", methods=["GET"])
def sync_issues():

    try:

        result = IssueSync().sync()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500