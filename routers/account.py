from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from auth_utils import verify_token

router = APIRouter(prefix="/account", tags=["Account"])

# ---------------- Global In-Memory Store ---------------- #
current_contact = {
    "email": "john@example.com",
    "phone": "9876543210"
}

# ---------------- Models ---------------- #

class AccountBalance(BaseModel):
    balance: str
    currency: str

class AccountDetails(BaseModel):
    account_number: str
    name: str
    ifsc: str
    branch: str
    email: Optional[str]
    phone: Optional[str]

class UpdateContactRequest(BaseModel):
    email: Optional[str]
    phone: Optional[str]

class MiniStatement(BaseModel):
    date: str
    description: str
    amount: float

class Nominee(BaseModel):
    name: str
    relationship: str

class NomineeUpdateRequest(BaseModel):
    name: str
    relationship: str

class ChequeStatus(BaseModel):
    cheque_number: str
    status: str

class EStatementRequest(BaseModel):
    email: str
    month: str

class BlockAccountRequest(BaseModel):
    reason: str

class ActivateAccountRequest(BaseModel):
    activation_code: str

# ---------------- Routes ---------------- #

@router.get("/balance", response_model=AccountBalance, dependencies=[Depends(verify_token)])
def get_balance():
    return AccountBalance(balance="₹2,45,678", currency="INR")

@router.get("/details", response_model=AccountDetails, dependencies=[Depends(verify_token)])
def get_account_details():
    return AccountDetails(
        account_number="1234567890",
        name="John Doe",
        ifsc="IDFC0001234",
        branch="Bangalore MG Road",
        email=current_contact["email"],
        phone=current_contact["phone"]
    )

@router.put("/update-contact", dependencies=[Depends(verify_token)])
def update_contact(req: UpdateContactRequest):
    if req.email:
        current_contact["email"] = req.email
    if req.phone:
        current_contact["phone"] = req.phone
    return {
        "message": "Contact details updated",
        "updated": current_contact
    }

@router.get("/mini-statement", response_model=List[MiniStatement], dependencies=[Depends(verify_token)])
def get_mini_statement():
    return [
        MiniStatement(date="2025-06-01", description="ATM Withdrawal", amount=-2000),
        MiniStatement(date="2025-06-03", description="Salary", amount=50000)
    ]

@router.get("/nominee", response_model=Nominee, dependencies=[Depends(verify_token)])
def get_nominee():
    return Nominee(name="Jane Doe", relationship="Spouse")

@router.put("/update-nominee", dependencies=[Depends(verify_token)])
def update_nominee(req: NomineeUpdateRequest):
    return {"message": f"Nominee updated to {req.name} ({req.relationship})"}

@router.get("/cheque-status", response_model=ChequeStatus, dependencies=[Depends(verify_token)])
def cheque_status(cheque_number: str = Query(...)):
    return ChequeStatus(cheque_number=cheque_number, status="Cleared")

@router.post("/e-statement", dependencies=[Depends(verify_token)])
def request_e_statement(req: EStatementRequest):
    return {"message": f"E-statement for {req.month} sent to {req.email}"}

@router.post("/block", dependencies=[Depends(verify_token)])
def block_account(req: BlockAccountRequest):
    return {"message": f"Account blocked due to: {req.reason}"}

@router.post("/activate", dependencies=[Depends(verify_token)])
def activate_account(req: ActivateAccountRequest):
    if req.activation_code == "123456":
        return {"message": "Account successfully activated"}
    raise HTTPException(status_code=400, detail="Invalid activation code")
