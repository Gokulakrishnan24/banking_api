from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AccountBalance(BaseModel):
    balance: str
    currency: str

class Transaction(BaseModel):
    date: str
    amount: str
    description: str

class TransactionList(BaseModel):
    transactions: List[Transaction]

class LoanStatus(BaseModel):
    loanId: str
    status: str
    principal: str
    interestRate: str
    dueAmount: str
    nextDueDate: str