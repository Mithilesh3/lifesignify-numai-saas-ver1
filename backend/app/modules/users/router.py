from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db.dependencies import get_db
from app.db.models import User, Organization

from app.modules.users.schemas import (
    UserCreate,
    UserResponse,
    TokenResponse,
    PlanUpdate,
)

from app.modules.users.service import (
    create_user,
    login_user,
    update_organization_plan,   # ✅ Service layer update
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
# AUTH DEPENDENCY (Tenant + Soft Delete Safe)
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
            User.tenant_id == int(tenant_id),
            User.is_deleted == False
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="User not found or deleted")

    return user


# =====================================================
# ROLE GUARD
# =====================================================
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# =====================================================
# PLAN GUARD (Soft Delete Safe)
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
# PROTECTED ROUTE
# =====================================================
@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        tenant_id=current_user.tenant_id,
        role=current_user.role,
        plan=current_user.organization.plan
    )


# =====================================================
# ADMIN ONLY ROUTE
# =====================================================
@router.get("/admin-test")
def admin_test(current_user: User = Depends(admin_required)):
    return {
        "message": "You are an admin",
        "email": current_user.email,
        "tenant_id": current_user.tenant_id,
        "role": current_user.role
    }


# =====================================================
# ADMIN UPDATE PLAN ROUTE (SERVICE LAYER SAFE)
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
# PRO PLAN ONLY ROUTE
# =====================================================
@router.get("/pro-feature")
def pro_feature(current_user: User = Depends(pro_plan_required)):
    return {
        "message": "You are using a Pro feature 🚀",
        "tenant_id": current_user.tenant_id
    }
