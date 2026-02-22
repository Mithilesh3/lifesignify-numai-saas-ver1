from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db.dependencies import get_db
from app.db.models import User, Organization, Subscription

from app.modules.users.schemas import (
    UserCreate,
    UserResponse,
    TokenResponse,
    PlanUpdate,
)

from app.modules.users.service import (
    create_user,
    login_user,
    update_organization_plan,
)

from app.core.security import decode_access_token


router = APIRouter(tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


# =====================================================
# REGISTER
# =====================================================
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = create_user(
        db,
        user.email,
        user.password,
        user.organization_name
    )

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        tenant_id=new_user.tenant_id,
        role=new_user.role,
        plan=new_user.organization.plan
    )


# =====================================================
# LOGIN
# =====================================================
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = login_user(db, form_data.username, form_data.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return result


# =====================================================
# AUTH DEPENDENCY
# =====================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")

    if not user_id or not tenant_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id),
            User.tenant_id == int(tenant_id)
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# =====================================================
# ADMIN GUARD  ✅ ADDED BACK
# =====================================================
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# =====================================================
# PRO PLAN GUARD  ✅ SAFE VERSION
# =====================================================
def pro_plan_required(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    organization = (
        db.query(Organization)
        .filter(
            Organization.id == current_user.tenant_id,
            Organization.is_deleted == False
        )
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if organization.plan not in ["pro", "enterprise"]:
        raise HTTPException(
            status_code=403,
            detail="Upgrade to Pro plan required"
        )

    return current_user


# =====================================================
# CURRENT USER DETAILS
# =====================================================
@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == current_user.tenant_id,
            Subscription.is_active == True
        )
        .first()
    )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "organization": {
            "id": current_user.organization.id,
            "name": current_user.organization.name,
            "plan": current_user.organization.plan,
        },
        "subscription": {
            "plan_name": subscription.plan_name if subscription else "basic",
            "is_active": subscription.is_active if subscription else False,
            "end_date": subscription.end_date if subscription else None,
            "reports_used": subscription.reports_used if subscription else 0,
        }
    }


# =====================================================
# ADMIN UPDATE PLAN
# =====================================================
@router.put("/update-plan")
def update_plan(
    plan_data: PlanUpdate,
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    organization = update_organization_plan(
        db=db,
        current_user=current_user,
        new_plan=plan_data.plan
    )

    return {
        "message": "Plan updated successfully",
        "new_plan": organization.plan
    }


# =====================================================
# ADMIN TEST
# =====================================================
@router.get("/admin-test")
def admin_test(current_user: User = Depends(admin_required)):
    return {
        "message": "You are an admin",
        "email": current_user.email
    }