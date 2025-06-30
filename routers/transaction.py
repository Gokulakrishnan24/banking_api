from fastapi import APIRouter, Depends, Header, HTTPException ,Depends
from models import Transaction, TransactionList
from faker import Faker
from random import randint, choice
from auth_utils import verify_token

router = APIRouter(prefix="/transaction", tags=["Transaction"],)

fake = Faker()

def generate_transactions(n=1):
    return [
        Transaction(
            date=fake.date_this_year().isoformat(),
            amount=f"{choice(['CR', 'DR'])}{randint(100, 10000)}",
            description=fake.bs().capitalize()
        )
        for _ in range(n)
    ]

@router.get("/history", response_model=TransactionList, dependencies=[Depends(verify_token)])
def get_transaction_history():
    return TransactionList(transactions=generate_transactions())