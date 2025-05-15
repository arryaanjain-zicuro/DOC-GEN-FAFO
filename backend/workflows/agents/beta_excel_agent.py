# agents/beta_excel_agent.py

from app.parsing.beta_excel_parser import parse_beta_excel
from typing import Dict, Any

from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument

from app.parsing.beta_excel_parser import parse_beta_excel
from typing import Dict, Any

def beta_excel_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    beta_excel_path = state.beta_excel_path
    if not beta_excel_path:
        return state  # Skip if not present

    beta_excel_data : ParsedBetaExcelDocument = parse_beta_excel(beta_excel_path, state.alpha_data)
    
    return {
        **state.dict(),
        "beta_excel_data": beta_excel_data
    }
