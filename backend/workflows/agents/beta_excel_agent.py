# agents/beta_excel_agent.py

from app.parsing.beta_excel_parser import parse_beta_excel
from agents.utils.mapping_enrichment import enrich_mapping
from typing import Dict, Any


def beta_excel_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state_dict = state.dict()
    beta_excel_path = state.beta_excel_path
    if not beta_excel_path:
        return state  # Skip if not present

    beta_excel_result = parse_beta_excel(beta_excel_path, state_dict["alpha_data"])

    enriched_mapping = enrich_mapping(beta_excel_result["mapping_result"])

    return {
        **state_dict,
        "beta_excel_mapping": enriched_mapping,
        "beta_excel_raw": beta_excel_result["beta_raw"]
    }
