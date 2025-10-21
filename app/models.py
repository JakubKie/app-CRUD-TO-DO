from datetime import datetime, timezone
from sqlalchemy import (Column, Integer, String, DateTime, Date, Enum, ForeignKey, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    pending = 'pending'
    in_progress = 'in-progress'
    completed = 'completed'

class PriorityEnum(str, enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    role = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    due_date = Column(Date, nullable=True)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium, nullable=False)

    user = relationship('User', back_populates='tasks')

def get_engine(database_url: str):
    return create_engine(database_url, future=True)

def get_sessionmaker(database_url: str):
    engine = get_engine(database_url)
    return sessionmaker(bind=engine, expire_on_commit=False)
