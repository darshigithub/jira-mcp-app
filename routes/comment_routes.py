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

    result = CommentSync().sync()

    return jsonify(result)


@comment_bp.route(
    "/comments",
    methods=["GET"]
)
def get_comments():

    comments = JiraComment.query.all()

    return jsonify([
        {
            "id": c.id,
            "comment_id": c.comment_id,
            "issue_id": c.issue_id,

            "jira_parent_comment_id":
                c.jira_parent_comment_id,

            "author": c.author,

            "body": c.body,

            "jsd_public": c.jsd_public,

            "created_at":
                c.created_at,

            "updated_at":
                c.updated_at
        }
        for c in comments
    ])