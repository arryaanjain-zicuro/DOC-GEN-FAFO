# backend/agents/utils/mapping_enrichment.py

from typing import Dict, List
from agents.utils.confidence_scorer import compute_confidence_score
from agents.utils.mapping_validator import validate_mapping

#TODO: demo enricher, testing of logic pending
def enrich_mapping(mapping: Dict[str, str]) -> List[Dict[str, any]]:
    enriched = []
    for source, target in mapping.items():
        enriched.append({
            "source": source,
            "target": target,
            "confidence": compute_confidence_score(source, target),
            "is_valid": validate_mapping(source, target)
        })
    return enriched
