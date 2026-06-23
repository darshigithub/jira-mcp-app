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

   
    # Projects

    def get_projects(self):

        url = f"{self.base_url}/rest/api/3/project"

        # Get Projects endpoint
        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
    
    # Project

    def get_project(self, project_key):

        url = f"{self.base_url}/rest/api/3/project/{project_key}"

        # Get Projects endpoint
        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    # Issues

    def get_issues(
        self,
        project_key="MCP",
        start_at=0,
        max_results=100  # manual we can give
    ):

        url = f"{self.base_url}/rest/api/3/search/jql"

        params = {
            "jql": f"project = {project_key}",
            "startAt": start_at,
            "maxResults": max_results
        }

        # get method 
        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()

    def get_issue_details(self, issue_id):

        url = f"{self.base_url}/rest/api/3/issue/{issue_id}"

        # Get issue details endpoint
        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()


    # Incremental Sync    

    def get_updated_issues(
        self,
        project_key="MCP",
        updated_since=None,
        start_at=0,
        max_results=100
    ):

        if updated_since:
            jql = (
                f'project = {project_key} '
                f'AND updated >= "{updated_since}"'
            )
        else:
            jql = f'project = {project_key}'

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
    
    def get_issue_comments(self, issue_id):

        url = f"{self.base_url}/rest/api/3/issue/{issue_id}/comment"

        # Get Isuue comment endpoint
        response = requests.get(
            url,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
    
    def get_issue_history(
        self,
        issue_id
    ):

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