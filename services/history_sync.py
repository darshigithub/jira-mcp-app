from services.jira_client import JiraClient

from models.issue import JiraIssue
from models.history import JiraIssueHistory

from database.db import db


class HistorySync:

    def sync(self):

        jira = JiraClient()

        issues = JiraIssue.query.all()

        inserted = 0
        updated = 0

        try:

            for issue in issues:

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

                    changed_at = history.get(
                        "created"
                    )

                    items = history.get(
                        "items",
                        []
                    )

                    for item in items:

                        unique_history_id = (
                            f"{history_id}_"
                            f"{item.get('field')}"
                        )

                        existing = (
                            JiraIssueHistory.query
                            .filter_by(
                                history_id=
                                unique_history_id
                            )
                            .first()
                        )

                        field_name = item.get(
                            "field"
                        )

                        old_value = item.get(
                            "fromString"
                        )

                        new_value = item.get(
                            "toString"
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