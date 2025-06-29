from fastapi import FastAPI, Depends
from routers import auth, account, loan, transaction , debug , cards


app = FastAPI(title="Banking API with JWT")

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(loan.router)
app.include_router(transaction.router)
app.include_router(debug.router)
app.include_router(cards.router)



