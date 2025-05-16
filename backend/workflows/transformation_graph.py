from langgraph.graph import StateGraph, END
from workflows.models.shared import TransformationState
from workflows.agents.alpha_agent import alpha_agent_node
from workflows.agents.beta_word_agent import beta_word_agent_node
from workflows.agents.beta_excel_agent import beta_excel_agent_node
from workflows.agents.persist_memory_agent import persist_memory_node #✅ NEW

def transformation_graph():
    builder = StateGraph(TransformationState)

    # Add agent nodes
    builder.add_node("alpha_agent", alpha_agent_node)
    builder.add_node("beta_word_agent", beta_word_agent_node)
    builder.add_node("beta_excel_agent", beta_excel_agent_node)
    builder.add_node("persist_memory_node", persist_memory_node)  # ✅ NEW

    # Set entry point
    builder.set_entry_point("alpha_agent")

    # Define edges
    builder.add_edge("alpha_agent", "beta_word_agent")
    builder.add_edge("beta_word_agent", "beta_excel_agent")
    builder.add_edge("beta_excel_agent", "persist_memory_node")  # ✅ NEW
    builder.add_edge("persist_memory_node", END)  # ✅ NEW

    return builder.compile()
