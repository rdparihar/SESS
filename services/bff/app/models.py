from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    members = relationship("User", back_populates="team")
    projects = relationship("Project", back_populates="team")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    team = relationship("Team", back_populates="members")
    pto = relationship("PTO", back_populates="user")
    allocations = relationship("Allocation", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    team = relationship("Team", back_populates="projects")
    incidents = relationship("Incident", back_populates="project")
    ci_events = relationship("CIEvent", back_populates="project")
    runbooks = relationship("Runbook", back_populates="project")
    allocations = relationship("Allocation", back_populates="project")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    status = Column(String(64), nullable=False, default="open")
    severity = Column(String(32), nullable=True)
    detected_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    project = relationship("Project", back_populates="incidents")


class CIEvent(Base):
    __tablename__ = "ci_events"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(255), nullable=True)
    provider = Column(String(64), nullable=False)
    status = Column(String(64), nullable=False)
    occurred_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="ci_events")


class Runbook(Base):
    __tablename__ = "runbooks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="runbooks")


class PTO(Base):
    __tablename__ = "pto"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(64), nullable=False, default="approved")

    user = relationship("User", back_populates="pto")


class Allocation(Base):
    __tablename__ = "allocations"
    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_allocation_user_project"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    percent = Column(Integer, nullable=False)

    user = relationship("User", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")


class SyncCursor(Base):
    __tablename__ = "sync_cursors"
    __table_args__ = (UniqueConstraint("source", "stream", name="uq_sync_cursor_source_stream"),)

    id = Column(Integer, primary_key=True)
    source = Column(String(64), nullable=False)
    stream = Column(String(64), nullable=False)
    cursor_value = Column(String(255), nullable=True)
    rate_limit_reset = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True)
    source = Column(String(64), nullable=False)
    external_id = Column(String(255), nullable=True)
    payload = Column(Text, nullable=False)
    received_at = Column(DateTime, nullable=False, default=datetime.utcnow)

