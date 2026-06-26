from flask import Blueprint, jsonify

from models.issue import JiraIssue
from services.issue_sync import IssueSync

issue_bp = Blueprint(
    "issue",
    __name__
)


@issue_bp.route(
    "/issues",
    methods=["GET"]
)
def get_issues():

    try:

        issues = JiraIssue.query.all()

        result = []

        for issue in issues:

            result.append({

                "id": issue.issue_id,

                "key": issue.issue_key,

                "summary": issue.summary,

                "description": issue.description,

                "status": issue.status,

                "issue_type": issue.issue_type,

                "assignee": issue.assignee,

                "reporter": issue.reporter,

                "priority": issue.priority,

                "due_date": issue.due_date,

                "start_date": issue.start_date,

                "team": issue.team,

                "labels": issue.labels,

                "parent_issue_key":
                    issue.parent_issue_key,

                "project_id":
                    issue.project_id,

                "created_at":
                    issue.created_at,

                "updated_at":
                    issue.updated_at,

                # NEW
                "custom_fields":
                    issue.custom_fields,

                # NEW
                "raw_issue":
                    issue.raw_issue

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


@issue_bp.route(
    "/issues/<issue_key>",
    methods=["GET"]
)
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

                "description": issue.description,

                "status": issue.status,

                "issue_type": issue.issue_type,

                "assignee": issue.assignee,

                "reporter": issue.reporter,

                "priority": issue.priority,

                "due_date": issue.due_date,

                "start_date": issue.start_date,

                "team": issue.team,

                "labels": issue.labels,

                "parent_issue_key":
                    issue.parent_issue_key,

                "project_id":
                    issue.project_id,

                "created_at":
                    issue.created_at,

                "updated_at":
                    issue.updated_at,

                # NEW
                "custom_fields":
                    issue.custom_fields,

                # NEW
                "raw_issue":
                    issue.raw_issue

            }

        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@issue_bp.route(
    "/sync/issues",
    methods=["GET"]
)
def sync_issues():

    try:

        result = IssueSync().sync()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500