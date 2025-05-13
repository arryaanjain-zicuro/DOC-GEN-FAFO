# agents/beta_excel_agent.py

from core.beta_excel_parser import parse_beta_excel

def beta_excel_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    beta_excel_path = state.get("beta_excel_path")
    if not beta_excel_path:
        return state  # Skip if not present

    beta_excel_result = parse_beta_excel(beta_excel_path, state["alpha_data"])
    return {
        **state,
        "beta_excel_mapping": beta_excel_result["mapping_result"]
    }
