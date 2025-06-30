from fastapi import APIRouter, Depends
from models import LoanStatus
from auth_utils import verify_token

router = APIRouter(prefix="/loan", tags=["Loan"])

@router.get("/status", response_model=LoanStatus, dependencies=[Depends(verify_token)])
def get_loan_status():
    return LoanStatus(
        loanId="LN456789",
        status="Active",
        principal="₹5,00,000",
        interestRate="8.5%",
        dueAmount="₹25,000",
        nextDueDate="2025-07-10"
    )