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

    try:

        result = HistorySync().sync()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@history_bp.route(
    "/history",
    methods=["GET"]
)
def get_history():

    try:

        history_records = JiraIssueHistory.query.all()

        result = []

        for h in history_records:

            result.append({

                "id": h.id,

                "history_id": h.history_id,

                "issue_id": h.issue_id,

                "author": h.author,

                "field_name": h.field_name,

                "field_type": h.field_type,

                "old_value": h.old_value,

                "new_value": h.new_value,

                "changed_at": h.changed_at

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


@history_bp.route(
    "/history/<history_id>",
    methods=["GET"]
)
def get_history_record(history_id):

    try:

        history = JiraIssueHistory.query.filter_by(
            history_id=history_id
        ).first()

        if not history:

            return jsonify({

                "success": False,

                "message": "History record not found"

            }), 404

        return jsonify({

            "success": True,

            "data": {

                "id": history.id,

                "history_id": history.history_id,

                "issue_id": history.issue_id,

                "author": history.author,

                "field_name": history.field_name,

                "field_type": history.field_type,

                "old_value": history.old_value,

                "new_value": history.new_value,

                "changed_at": history.changed_at

            }

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


@history_bp.route(
    "/issues/<issue_key>/history",
    methods=["GET"]
)
def get_issue_history(issue_key):

    try:

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

        result = []

        for h in history_records:

            result.append({

                "history_id": h.history_id,

                "author": h.author,

                "field_name": h.field_name,

                "field_type": h.field_type,

                "old_value": h.old_value,

                "new_value": h.new_value,

                "changed_at": h.changed_at

            })

        return jsonify({

            "success": True,

            "issue_key": issue.issue_key,

            "count": len(result),

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500