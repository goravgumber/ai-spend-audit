from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class ToolEntryInput(BaseModel):
    tool: str
    plan: str
    monthly_spend: float
    seats: int
    use_case: str


class AuditCreateRequest(BaseModel):
    tool_entries: list[ToolEntryInput]


class ToolResultResponse(BaseModel):
    tool: str
    current_plan: str
    current_monthly_spend: float
    recommended_plan: str
    recommended_monthly_spend: float
    monthly_savings: float
    annual_savings: float
    reason: str
    action: str
    credex_opportunity: bool


class AuditResponse(BaseModel):
    id: UUID
    share_token: UUID
    tool_results: list[ToolResultResponse]
    total_current_monthly_spend: float
    total_monthly_savings: float
    total_annual_savings: float
    credex_opportunity: bool
    summary: Optional[str]
    created_at: datetime


class LeadCreateRequest(BaseModel):
    audit_id: UUID
    email: str
    company_name: Optional[str] = None
    role: Optional[str] = None
    team_size: Optional[str] = None


class LeadResponse(BaseModel):
    id: UUID
    audit_id: UUID
    email: str