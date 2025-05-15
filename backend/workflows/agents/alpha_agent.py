# agents/alpha_agent.py

from app.parsing.alpha_doc_parser import parse_alpha_document
from workflows.models.alpha_models import ParsedAlphaDocument
from typing import Dict, Any

from app.core.gemini_rate_limiter import GeminiRateLimiter

limiter = GeminiRateLimiter(rate_limit_per_minute=60)

def alpha_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    alpha_path = state.alpha_path
    if not alpha_path:
        raise ValueError("Missing required 'alpha_path' in state")

    limiter.wait()

    alpha_result: ParsedAlphaDocument = parse_alpha_document(alpha_path)

    return {
        **state.dict(),
        "alpha_data": alpha_result.model_dump(),  # Use model_dump() for compatibility
    }
