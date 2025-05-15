# agents/beta_excel_agent.py

from app.parsing.beta_excel_parser import parse_beta_excel

from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument
from workflows.models.shared import TransformationState

def beta_excel_agent_node(state: TransformationState) -> TransformationState:
    beta_excel_path = state.beta_excel_path
    if not beta_excel_path:
        return state  # Skip if not present

    beta_excel_data : ParsedBetaExcelDocument = parse_beta_excel(beta_excel_path, state.alpha_data)
    
    return state.model_copy(update={"beta_excel_data": beta_excel_data})

