from database.db import db

class SyncMetadata(db.Model):

    __tablename__ = "sync_metadata"

    id = db.Column(db.Integer, primary_key=True)

    sync_name = db.Column(db.String(100))

    last_sync = db.Column(db.DateTime)