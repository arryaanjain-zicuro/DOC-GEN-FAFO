# agents/beta_word_agent.py

from parser.beta_doc_parser import parse_beta_document
from typing import Dict, Any


def beta_word_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state_dict = state.dict()  # Convert the LangGraph State object to a regular dictionary
    beta_doc_path = state.beta_word_path
    print("Beta Word path:", beta_doc_path)

    if not beta_doc_path:
        return state  # Skip if not present

    beta_word_result = parse_beta_document(beta_doc_path, state_dict["alpha_data"])
    return {
        **state_dict,
        "beta_word_mapping": beta_word_result["mapping_result"],
        "beta_raw": beta_word_result["beta_raw"]
    }
