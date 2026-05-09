import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.audit import Audit, Lead
from app.schemas.audit import (
    AuditCreateRequest,
    AuditResponse,
    LeadCreateRequest,
    LeadResponse,
)
from app.services.audit_engine import run_full_audit

router = APIRouter(prefix="/audits", tags=["audits"])


@router.post("/", response_model=AuditResponse)
def create_audit(request: AuditCreateRequest, db: Session = Depends(get_db)):
    # Convert pydantic models to dicts for audit engine
    tool_entries = [entry.model_dump() for entry in request.tool_entries]

    # Run the audit engine
    audit_results = run_full_audit(tool_entries)

    # Save to database
    audit = Audit(
        tool_entries=tool_entries,
        results=audit_results["tool_results"],
        total_monthly_savings=audit_results["total_monthly_savings"],
        total_annual_savings=audit_results["total_annual_savings"],
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    return AuditResponse(
        id=audit.id,
        share_token=audit.share_token,
        tool_results=audit_results["tool_results"],
        total_current_monthly_spend=audit_results["total_current_monthly_spend"],
        total_monthly_savings=audit_results["total_monthly_savings"],
        total_annual_savings=audit_results["total_annual_savings"],
        credex_opportunity=audit_results["credex_opportunity"],
        summary=audit.summary,
        created_at=audit.created_at,
    )


@router.get("/{share_token}/public")
def get_public_audit(share_token: uuid.UUID, db: Session = Depends(get_db)):
    audit = db.query(Audit).filter(Audit.share_token == share_token).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    # Return public version - no PII
    return {
        "tool_results": audit.results,
        "total_monthly_savings": float(audit.total_monthly_savings),
        "total_annual_savings": float(audit.total_annual_savings),
        "credex_opportunity": any(
            r.get("credex_opportunity") for r in audit.results
        ),
    }


@router.post("/leads", response_model=LeadResponse)
def capture_lead(request: LeadCreateRequest, db: Session = Depends(get_db)):
    lead = Lead(
        audit_id=request.audit_id,
        email=request.email,
        company_name=request.company_name,
        role=request.role,
        team_size=request.team_size,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return LeadResponse(id=lead.id, audit_id=lead.audit_id, email=lead.email)