# agents/beta_word_agent.py

from app.parsing.beta_word_parser import parse_beta_word
from agents.utils.mapping_enrichment import enrich_mapping
from typing import Dict, Any


def beta_word_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state_dict = state.dict()
    beta_doc_path = state.beta_word_path
    print("Beta Word path:", beta_doc_path)

    if not beta_doc_path:
        return state  # Skip if not present

    beta_word_result = parse_beta_word(beta_doc_path, state_dict["alpha_data"])
    
    enriched_mapping = enrich_mapping(beta_word_result["mapping_result"])

    return {
        **state_dict,
        "beta_word_mapping": enriched_mapping,
        "beta_raw": beta_word_result["beta_raw"]
    }
