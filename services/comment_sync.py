from datetime import datetime

from services.jira_client import JiraClient

from models.issue import JiraIssue
from models.comment import JiraComment
from models.sync_metadata import SyncMetadata

from database.db import db

from utils.adf_parser import extract_text_from_adf


class CommentSync:

    def sync(self):

        jira = JiraClient()

        inserted = 0
        updated = 0
        total_comments = 0

        try:

            print("=" * 60)
            print("RUNNING COMMENT SYNC")
            print("=" * 60)

            sync_record = SyncMetadata.query.filter_by(
                sync_name="comment_sync"
            ).first()

            if (
                sync_record and
                sync_record.last_sync_time
            ):

                last_sync_time = sync_record.last_sync_time

                print(
                    f"Running Incremental Comment Sync since "
                    f"{last_sync_time}"
                )

                issues = JiraIssue.query.filter(
                    JiraIssue.updated_at >= last_sync_time
                ).all()

            else:

                last_sync_time = None

                print(
                    "No Comment Sync Cursor Found"
                )

                print(
                    "Running Full Comment Sync"
                )

                issues = JiraIssue.query.all()

            print(
                f"Processing {len(issues)} issues"
            )

            latest_comment_time = last_sync_time

            for issue in issues:

                print("=" * 60)

                print(
                    f"Fetching comments for "
                    f"{issue.issue_key}"
                )

                print("=" * 60)

                comments_response = jira.get_issue_comments(
                    issue.issue_id
                )

                comments = comments_response.get(
                    "comments",
                    []
                )

                print(
                    f"Found {len(comments)} comments"
                )

                for comment in comments:

                    total_comments += 1

                    comment_id = comment["id"]

                    existing = JiraComment.query.filter_by(
                        comment_id=comment_id
                    ).first()

                    author = ""

                    if comment.get("author"):

                        author = comment[
                            "author"
                        ].get(
                            "displayName",
                            ""
                        )
                    
                    # ------------------------------------
                    # Collect additional/custom fields
                    # ------------------------------------

                    STANDARD_FIELDS = {
                        "id",
                        "author",
                        "body",
                        "created",
                        "updated",
                        "jsdPublic",
                        "parentId",
                        "self"
                    }

                    custom_fields = {}

                    for field_name, value in comment.items():

                        if field_name not in STANDARD_FIELDS:

                            custom_fields[field_name] = value

                    body = extract_text_from_adf(
                        comment.get(
                            "body",
                            {}
                        )
                    )

                    parent_id = comment.get(
                        "parentId"
                    )

                    jsd_public = comment.get(
                        "jsdPublic",
                        True
                    )

                    created_at = datetime.strptime(
                        comment["created"],
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).replace(tzinfo=None)

                    updated_at = datetime.strptime(
                        comment["updated"],
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).replace(tzinfo=None)

                    if (
                        latest_comment_time is None
                        or updated_at > latest_comment_time
                    ):
                        latest_comment_time = updated_at

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

                        existing.custom_fields = custom_fields

                        updated += 1

                        print(
                            f"Updated Comment: "
                            f"{comment_id}"
                        )

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

                            updated_at=updated_at,

                            custom_fields=custom_fields
                        )

                        db.session.add(
                            new_comment
                        )

                        inserted += 1

                        print(
                            f"Inserted Comment: "
                            f"{comment_id}"
                        )

            db.session.commit()

            if latest_comment_time:

                sync_record = SyncMetadata.query.filter_by(
                    sync_name="comment_sync"
                ).first()

                if not sync_record:

                    sync_record = SyncMetadata(
                        sync_name="comment_sync",
                        last_sync_time=latest_comment_time
                    )

                    db.session.add(
                        sync_record
                    )

                else:

                    sync_record.last_sync_time = (
                        latest_comment_time
                    )

                db.session.commit()

                print(
                    f"Updated Comment Cursor: "
                    f"{latest_comment_time}"
                )

            print("=" * 60)
            print("COMMENT SYNC COMPLETE")
            print("=" * 60)

            return {
                "success": True,
                "total_comments": total_comments,
                "inserted": inserted,
                "updated": updated
            }

        except Exception as e:

            db.session.rollback()

            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "error": str(e)
            }