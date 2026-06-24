# services/sync_metadata_service.py

from models.sync_metadata import SyncMetadata
from database.db import db

from datetime import datetime


class SyncMetadataService:

    @staticmethod
    def get_last_sync(sync_name):

        return SyncMetadata.query.filter_by(
            sync_name=sync_name
        ).first()

    @staticmethod
    def update_sync(sync_name):

        record = SyncMetadata.query.filter_by(
            sync_name=sync_name
        ).first()

        if not record:

            record = SyncMetadata(
                sync_name=sync_name
            )

            db.session.add(record)

        record.last_sync_time = datetime.utcnow()

        db.session.commit()