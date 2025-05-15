# app/agents/mapper_agent.py

from langgraph.graph import State
from typing import Annotated
from models.mapper_models import MapperState
from app.parsing.mapper_logic import run_mapper_agent


def mapper_agent_node(state: Annotated[MapperState, State]) -> MapperState:
    beta_type = state.beta_type  # "word" or "excel"

    if beta_type == "word":
        beta_data = state.beta_word_data
    elif beta_type == "excel":
        beta_data = state.beta_excel_data
    else:
        raise ValueError(f"Invalid beta_type: {beta_type}")

    result = run_mapper_agent(
        alpha_data=state.alpha_data,
        beta_data=beta_data,
        beta_type=beta_type
    )

    return MapperState(
        **state.dict(),
        mapper_output=result
    )
