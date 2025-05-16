from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.services.db import engine, SessionLocal
from workflows.models.memory.memory_snapshot import MemorySnapshot

Base = declarative_base()


class MemorySnapshotDB(Base):
    __tablename__ = "memory_snapshots"

    session_id = Column(String, primary_key=True, index=True)
    snapshot = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


Base.metadata.create_all(bind=engine)


def save_snapshot(snapshot: MemorySnapshot):
    db = SessionLocal()
    try:
        print(f"Saving snapshot: {snapshot.session_id}")  # DEBUG
        db_record = MemorySnapshotDB(
            session_id=snapshot.session_id,
            snapshot=snapshot.model_dump()  # ✅ Use native dict for JSONB
        )
        db.merge(db_record)  # Upsert
        db.commit()
        print("Snapshot saved successfully.")  # DEBUG
    finally:
        db.close()


def get_snapshot(session_id: str) -> MemorySnapshot:
    db = SessionLocal()
    try:
        record = db.query(MemorySnapshotDB).filter_by(session_id=session_id).first()
        if not record:
            raise ValueError(f"Snapshot not found for session_id: {session_id}")
        return MemorySnapshot(**record.snapshot)  # ✅ Deserialize to Pydantic
    finally:
        db.close()
