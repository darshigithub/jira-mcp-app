# models/sync_metadata.py

from database.db import db

class SyncMetadata(db.Model):

    __tablename__ = "sync_metadata"

    id = db.Column(db.Integer, primary_key=True)

    sync_name = db.Column(
        db.String(50),
        unique=True
    )

    last_sync_time = db.Column(db.DateTime)