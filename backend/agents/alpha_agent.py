# agents/alpha_agent.py

from backend.app.parsing.alpha_doc_parser import parse_alpha_document
from typing import Dict, Any


from app.core.gemini_rate_limiter import GeminiRateLimiter

limiter = GeminiRateLimiter(rate_limit_per_minute=60)

def alpha_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    alpha_path = state.alpha_path
    if not alpha_path:
        raise ValueError("Missing required 'alpha_path' in state")

    limiter.wait()  # 🛑 wait before hitting Gemini API
    alpha_result = parse_alpha_document(alpha_path)

    return {
        **state.dict(),
        "alpha_data": alpha_result["gemini_analysis"],
        "alpha_raw": alpha_result["raw_data"]
    }
