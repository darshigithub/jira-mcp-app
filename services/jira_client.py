import os
import requests
from requests.auth import HTTPBasicAuth


class JiraClient:

    def __init__(self):

        self.base_url = os.getenv("JIRA_BASE_URL")

        self.auth = HTTPBasicAuth(
            os.getenv("JIRA_EMAIL"),
            os.getenv("JIRA_API_TOKEN")
        )

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    # -------------------------
    # Projects
    # -------------------------

    def get_projects(self):

        url = f"{self.base_url}/rest/api/3/project"

        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    def get_project(self, project_key):

        url = f"{self.base_url}/rest/api/3/project/{project_key}"

        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    # -------------------------
    # Full Issue Sync
    # -------------------------

    def get_issues(
        self,
        project_key="MCP",
        start_at=0,
        max_results=100
    ):

        url = f"{self.base_url}/rest/api/3/search/jql"

        params = {
            "jql": f"project = {project_key}",
            "startAt": start_at,
            "maxResults": max_results
        }

        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    # -------------------------
    # Incremental Issue Sync
    # -------------------------

    def get_updated_issues(
        self,
        project_key="MCP",
        updated_since=None,
        start_at=0,
        max_results=100
    ):

        if updated_since:

            print(f"Updated Since Raw: {updated_since}")

            jql = (
                f'project = {project_key} '
                f'AND updated >= "{updated_since}" '
                f'ORDER BY updated ASC'
            )

        else:

            jql = (
                f'project = {project_key} '
                f'AND updated >= -2d '
                f'ORDER BY updated ASC'
            )

        print("=" * 60)
        print("INCREMENTAL JQL")
        print(jql)
        print("=" * 60)

        url = f"{self.base_url}/rest/api/3/search/jql"

        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results
        }

        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers=self.headers
        )

        print("=" * 60)
        print("STATUS CODE")
        print(response.status_code)
        print("=" * 60)

        response.raise_for_status()

        data = response.json()

        print("=" * 60)
        print("RAW JIRA RESPONSE")
        print(data)
        print("=" * 60)

        print(
            f"Total Issues Returned: "
            f"{len(data.get('issues', []))}"
        )

        return data

    # -------------------------
    # Issue Details
    # -------------------------

    def get_issue_details(self, issue_id):

        url = f"{self.base_url}/rest/api/3/issue/{issue_id}"

        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    # -------------------------
    # Comments
    # -------------------------

    def get_issue_comments(self, issue_id):

        url = f"{self.base_url}/rest/api/3/issue/{issue_id}/comment"

        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    # -------------------------
    # Changelog / History
    # -------------------------

    def get_issue_history(self, issue_id):

        url = (
            f"{self.base_url}"
            f"/rest/api/3/issue/"
            f"{issue_id}"
            f"?expand=changelog"
        )

        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
    
    # Include if required extra feature 
    
    def get_recent_issues(
        self,
        project_key="MCP",
        days=os.getenv(
            "SYNC_LOOKBACK_DAYS",
        ),
        start_at=0,
        max_results=100
    ):

        jql = (
            f"project = {project_key} "
            f"AND updated >= -{days}d "
            f"ORDER BY updated DESC"
        )

        url = f"{self.base_url}/rest/api/3/search/jql"

        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results
        }

        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()