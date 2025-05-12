# app/main.py
from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.limiter import limiter

app = FastAPI(title="TermSheet AI Generator")

# Add rate limit middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Optional: Handle rate-limit exceptions cleanly
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# Include routes
app.include_router(router)
