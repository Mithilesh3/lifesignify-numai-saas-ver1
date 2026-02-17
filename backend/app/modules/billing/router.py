from fastapi import APIRouter, Depends
from app.modules.users.router import get_current_user
from app.modules.billing.service import create_checkout_session
from app.db.models import User

router = APIRouter(tags=["Billing"])

@router.post("/subscribe")
def subscribe(current_user: User = Depends(get_current_user)):
    return create_checkout_session(current_user)
