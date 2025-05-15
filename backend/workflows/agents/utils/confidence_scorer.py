# backend/agents/utils/confidence_scorer.py
def compute_confidence_score(source: str, target: str) -> float:
    # TODO: dummy example, replace with actual NLP-based confidence logic
    from difflib import SequenceMatcher
    return round(SequenceMatcher(None, source.lower(), target.lower()).ratio(), 2)
