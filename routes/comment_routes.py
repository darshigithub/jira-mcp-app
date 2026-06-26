from flask import Blueprint, jsonify

from services.comment_sync import CommentSync
from models.comment import JiraComment

comment_bp = Blueprint(
    "comment_bp",
    __name__
)


@comment_bp.route(
    "/sync/comments",
    methods=["GET"]
)
def sync_comments():

    try:

        result = CommentSync().sync()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@comment_bp.route(
    "/comments",
    methods=["GET"]
)
def get_comments():

    try:

        comments = JiraComment.query.all()

        result = []

        for c in comments:

            result.append({

                "id": c.id,

                "comment_id": c.comment_id,

                "issue_id": c.issue_id,

                "jira_parent_comment_id":
                    c.jira_parent_comment_id,

                "parent_comment_id":
                    c.parent_comment_id,

                "author":
                    c.author,

                "body":
                    c.body,

                "jsd_public":
                    c.jsd_public,

                "created_at":
                    c.created_at,

                "updated_at":
                    c.updated_at,

                "custom_fields":
                    c.custom_fields

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


@comment_bp.route(
    "/comments/<comment_id>",
    methods=["GET"]
)
def get_comment(comment_id):

    try:

        comment = JiraComment.query.filter_by(
            comment_id=comment_id
        ).first()

        if not comment:

            return jsonify({

                "success": False,

                "message": "Comment not found"

            }), 404

        return jsonify({

            "success": True,

            "data": {

                "id": comment.id,

                "comment_id": comment.comment_id,

                "issue_id": comment.issue_id,

                "jira_parent_comment_id":
                    comment.jira_parent_comment_id,

                "parent_comment_id":
                    comment.parent_comment_id,

                "author":
                    comment.author,

                "body":
                    comment.body,

                "jsd_public":
                    comment.jsd_public,

                "created_at":
                    comment.created_at,

                "updated_at":
                    comment.updated_at,

                "custom_fields":
                    comment.custom_fields

            }

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500