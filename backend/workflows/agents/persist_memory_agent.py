# workflows/agents/persist_memory_node.py

from workflows.models.shared import TransformationState
from app.memory.memory_utils import from_state_to_snapshot
from app.memory.memory_store import save_snapshot

def persist_memory_node(state: TransformationState) -> TransformationState:
    if not state.session_id:
        raise ValueError("Cannot persist memory: session_id is missing in TransformationState")
    
    snapshot = from_state_to_snapshot(state, state.session_id)
    save_snapshot(snapshot)
    
    return state
