from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from auth_utils import verify_token

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/divide", dependencies=[Depends(verify_token)])
def divide(a: int = Query(...), b: int = Query(...)):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    result = a / b
    return JSONResponse(content={"result": result})