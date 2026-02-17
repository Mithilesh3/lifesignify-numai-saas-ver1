import stripe
from fastapi import HTTPException
from app.core.stripe_config import STRIPE_WEBHOOK_SECRET
from app.db.models import Subscription


def create_checkout_session(current_user):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": "YOUR_STRIPE_PRICE_ID",
                "quantity": 1,
            }],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            customer_email=current_user.email,
        )
        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
