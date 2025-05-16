# agents/alpha_agent.py

from app.parsing.alpha_doc_parser import parse_alpha_document
from workflows.models.alpha.alpha_models import ParsedAlphaDocument
from workflows.models.shared import TransformationState

def alpha_agent_node(state: TransformationState) -> TransformationState:
    alpha_path = state.alpha_path
    if not alpha_path:
        raise ValueError("Missing required 'alpha_path' in state")

    alpha_result: ParsedAlphaDocument = parse_alpha_document(alpha_path)
    return state.model_copy(update={"alpha_data": alpha_result})

 