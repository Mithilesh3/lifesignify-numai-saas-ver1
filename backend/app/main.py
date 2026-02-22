from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import time
import traceback

from app.db.session import engine, Base
from app.db import models  # ensures models are registered

from app.modules.users.router import router as users_router
from app.modules.reports.router import router as reports_router
from app.modules.payments.router import router as payments_router
from app.modules.admin.router import router as admin_router

from app.core.engine_config import ENGINE_VERSION


# =====================================================
# APP INITIALIZATION
# =====================================================

app = FastAPI(title="Life Signify NumAI SaaS")


# =====================================================
# CORS CONFIG (DEV SAFE VERSION)
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 If you still face issues in development,
# temporarily replace allow_origins with:
# allow_origins=["*"]
# (Do NOT use "*" in production)


# =====================================================
# GLOBAL EXCEPTION HANDLER
# =====================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("🔥 Unhandled Exception:")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "detail": str(exc),
        },
    )


# =====================================================
# DATABASE STARTUP RETRY (Docker-Safe)
# =====================================================

@app.on_event("startup")
def startup_event():
    MAX_RETRIES = 10
    RETRY_DELAY = 3

    for attempt in range(MAX_RETRIES):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected successfully.")
            return
        except OperationalError:
            print(f"⏳ Database not ready. Retry {attempt + 1}/{MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)

    raise Exception("❌ Could not connect to database after multiple attempts.")


# =====================================================
# ROUTERS
# =====================================================

app.include_router(users_router, prefix="/api/users")
app.include_router(reports_router, prefix="/api/reports")
app.include_router(payments_router, prefix="/api/payments")
app.include_router(admin_router)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "status": "Life Signify NumAI SaaS Running 🚀",
        "engine_version": ENGINE_VERSION
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health", tags=["System"])
def health_check():
    db_status = "unknown"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "connected"
    except SQLAlchemyError:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "service": "Life Signify NumAI",
        "engine_version": ENGINE_VERSION,
        "database": db_status
    }