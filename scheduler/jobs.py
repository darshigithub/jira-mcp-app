from apscheduler.schedulers.background import BackgroundScheduler

from services.project_sync import ProjectSync
from services.issue_sync import IssueSync


def init_scheduler(app):

    scheduler = BackgroundScheduler()

    def sync_projects():

        with app.app_context():

            print("Running Project Sync...")

            ProjectSync().sync()

    def sync_issues():

        with app.app_context():

            print("Running Issue Sync...")

            IssueSync().sync()

    scheduler.add_job(
        sync_projects,
        trigger="interval",
        hours=24, # we can mannuly set this time interval for this job
        id="project_sync"
    )

    scheduler.add_job(
        sync_issues,
        trigger="interval",
        minutes=10,  # we can mannuly set this time interval for this job
        id="issue_sync"
    )

    scheduler.start()

    return scheduler