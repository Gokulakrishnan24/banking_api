from fastapi import APIRouter, HTTPException, Path, Query , Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from auth_utils import verify_token

router = APIRouter(prefix="/cards", tags=["Cards"])

# ----------------------------- Models -----------------------------

class BlockCardRequest(BaseModel):
    card_number: str
    reason: str

class UnblockCardRequest(BaseModel):
    card_number: str

class LimitUpdateRequest(BaseModel):
    card_number: str
    new_limit: int

class CardInfo(BaseModel):
    card_number: str
    type: str
    status: str
    limit: int

class CardTransaction(BaseModel):
    date: datetime
    amount: float
    merchant: str

# ----------------------------- Data -----------------------------

dummy_cards = [
    CardInfo(card_number="4111222233334444", type="credit", status="active", limit=50000),
    CardInfo(card_number="5555666677778888", type="debit", status="blocked", limit=100000)
]

dummy_txns = [
    CardTransaction(date=datetime.now(), amount=1234.56, merchant="Amazon"),
    CardTransaction(date=datetime.now(), amount=250.00, merchant="Swiggy")
]

# ----------------------------- Routes -----------------------------

@router.get("/list", response_model=List[CardInfo],dependencies=[Depends(verify_token)])
def list_cards():
    return dummy_cards

@router.post("/block", dependencies=[Depends(verify_token)])
def block_card(request: BlockCardRequest):
    for card in dummy_cards:
        if card.card_number == request.card_number:
            if card.status == "blocked":
                raise HTTPException(status_code=409, detail="Card is already blocked")
            card.status = "blocked"
            return {"message": f"Card {card.card_number} blocked"}
    raise HTTPException(status_code=404, detail="Card not found")


@router.post("/unblock",dependencies=[Depends(verify_token)])
def unblock_card(request: UnblockCardRequest):
    for card in dummy_cards:
        if card.card_number == request.card_number:
            if card.status == "blocked":
                card.status = "active"
                return {"message": f"Card {card.card_number} unblocked"}
            return {"message": "Card is not blocked"}
    raise HTTPException(status_code=404, detail="Card not found")

@router.get("/limits",dependencies=[Depends(verify_token)])
def get_limits(card_number: str = Query(...)):
    for card in dummy_cards:
        if card.card_number == card_number:
            return {"limit": card.limit, "card_number": card.card_number}
    raise HTTPException(status_code=404, detail="Card not found")

@router.patch("/update-limit",dependencies=[Depends(verify_token)])
def update_limit(req: LimitUpdateRequest):
    for card in dummy_cards:
        if card.card_number == req.card_number:
            card.limit = req.new_limit
            return {"message": "Limit updated", "new_limit": req.new_limit}
    raise HTTPException(status_code=404, detail="Card not found")

@router.get("/transactions/{card_number}", response_model=List[CardTransaction],dependencies=[Depends(verify_token)])
def get_card_transactions(card_number: str = Path(...)):
    for card in dummy_cards:
        if card.card_number == card_number:
            return dummy_txns
    raise HTTPException(status_code=404, detail="Card not found")