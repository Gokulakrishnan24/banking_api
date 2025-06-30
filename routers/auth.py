from fastapi import APIRouter, HTTPException
from models import User, Token
from auth_utils import save_token
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

# Static username-password store (replace with DB in production)
VALID_USERS = {
    "admin": "password"
}

@router.post("/login", response_model=Token)
def login(user: User):
    if VALID_USERS.get(user.username) == user.password:
        token = str(uuid.uuid4())
        print("Issued token:", token)  # debug print
        save_token(token)  # Save token in memory
        return Token(access_token=token)
    raise HTTPException(status_code=401, detail="Invalid username or password")