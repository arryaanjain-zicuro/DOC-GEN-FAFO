# workflows/transformation_graph.py

from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from typing import Optional, Dict, Any
from agents.alpha_agent import alpha_agent_node
from agents.beta_word_agent import beta_word_agent_node
from agents.beta_excel_agent import beta_excel_agent_node

from pydantic import BaseModel

#the state schema (updated)
class State(BaseModel):
    alpha_path: Optional[str] = None
    beta_word_path: Optional[str] = None
    beta_excel_path: Optional[str] = None

    alpha_data: Optional[Dict[str, Any]] = None
    alpha_raw: Optional[Dict[str, Any]] = None

    beta_word_mapping: Optional[Dict[str, Any]] = None
    beta_raw: Optional[Dict[str, Any]] = None

    beta_excel_mapping: Optional[Dict[str, Any]] = None
    beta_excel_raw: Optional[Dict[str, Any]] = None
# Build the LangGraph DAG
def build_transformation_graph():
    builder = StateGraph(State)

    # Nodes
    builder.add_node("parse_alpha", alpha_agent_node)
    builder.add_node("analyze_beta_word", beta_word_agent_node)
    builder.add_node("analyze_beta_excel", beta_excel_agent_node)

    # Edges (sequential for now, parallel later if needed)
    builder.set_entry_point("parse_alpha")
    builder.add_edge("parse_alpha", "analyze_beta_word")
    builder.add_edge("analyze_beta_word", "analyze_beta_excel")
    builder.add_edge("analyze_beta_excel", END)

    return builder.compile()
