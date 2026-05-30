from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi import WebSocket
from webstock import websocket_endpoint
from database import Base, engine, SessionLocal
from models import User
from auth import (
    hash_password,
    verify_password
)
from jwt_handler import (
    create_access_token
)
from ai_engine import (
    analyze_password
)
from security_logger import (
    log_security_event
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adaptive Credential Intelligence",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordRequest(BaseModel):
    password: str


# -------------------------
# Home Route
# -------------------------

@app.get("/")
def home():

    return {
        "message": "Adaptive Credential Intelligence Running"
    }


# -------------------------
# Register
# -------------------------

@app.post("/register")
def register(data: RegisterRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:

        return {
            "success": False,
            "message": "Email already exists"
        }

    hashed_password = hash_password(
        data.password
    )

    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    log_security_event(
        "USER_REGISTERED",
        data.email
    )

    return {
        "success": True,
        "message": "User Registered Successfully"
    }


# -------------------------
# Login
# -------------------------

@app.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:

        log_security_event(
            "LOGIN_FAILED",
            data.email
        )

        return {
            "success": False,
            "message": "User not found"
        }

    if not verify_password(
        data.password,
        user.password
    ):

        log_security_event(
            "INVALID_PASSWORD",
            data.email
        )

        return {
            "success": False,
            "message": "Invalid password"
        }

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    log_security_event(
        "LOGIN_SUCCESS",
        user.email
    )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# AI Password Analysis
# -------------------------

@app.post("/analyze")
def analyze(data: PasswordRequest):

    result = analyze_password(
        data.password
    )

    return result


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
@app.websocket("/ws")
async def websocket_route(
    websocket: WebSocket
):
    await websocket_endpoint(
        websocket
    )