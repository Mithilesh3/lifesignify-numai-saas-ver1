from sqlalchemy.orm import Session
from app.db.models import Payment, User
from app.core.payment_config import razorpay_client
from datetime import datetime

def create_payment_order(db: Session, current_user: User):

    amount = 49900  # ₹499 in paise

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment(
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        razorpay_order_id=order["id"],
        amount=amount,
        currency="INR",
        status="created",
        created_at=datetime.utcnow()
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "order_id": order["id"],
        "amount": amount,
        "key": razorpay_client.auth[0]
    }

import hmac
import hashlib
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User


def verify_payment_signature(
    db: Session,
    current_user: User,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    razorpay_secret: str
):
    """
    Verify Razorpay signature to confirm payment authenticity.
    """

    try:
        generated_signature = hmac.new(
            bytes(razorpay_secret, 'utf-8'),
            bytes(f"{razorpay_order_id}|{razorpay_payment_id}", 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != razorpay_signature:
            raise HTTPException(status_code=400, detail="Invalid payment signature")

        # ✅ Upgrade user subscription
        current_user.is_premium = True
        db.commit()

        return {"message": "Payment verified. Subscription activated."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
