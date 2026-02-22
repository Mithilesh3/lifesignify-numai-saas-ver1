from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.db.models import Report, User, Subscription
from app.core.audit import log_action
from app.core.engine_config import ENGINE_VERSION


# =====================================================
# PLAN LIMITS
# =====================================================
PLAN_LIMITS = {
    "basic": 10,
    "pro": 50,
    "enterprise": 999999
}


# =====================================================
# CREATE MANUAL REPORT
# =====================================================
def create_report(
    db: Session,
    current_user: User,
    title: str,
    content: dict
):
    try:
        report = Report(
            title=title,
            content=content,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            engine_version="manual",
            confidence_score=75
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        log_action(
            db=db,
            user_id=current_user.id,
            tenant_id=current_user.tenant_id,
            action="REPORT_CREATED",
            details={"report_id": report.id}
        )

        return report

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Manual report creation failed"
        )


# =====================================================
# CREATE AI REPORT
# =====================================================
def create_ai_report(
    db: Session,
    current_user: User,
    intake_data: dict
):
    try:
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.tenant_id == current_user.tenant_id,
                Subscription.is_active == True
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=403,
                detail="Active subscription required"
            )

        # Expiry check
        if hasattr(subscription, "end_date") and subscription.end_date:
            if subscription.end_date < datetime.utcnow():
                subscription.is_active = False
                db.commit()
                raise HTTPException(
                    status_code=403,
                    detail="Subscription expired"
                )

        limit = PLAN_LIMITS.get(subscription.plan_name, 10)

        if hasattr(subscription, "reports_used"):
            if subscription.reports_used >= limit:
                raise HTTPException(
                    status_code=403,
                    detail="Report limit reached"
                )

        from app.modules.reports.ai_engine import generate_life_signify_report

        ai_output = generate_life_signify_report(intake_data)

        report = Report(
            title="Life Signify NumAI Report",
            content=ai_output,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            engine_version=ENGINE_VERSION,
            confidence_score=ai_output.get("disclaimer", {}).get("confidence_score", 70)
        )

        db.add(report)

        if hasattr(subscription, "reports_used"):
            subscription.reports_used += 1

        db.commit()
        db.refresh(report)

        log_action(
            db=db,
            user_id=current_user.id,
            tenant_id=current_user.tenant_id,
            action="AI_REPORT_GENERATED",
            details={"report_id": report.id}
        )

        return report

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"AI report failed: {str(e)}"
        )


# =====================================================
# GET ALL REPORTS
# =====================================================
def get_reports(db: Session, current_user: User):
    return (
        db.query(Report)
        .filter(
            Report.tenant_id == current_user.tenant_id,
            Report.is_deleted == False
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
            Report.is_deleted == False
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


# =====================================================
# GET RADAR DATA
# =====================================================
def get_radar_data(
    db: Session,
    current_user: User,
    report_id: int
):
    report = get_report(db, current_user, report_id)

    radar_data = report.content.get("radar_chart_data")

    if not radar_data:
        raise HTTPException(
            status_code=404,
            detail="Radar data not available"
        )

    return radar_data


# =====================================================
# UPDATE REPORT
# =====================================================
def update_report(
    db: Session,
    current_user: User,
    report_id: int,
    title: str,
    content: dict
):
    report = get_report(db, current_user, report_id)

    report.title = title
    report.content = content

    db.commit()
    db.refresh(report)

    return report


# =====================================================
# SOFT DELETE REPORT
# =====================================================
def soft_delete_report(db: Session, current_user: User, report_id: int):
    report = get_report(db, current_user, report_id)
    report.is_deleted = True
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
            Report.is_deleted == True
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Deleted report not found")

    report.is_deleted = False
    db.commit()

    return {"message": "Report restored"}


# =====================================================
# HARD DELETE REPORT
# =====================================================
def hard_delete_report(db: Session, current_user: User, report_id: int):
    report = get_report(db, current_user, report_id)
    db.delete(report)
    db.commit()
    return {"message": "Report permanently deleted"}


from fastapi.responses import StreamingResponse
from app.modules.reports.pdf_engine import generate_report_pdf


# =====================================================
# EXPORT REPORT PDF
# =====================================================
def export_report_pdf(
    db: Session,
    current_user: User,
    report_id: int
):
    report = get_report(db, current_user, report_id)

    pdf_buffer = generate_report_pdf(report)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=report_{report_id}.pdf"
        }
    )