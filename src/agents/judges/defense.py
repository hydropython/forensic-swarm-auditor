from typing import Dict, Any

def defense_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    The Defense Attorney: Advocates for the student by finding 
    engineering sophistication hidden behind framework failures.
    """
    evidences = state.get("evidences", {})
    opinions = state.get("opinions", [])
    
    # --- FIX 1: Safe Evidence Extraction ---
    raw_repo = evidences.get("repo_agent", [])
    repo_findings = raw_repo if isinstance(raw_repo, list) else [raw_repo]
    
    # --- FIX 2: Attribute Safety Check ---
    has_complex_parsing = any(
        "AST" in str(e.get("rationale", "")) or "parsing" in str(e.get("rationale", ""))
        for e in repo_findings
        if isinstance(e, dict)
    )
    
    # --- STATUTE OF EFFORT: MITIGATION 2 (Dialectical Tension) ---
    temp_scores = [
        op.get("score", 3) 
        for op in opinions 
        if isinstance(op, dict) and "score" in op
    ]
    has_tension = len(set(temp_scores)) > 1 if temp_scores else False

    # --- THE ARCHITECTURAL DEFENSE (Protocol B-2 Implementation) ---
    if has_complex_parsing:
        score = 4.8
        argument = (
            "The forensic data indicates full compliance with Protocol B-2, particularly "
            "in diagram classification and parallel flow validation. The engineer achieved "
            "deep code comprehension via sophisticated AST parsing logic..."
        )
    elif has_tension:
        score = 4.2
        argument = (
            "While the prosecution alleges oversight, the evidence confirms successful "
            "role separation yielding true dialectical tension..."
        )
    else:
        score = 3.8
        argument = (
            "The defendant demonstrated clear structural intent. The foundational engineering "
            "is sound..."
        )

    defense_opinion = {
        "judge": "Defense",
        "score": score,
        "commentary": argument, 
        "statute": "Protocol B-2: Statute of Effort"
    }

    return {"opinions": [defense_opinion]}