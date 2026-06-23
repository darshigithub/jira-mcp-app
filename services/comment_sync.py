from services.jira_client import JiraClient
from models.issue import JiraIssue
from models.comment import JiraComment
from database.db import db


class CommentSync:

    def sync(self):

        jira = JiraClient()

        issues = JiraIssue.query.all()

        inserted = 0
        updated = 0

        try:

            for issue in issues:

                comments_response = jira.get_issue_comments(
                    issue.issue_id
                )

                comments = comments_response.get(
                    "comments",
                    []
                )

                for comment in comments:

                    comment_id = comment["id"]

                    existing = JiraComment.query.filter_by(
                        comment_id=comment_id
                    ).first()

                    author = ""

                    if comment.get("author"):
                        author = comment["author"].get(
                            "displayName",
                            ""
                        )

                    body = str(
                        comment.get("body", "")
                    )

                    parent_id = comment.get(
                        "parentId"
                    )

                    jsd_public = comment.get(
                        "jsdPublic",
                        True
                    )

                    created_at = comment.get(
                        "created"
                    )

                    updated_at = comment.get(
                        "updated"
                    )

                    if existing:

                        existing.author = author
                        existing.body = body

                        existing.jira_parent_comment_id = (
                            str(parent_id)
                            if parent_id
                            else None
                        )

                        existing.jsd_public = jsd_public
                        existing.updated_at = updated_at

                        updated += 1

                    else:

                        new_comment = JiraComment(

                            comment_id=comment_id,

                            issue_id=issue.id,

                            jira_parent_comment_id=(
                                str(parent_id)
                                if parent_id
                                else None
                            ),

                            author=author,

                            body=body,

                            jsd_public=jsd_public,

                            created_at=created_at,

                            updated_at=updated_at
                        )

                        db.session.add(
                            new_comment
                        )

                        inserted += 1

            db.session.commit()

            return {
                "success": True,
                "inserted": inserted,
                "updated": updated
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "error": str(e)
            }