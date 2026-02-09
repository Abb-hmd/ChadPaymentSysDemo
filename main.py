"""
ChadPay Mobile Money Payment System
====================================
Proof of Concept for N'Djamena, Chad

A lightweight, USSD-based mobile money payment system that enables
transport operators and street vendors to accept payments without
direct API integration with mobile money providers.

Stack: FastAPI + Jinja2 + HTMX + Tailwind CSS + SQLite
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.database import init_database
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("🚀 Starting ChadPay...")
    init_database()
    print("✅ Database initialized")
    
    # Ensure QR codes directory exists
    qr_dir = os.path.join("app", "static", "qr_codes")
    os.makedirs(qr_dir, exist_ok=True)
    
    yield
    
    # Shutdown
    print("👋 Shutting down ChadPay...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Mobile money payment system for transport operators and vendors in Chad",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")


# ==================== ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page - redirect to appropriate dashboard or info page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


# Import and include routers
from app.routers import public, merchant, admin

app.include_router(public.router, tags=["public"])
app.include_router(merchant.router, prefix="/merchant", tags=["merchant"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
