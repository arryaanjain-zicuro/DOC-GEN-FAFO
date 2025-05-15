# agents/beta_word_agent.py

from app.parsing.beta_word_parser import parse_beta_word
from typing import Dict, Any
from workflows.models.betaWord.beta_word_models import ParsedBetaWordDocument

def beta_word_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state_dict = state.dict()
    beta_doc_path = state.beta_word_path
    if not beta_doc_path:
        return state  # Skip if not present

    beta_word_data : ParsedBetaWordDocument = parse_beta_word(beta_doc_path, state_dict["alpha_data"])

    return {
        **state_dict,
        "beta_word_data": beta_word_data
    }
