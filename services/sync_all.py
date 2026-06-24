# Imports for for all services for sync all 

from services.project_sync import ProjectSync
from services.issue_sync import IssueSync
from services.comment_sync import CommentSync
from services.history_sync import HistorySync

class SyncAll:

    def sync(self):

        project_result = ProjectSync().sync()
        issue_result = IssueSync().sync()
        comment_result = CommentSync().sync()
        history_result = HistorySync().sync()

        return {
            "projects": project_result,
            "issues": issue_result,
            "comments": comment_result,
            "history": history_result
        }