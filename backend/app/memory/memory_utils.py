# app/utils/memory_utils.py

from workflows.models.memory.memory_snapshot import MemorySnapshot
from workflows.models.shared import TransformationState

def from_state_to_snapshot(state: TransformationState, session_id: str) -> MemorySnapshot:
    return MemorySnapshot(
        session_id=session_id,
        alpha_data=state.alpha_data,
        beta_excel_data=state.beta_excel_data,
        beta_word_data=state.beta_word_data,
    )
