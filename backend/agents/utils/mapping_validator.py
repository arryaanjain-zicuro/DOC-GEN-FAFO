# backend/agents/utils/mapping_validator.py

def validate_mapping(source: str, target: str) -> bool:
    # TODO: Dummy rule: length mismatch > 80% invalid
    return len(source) > 0 and (len(target) / len(source)) > 0.8
