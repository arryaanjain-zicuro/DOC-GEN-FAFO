from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="TermSheet AI Generator")
app.include_router(router)
