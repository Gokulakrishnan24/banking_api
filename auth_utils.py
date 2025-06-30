from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

# Use Authorization header (Swagger-friendly)
oauth2_scheme = APIKeyHeader(name="Authorization")

# In-memory store for valid tokens
VALID_TOKENS = set()

# Function to save token (called during login)
def save_token(token: str):
    cleaned = token.replace("Bearer ", "")
    print("[SAVE] Token:", cleaned)
    VALID_TOKENS.add(cleaned)
    print("[SAVE] All tokens:", VALID_TOKENS)

# FastAPI dependency to verify token (used in routes)
def verify_token(token: str = Depends(oauth2_scheme)):
    print("[VERIFY] Received:", token)
    cleaned = token.replace("Bearer ", "")
    print("[VERIFY] Stored:", VALID_TOKENS)
    if cleaned not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    return cleaned