from datetime import datetime

from services.jira_client import JiraClient

from models.issue import JiraIssue
from models.history import JiraIssueHistory
from models.sync_metadata import SyncMetadata

from database.db import db


class HistorySync:

    def sync(self):

        jira = JiraClient()

        inserted = 0
        updated = 0
        total_histories = 0

        try:

            print("=" * 60)
            print("RUNNING HISTORY SYNC")
            print("=" * 60)

            sync_record = SyncMetadata.query.filter_by(
                sync_name="history_sync"
            ).first()

            last_sync_time = None

            if (
                sync_record and
                sync_record.last_sync_time
            ):

                last_sync_time = (
                    sync_record.last_sync_time
                )

                print(
                    f"Running Incremental History Sync since "
                    f"{last_sync_time}"
                )

                issues = JiraIssue.query.filter(
                    JiraIssue.updated_at >= last_sync_time
                ).all()

            else:

                print(
                    "No History Cursor Found"
                )

                print(
                    "Running Full History Sync"
                )

                issues = JiraIssue.query.all()

            print(
                f"Processing {len(issues)} issues"
            )

            latest_history_time = last_sync_time

            for issue in issues:

                print("=" * 60)

                print(
                    f"Fetching History For: "
                    f"{issue.issue_key}"
                )

                print("=" * 60)

                response = jira.get_issue_history(
                    issue.issue_id
                )

                changelog = response.get(
                    "changelog",
                    {}
                )

                histories = changelog.get(
                    "histories",
                    []
                )

                print(
                    f"Histories Found: "
                    f"{len(histories)}"
                )

                for history in histories:

                    history_id = history.get(
                        "id"
                    )

                    author = ""

                    if history.get("author"):

                        author = history[
                            "author"
                        ].get(
                            "displayName",
                            ""
                        )

                    changed_at = None

                    if history.get("created"):

                        changed_at = datetime.strptime(
                            history["created"],
                            "%Y-%m-%dT%H:%M:%S.%f%z"
                        ).replace(
                            tzinfo=None
                        )

                    if (
                        changed_at and
                        (
                            latest_history_time is None
                            or changed_at >
                            latest_history_time
                        )
                    ):
                        latest_history_time = (
                            changed_at
                        )

                    items = history.get(
                        "items",
                        []
                    )

                    for item in items:

                        total_histories += 1

                        field_name = item.get(
                            "field"
                        )

                        old_value = item.get(
                            "fromString"
                        )

                        new_value = item.get(
                            "toString"
                        )

                        unique_history_id = (
                            f"{history_id}_"
                            f"{field_name}"
                        )

                        existing = (
                            JiraIssueHistory.query
                            .filter_by(
                                history_id=
                                unique_history_id
                            )
                            .first()
                        )

                        if existing:

                            existing.author = author

                            existing.field_name = (
                                field_name
                            )

                            existing.old_value = (
                                old_value
                            )

                            existing.new_value = (
                                new_value
                            )

                            existing.changed_at = (
                                changed_at
                            )

                            updated += 1

                            print(
                                f"Updated History: "
                                f"{unique_history_id}"
                            )

                        else:

                            history_record = (
                                JiraIssueHistory(

                                    history_id=
                                    unique_history_id,

                                    issue_id=
                                    issue.id,

                                    author=
                                    author,

                                    field_name=
                                    field_name,

                                    old_value=
                                    old_value,

                                    new_value=
                                    new_value,

                                    changed_at=
                                    changed_at
                                )
                            )

                            db.session.add(
                                history_record
                            )

                            inserted += 1

                            print(
                                f"Inserted History: "
                                f"{unique_history_id}"
                            )

            db.session.commit()

            if latest_history_time:

                sync_record = (
                    SyncMetadata.query.filter_by(
                        sync_name=
                        "history_sync"
                    ).first()
                )

                if not sync_record:

                    sync_record = SyncMetadata(
                        sync_name=
                        "history_sync",

                        last_sync_time=
                        latest_history_time
                    )

                    db.session.add(
                        sync_record
                    )

                else:

                    sync_record.last_sync_time = (
                        latest_history_time
                    )

                db.session.commit()

                print(
                    f"Updated History Cursor: "
                    f"{latest_history_time}"
                )

            print("=" * 60)
            print("HISTORY SYNC COMPLETE")
            print("=" * 60)

            return {
                "success": True,
                "total_histories": total_histories,
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