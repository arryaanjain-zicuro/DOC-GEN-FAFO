# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.limiter import limiter

app = FastAPI(title="TermSheet AI Generator")

# CORS settings
origins = [
    "http://localhost:5173",  # frontend dev server
    "http://127.0.0.1:5173",
    # Add production domain here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limit middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# Register your API routes
app.include_router(router)
