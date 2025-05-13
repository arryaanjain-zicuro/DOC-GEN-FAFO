# agents/alpha_agent.py

from core.alpha_doc_parser import parse_alpha_document

def alpha_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    alpha_path = state["alpha_path"]
    alpha_result = parse_alpha_document(alpha_path)
    return {
        **state,
        "alpha_data": alpha_result["gpt_analysis"],
        "alpha_raw": alpha_result["raw_data"]
    }
