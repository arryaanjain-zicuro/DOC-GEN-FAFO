# agents/beta_word_agent.py

from parser.beta_doc_parser import parse_beta_document
from typing import Dict, Any


def beta_word_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    beta_doc_path = state.get("beta_word_path")
    if not beta_doc_path:
        return state  # Skip if not present

    beta_word_result = parse_beta_document(beta_doc_path, state["alpha_data"])
    return {
        **state,
        "beta_word_mapping": beta_word_result["mapping_result"]
    }
