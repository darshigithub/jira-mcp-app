from services.jira_client import JiraClient
from models.project import JiraProject
from database.db import db

import traceback


class ProjectSync:

    def sync(self):

        inserted = 0
        updated_count = 0

        try:

            jira = JiraClient()

            projects = jira.get_projects()

            print(
                f"Found {len(projects)} projects"
            )

            for project in projects:

                project_id = str(
                    project.get("id")
                )

                existing = JiraProject.query.filter_by(
                    project_id=project_id
                ).first()

                if existing:

                    existing.project_key = project.get(
                        "key"
                    )

                    existing.project_name = project.get(
                        "name"
                    )

                    if hasattr(
                        existing,
                        "project_type"
                    ):
                        existing.project_type = project.get(
                            "projectTypeKey"
                        )

                    updated_count += 1

                    print(
                        f"Updated: {existing.project_key}"
                    )

                else:

                    new_project = JiraProject(
                        project_id=project_id,
                        project_key=project.get(
                            "key"
                        ),
                        project_name=project.get(
                            "name"
                        )
                    )

                    if hasattr(
                        new_project,
                        "project_type"
                    ):
                        new_project.project_type = project.get(
                            "projectTypeKey"
                        )

                    db.session.add(
                        new_project
                    )

                    inserted += 1

                    print(
                        f"Inserted: {project.get('key')}"
                    )

            db.session.commit()

            result = {
                "success": True,
                "total_projects": len(projects),
                "inserted": inserted,
                "updated": updated_count
            }

            print(result)

            return result

        except Exception as e:

            print("Project Sync Failed")

            traceback.print_exc()

            try:
                db.session.rollback()
            except Exception as rollback_error:
                print(
                    f"Rollback Error: {rollback_error}"
                )

            return {
                "success": False,
                "error": str(e)
            }