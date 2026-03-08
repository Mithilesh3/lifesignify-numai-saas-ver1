from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime
from fastapi.responses import StreamingResponse

import json
import traceback

from app.db.models import Report, User, Subscription
from app.core.audit import log_action
from app.core.config import settings
from app.modules.reports.ai_engine import generate_life_signify_report
from app.modules.reports.pdf_engine import generate_report_pdf


# =====================================================
# PLAN LIMITS
# =====================================================

PLAN_LIMITS = {
    "basic": 1,
    "pro": 5,
    "premium": 50,
    "enterprise": 200,
}


# =====================================================
# REPORT ENRICHMENT LAYER
# =====================================================

def enrich_report_content(report_content: dict) -> dict:
    """
    Ensures the report always returns a complete schema.
    Prevents null sections in API responses.
    """

    report_content = report_content or {}

    report_content.setdefault(
        "executive_brief",
        {
            "summary": "Your numerology indicators suggest an adaptive personality with leadership potential.",
            "core_strength": "Strategic thinking and adaptability.",
            "primary_risk": "Financial discipline fluctuations.",
            "strategic_focus": "Build structured financial planning while leveraging leadership ability."
        },
    )

    report_content.setdefault(
        "analysis_sections",
        {
            "career_analysis": "Your numerology pattern supports leadership and entrepreneurial environments.",
            "financial_analysis": "Financial discipline indicators suggest strengthening structured savings habits.",
            "emotional_analysis": "Moderate emotional regulation with occasional impulsive decisions under stress."
        },
    )

    report_content.setdefault(
        "growth_blueprint",
        {
            "phase_1": "Stabilize emotional and financial decision frameworks.",
            "phase_2": "Develop scalable personal or business growth strategies.",
            "phase_3": "Align long-term life strategy with leadership opportunities."
        },
    )

    report_content.setdefault(
        "strategic_guidance",
        {
            "career_strategy": "Focus on leadership-driven roles or entrepreneurial initiatives.",
            "financial_strategy": "Adopt disciplined financial planning and risk evaluation.",
            "life_strategy": "Maintain structured routines and long-term strategic planning."
        },
    )

    report_content.setdefault("business_block", {})
    report_content.setdefault("correction_block", {})
    report_content.setdefault("compatibility_block", {})

    return report_content


# =====================================================
# RADAR DATA
# =====================================================

def get_radar_data(db: Session, current_user: User, report_id: int):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(False),
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    content = report.content or {}
    scores = content.get("core_metrics", {})

    return {
        "Career": scores.get("career_score", 50),
        "Finance": scores.get("financial_score", 50),
        "Emotional": scores.get("emotional_score", 50),
        "Decision": scores.get("decision_score", 50),
        "Stability": scores.get("stability_score", 50),
    }


# =====================================================
# SUBSCRIPTION VALIDATION
# =====================================================

def _validate_and_lock_subscription(db: Session, current_user: User):

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == current_user.tenant_id,
            Subscription.is_active.is_(True),
        )
        .with_for_update()
        .first()
    )

    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")

    if subscription.end_date and subscription.end_date < datetime.utcnow():
        subscription.is_active = False
        db.commit()
        raise HTTPException(status_code=403, detail="Subscription expired")

    return subscription


# =====================================================
# CREATE MANUAL REPORT
# =====================================================

def create_report(db: Session, current_user: User, title: str, content: dict):

    report = Report(
        title=title,
        content=content,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        engine_version="manual",
        confidence_score=75,
    )

    try:

        db.add(report)
        db.commit()
        db.refresh(report)

        log_action(
            db=db,
            user_id=current_user.id,
            tenant_id=current_user.tenant_id,
            action="REPORT_CREATED",
            details={"report_id": report.id},
        )

        return report

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Manual report creation failed")


# =====================================================
# UPDATE REPORT
# =====================================================

def update_report(db: Session, current_user: User, report_id: int, title: str, content: dict):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(False),
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    try:

        report.title = title
        report.content = content
        report.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(report)

        log_action(
            db=db,
            user_id=current_user.id,
            tenant_id=current_user.tenant_id,
            action="REPORT_UPDATED",
            details={"report_id": report.id},
        )

        return report

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Report update failed"
        )


# =====================================================
# SOFT DELETE REPORT
# =====================================================

def soft_delete_report(db: Session, current_user: User, report_id: int):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(False),
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.is_deleted = True
    report.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Report soft deleted"}


# =====================================================
# RESTORE REPORT
# =====================================================

def restore_report(db: Session, current_user: User, report_id: int):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(True),
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Deleted report not found")

    report.is_deleted = False
    report.deleted_at = None

    db.commit()

    return {"message": "Report restored"}


# =====================================================
# HARD DELETE REPORT
# =====================================================

def hard_delete_report(db: Session, current_user: User, report_id: int):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()

    return {"message": "Report permanently deleted"}


# =====================================================
# GENERATE AI REPORT
# =====================================================

def generate_ai_report_service(db: Session, current_user: User, intake_data: dict):

    try:

        subscription = _validate_and_lock_subscription(db, current_user)

        plan_name = (
            intake_data.get("plan_override")
            or subscription.plan_name
            or "basic"
        ).lower()

        if plan_name not in PLAN_LIMITS:
            raise HTTPException(status_code=400, detail="Invalid plan")

        limit = PLAN_LIMITS[plan_name]
        used = subscription.reports_used or 0

        if used >= limit:
            raise HTTPException(
                status_code=403,
                detail="Report limit reached. Upgrade required.",
            )

        normalized_data = {
            "identity": intake_data.get("identity"),
            "birth_details": intake_data.get("birth_details"),
            "focus": intake_data.get("focus"),
            "financial": intake_data.get("financial"),
            "career": intake_data.get("career"),
            "emotional": intake_data.get("emotional"),
            "life_events": intake_data.get("life_events"),
            "calibration": intake_data.get("calibration"),
            "contact": intake_data.get("contact"),
            "current_problem": intake_data.get("current_problem"),
        }

        ai_output = generate_life_signify_report(
            request_data=normalized_data,
            plan_name=plan_name,
        )

        if isinstance(ai_output, str):
            ai_output = json.loads(ai_output)

        ai_output = enrich_report_content(ai_output)

        confidence_score = ai_output.get(
            "disclaimer", {}
        ).get("confidence_score", 80)

        report = Report(
            title=f"Life Signify NumAI Report ({plan_name.title()})",
            content=ai_output,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            engine_version=settings.ENGINE_VERSION,
            confidence_score=confidence_score,
        )

        db.add(report)

        subscription.reports_used = used + 1

        db.commit()
        db.refresh(report)

        return report

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"AI report generation failed: {str(e)}",
        )


# =====================================================
# GET ALL REPORTS
# =====================================================

def get_reports(db: Session, current_user: User):

    return (
        db.query(Report)
        .filter(
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(False),
        )
        .order_by(Report.created_at.desc())
        .all()
    )


# =====================================================
# GET SINGLE REPORT
# =====================================================

def get_report(db: Session, current_user: User, report_id: int):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted.is_(False),
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


# =====================================================
# EXPORT PDF
# =====================================================

def export_report_pdf(db: Session, current_user: User, report_id: int):

    report = get_report(db, current_user, report_id)

    pdf_buffer = generate_report_pdf(report)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=report_{report_id}.pdf"
        },
    )