import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./ai_crm.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(String, index=True, nullable=False)
    rep_id = Column(String, index=True, nullable=False)
    interaction_type = Column(String, nullable=False)
    notes = Column(Text)
    summary = Column(Text)
    entities = Column(Text)  # store JSON string
    extra_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_tables():
    Base.metadata.create_all(bind=engine)

async def init_db():
    # synchronous creation is fine at startup for SQLite
    init_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
