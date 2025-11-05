from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, String, Boolean, DateTime, JSON, ForeignKey, Integer, Text, UniqueConstraint
)

Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"

    id = Column(String, primary_key=True)  # Slack channel ID
    name = Column(String, index=True)
    is_private = Column(Boolean, default=False)
    raw = Column(JSON)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # Slack user ID
    real_name = Column(String)
    display_name = Column(String, index=True)
    email = Column(String, index=True)
    raw = Column(JSON)


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)  # composite key suggestion: f"{channel_id}:{ts}"
    channel_id = Column(String, index=True)
    user_id = Column(String, index=True)
    text = Column(Text)
    ts = Column(String, index=True)  # Slack timestamp string
    thread_ts = Column(String, index=True, nullable=True)
    edited_ts = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)
    raw = Column(JSON)
    ingested_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('channel_id', 'ts', name='uq_channel_ts'),)


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, index=True)
    user_id = Column(String, index=True)
    name = Column(String, index=True)  # e.g., ":thumbsup:"
    ts = Column(String)


class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True)  # Slack file id
    message_id = Column(String, index=True)
    uploader_id = Column(String, index=True)
    name = Column(String)
    mimetype = Column(String)
    url_private = Column(Text)
    raw = Column(JSON)
