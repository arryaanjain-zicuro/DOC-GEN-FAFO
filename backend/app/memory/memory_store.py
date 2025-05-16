# app/memory_store.py

from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from backend.app.services.db import engine, SessionLocal
from workflows.models.memory.memory_snapshot import MemorySnapshot
import json

Base = declarative_base()


class MemorySnapshotDB(Base):
    __tablename__ = "memory_snapshots"

    session_id = Column(String, primary_key=True, index=True)
    snapshot = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


Base.metadata.create_all(bind=engine)


def save_snapshot(snapshot: MemorySnapshot):
    db = SessionLocal()
    try:
        db_record = MemorySnapshotDB(
            session_id=snapshot.session_id,
            snapshot=json.loads(snapshot.model_dump_json())
        )
        db.merge(db_record)  # upsert
        db.commit()
    finally:
        db.close()


def get_snapshot(session_id: str) -> MemorySnapshot:
    db = SessionLocal()
    try:
        record = db.query(MemorySnapshotDB).filter_by(session_id=session_id).first()
        if not record:
            raise ValueError("Snapshot not found")
        return MemorySnapshot(**record.snapshot)
    finally:
        db.close()
