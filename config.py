import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    DATABASE_DIR = os.path.join(
        BASE_DIR,
        "database"
    )

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(DATABASE_DIR, 'jira_sync.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SYNC_LOOKBACK_DAYS = int(
        os.getenv(
            "SYNC_LOOKBACK_DAYS",
            25
        )
    )