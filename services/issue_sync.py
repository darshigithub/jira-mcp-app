from services.jira_client import JiraClient
from models.issue import JiraIssue
from models.project import JiraProject
from database.db import db
from utils.adf_parser import extract_text_from_adf 

from models.sync_metadata import SyncMetadata
from datetime import datetime

import traceback
import os

class IssueSync:

    def sync(self):

        inserted = 0
        updated_count = 0

        try:

            jira = JiraClient()

            sync_record = SyncMetadata.query.filter_by(
                sync_name="issue_sync"
            ).first()

            # First Sync
            if not sync_record:

                print("Running Full Issue Sync...")

                lookback_days = int(
                    os.getenv(
                        "SYNC_LOOKBACK_DAYS",
                        25
                    )
                )

                print(
                    f"Fetching last {lookback_days} days issues..."
                )

                data = jira.get_recent_issues(
                    project_key="MCP",
                    days=lookback_days
                )

            # Incremental Sync
            else:

                print(
                    f"Running Incremental Sync "
                    f"since {sync_record.last_sync_time}"
                )

                updated_since = (
                    sync_record.last_sync_time
                    .strftime("%Y-%m-%d %H:%M")
                )

                print(f"Updated Since: {updated_since}")

                data = jira.get_updated_issues(
                    project_key="MCP",
                    updated_since=updated_since
                )

            issues = data.get(
                "issues",
                []
            )

            print(
                f"Found {len(issues)} issues"
            )

            for issue in issues:

                issue_id = issue["id"]

                details = jira.get_issue_details(
                    issue_id
                )

                key = details.get("key")

                fields = details.get(
                    "fields",
                    {}
                )

                summary = fields.get(
                    "summary"
                )

                # Status
                status = (
                    fields.get(
                        "status",
                        {}
                    ).get("name")
                )

                # Assignee
                assignee = None

                if fields.get("assignee"):

                    assignee = (
                        fields["assignee"]
                        .get("displayName")
                    )

                # Reporter
                reporter = None

                if fields.get("reporter"):

                    reporter = (
                        fields["reporter"]
                        .get("displayName")
                    )

                # Priority
                priority = None

                if fields.get("priority"):

                    priority = (
                        fields["priority"]
                        .get("name")
                    )

                # Issue Type
                issue_type = None

                if fields.get("issuetype"):

                    issue_type = (
                        fields["issuetype"]
                        .get("name")
                    )

                # Description
                description = extract_text_from_adf(
                    fields.get(
                        "description",
                        {}
                    )
                )

                # Due Date
                due_date = fields.get(
                    "duedate"
                )

                # Parent Issue
                parent_issue_key = None

                if fields.get("parent"):

                    parent_issue_key = (
                        fields["parent"]
                        .get("key")
                    )

                # Labels
                labels = ",".join(
                    fields.get(
                        "labels",
                        []
                    )
                )

                # --------------------------------------------------
                # CUSTOM FIELDS
                # Replace IDs after checking Jira field API
                # --------------------------------------------------

                # We need to edit this fields after after getting api response 

                team = fields.get(
                    "customfield_10001"
                )

                start_date = fields.get(
                    "customfield_10002"
                )

                # --------------------------------------------------

                created = fields.get(
                    "created"
                )

                updated = fields.get(
                    "updated"
                )

                project_data = fields.get(
                    "project",
                    {}
                )

                jira_project_id = str(
                    project_data.get("id")
                )

                project = JiraProject.query.filter_by(
                    project_id=jira_project_id
                ).first()

                if not project:

                    print(
                        f"Project not found for Jira Project ID: "
                        f"{jira_project_id}"
                    )

                existing = JiraIssue.query.filter_by(
                    issue_id=issue_id
                ).first()

                if existing:

                    existing.issue_key = key
                    existing.summary = summary
                    existing.description = description

                    existing.status = status
                    existing.issue_type = issue_type

                    existing.assignee = assignee
                    existing.reporter = reporter

                    existing.priority = priority

                    existing.due_date = due_date
                    existing.start_date = start_date

                    existing.labels = labels
                    existing.team = team

                    existing.parent_issue_key = (
                        parent_issue_key
                    )

                    existing.created_at = created
                    existing.updated_at = updated

                    existing.project_id = (
                        project.id
                        if project
                        else None
                    )

                    updated_count += 1

                    print(
                        f"Updated: {key}"
                    )

                else:

                    new_issue = JiraIssue(

                        issue_id=issue_id,

                        issue_key=key,

                        summary=summary,

                        description=description,

                        status=status,

                        issue_type=issue_type,

                        assignee=assignee,

                        reporter=reporter,

                        priority=priority,

                        due_date=due_date,

                        start_date=start_date,

                        labels=labels,

                        team=team,

                        parent_issue_key=(
                            parent_issue_key
                        ),

                        created_at=created,

                        updated_at=updated,

                        project_id=(
                            project.id
                            if project
                            else None
                        )
                    )

                    db.session.add(
                        new_issue
                    )

                    inserted += 1

                    print(
                        f"Inserted: {key}"
                    )

            # Update sync cursor using latest Jira issue timestamp
            sync_record = SyncMetadata.query.filter_by(
                sync_name="issue_sync"
            ).first()

            latest_updated = None

            for issue in issues:

                details = jira.get_issue_details(
                    issue["id"]
                )

                updated_str = (
                    details.get("fields", {})
                    .get("updated")
                )

                if updated_str:

                    jira_updated = datetime.strptime(
                        updated_str,
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    )

                    if (
                        latest_updated is None
                        or jira_updated > latest_updated
                    ):
                        latest_updated = jira_updated

            if latest_updated:

                if not sync_record:

                    sync_record = SyncMetadata(
                        sync_name="issue_sync",
                        last_sync_time=latest_updated
                    )

                    db.session.add(sync_record)

                else:

                    sync_record.last_sync_time = latest_updated

                print(
                    f"Updated Sync Cursor: "
                    f"{latest_updated}"
                )

            else:

                print(
                    "No issues found. "
                    "Keeping existing sync cursor."
                )

            db.session.commit()

            result = {
                "success": True,
                "total_issues": len(issues),
                "inserted": inserted,
                "updated": updated_count
            }

            print(result)

            return result

        except Exception as e:

            print(
                "Issue Sync Failed"
            )

            traceback.print_exc()

            try:

                db.session.rollback()

            except Exception as rollback_error:

                print(
                    f"Rollback Error: "
                    f"{rollback_error}"
                )

            return {
                "success": False,
                "error": str(e)
            }