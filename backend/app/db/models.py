from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.session import Base


# ==========================================
# ORGANIZATION (TENANT)
# ==========================================
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Subscription Plan
    plan = Column(String, default="free", nullable=False)

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships
    users = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    reports = relationship(
        "Report",
        back_populates="organization",
        cascade="all, delete-orphan"
    )


# ==========================================
# USER
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # Multi-tenant
    tenant_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    # Role-based access
    role = Column(String, default="user", nullable=False)

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships
    organization = relationship("Organization", back_populates="users")

    reports = relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================================
# REPORT (AI Structured Storage)
# ==========================================
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    # 🔥 Structured AI Output (JSONB instead of Text)
    content = Column(JSONB, nullable=False)

    # 🔥 AI Engine Versioning
    engine_version = Column(String, default="v1", nullable=False)

    # 🔥 AI Confidence Score (0–100)
    confidence_score = Column(Integer, default=75)

    tenant_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships
    organization = relationship("Organization", back_populates="reports")
    user = relationship("User", back_populates="reports")


# ==========================================
# AUDIT LOG
# ==========================================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    tenant_id = Column(Integer, index=True, nullable=False)

    action = Column(String, nullable=False)

    # Structured audit metadata
    details = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)

    plan_name = Column(String, default="free")
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tenant_id = Column(Integer)
    razorpay_order_id = Column(String, unique=True)
    razorpay_payment_id = Column(String, nullable=True)
    razorpay_signature = Column(String, nullable=True)
    amount = Column(Integer)
    currency = Column(String, default="INR")
    status = Column(String, default="created")  # created | paid | failed
    created_at = Column(DateTime, default=datetime.utcnow)
