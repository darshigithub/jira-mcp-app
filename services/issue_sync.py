from services.jira_client import JiraClient
from models.issue import JiraIssue
from models.project import JiraProject
from database.db import db
from utils.adf_parser import extract_text_from_adf 

import json
import traceback


class IssueSync:

    def sync(self):

        inserted = 0
        updated_count = 0

        try:

            jira = JiraClient()

            data = jira.get_issues("MCP")

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