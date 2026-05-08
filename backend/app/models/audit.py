import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base


class Audit(Base):
    __tablename__ = "audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    tool_entries = Column(JSONB, nullable=False)
    results = Column(JSONB, nullable=True)
    total_monthly_savings = Column(Numeric(10, 2), default=0)
    total_annual_savings = Column(Numeric(10, 2), default=0)
    summary = Column(Text, nullable=True)
    share_token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"))
    email = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    role = Column(String, nullable=True)
    team_size = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)