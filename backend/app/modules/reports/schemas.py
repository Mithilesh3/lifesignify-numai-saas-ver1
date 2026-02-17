from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# =====================================================
# BASIC REPORT CREATE (Manual Report)
# =====================================================

class ReportCreate(BaseModel):
    title: str
    content: Dict[str, Any]   # JSON-based storage


# =====================================================
# REPORT UPDATE
# =====================================================

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


# =====================================================
# REPORT RESPONSE (Enterprise Version)
# =====================================================

class ReportResponse(BaseModel):

    id: int
    title: str

    # Structured AI Output
    content: Dict[str, Any]

    engine_version: str
    confidence_score: int

    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
