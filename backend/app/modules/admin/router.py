from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.dependencies import get_db
from app.modules.users.router import admin_required
from app.db.models import User, Report

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/analytics")
def get_admin_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_users = db.query(func.count(User.id)).scalar()
    total_reports = db.query(func.count(Report.id)).scalar()
    premium_users = db.query(func.count(User.id)).filter(User.plan == "premium").scalar()

    return {
        "total_users": total_users,
        "total_reports": total_reports,
        "premium_users": premium_users,
        "conversion_rate": round((premium_users / total_users) * 100, 2) if total_users else 0
    }
