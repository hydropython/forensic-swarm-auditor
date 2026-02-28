from typing import Dict, Any

def tech_lead_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    The Tech Lead: Enforces Pydantic Rigor and Security Standards.
    Final Arbitrator: Synthesizes engineering effort with production reality.
    """
    evidences = state.get("evidences", {})
    opinions = state.get("opinions", [])
    
    # --- FIX: SAFE EVIDENCE EXTRACTION ---
    raw_repo = evidences.get("repo_agent", [])
    repo_findings = raw_repo if isinstance(raw_repo, list) else [raw_repo]
    
    # --- STATUTE OF ENGINEERING: PRECEDENT 1 (Type Safety) ---
    uses_dict_soup = any(
        "dictionary" in str(e.get("rationale", "")).lower() and 
        "BaseModel" not in str(e.get("rationale", "")) 
        for e in repo_findings if isinstance(e, dict)
    )
    
    # --- STATUTE OF ENGINEERING: PRECEDENT 2 (Sandboxing) ---
    is_sandboxed = any(
        "temp_dir" in str(e.get("rationale", "")) or 
        "tempfile" in str(e.get("rationale", "")) 
        for e in repo_findings if isinstance(e, dict)
    )
    is_unprotected_clone = any(
        "os.system" in str(e.get("rationale", "")) and 
        "git clone" in str(e.get("rationale", "")) 
        for e in repo_findings if isinstance(e, dict)
    )

    # --- THE PRAGMATIC SYNTHESIS ---
    score = 5.0
    rulings = []

    if uses_dict_soup:
        score = 3.2
        rulings.append("RULING: Architectural Fragility. The system relies on 'Dict Soups'.")

    if is_unprotected_clone or not is_sandboxed:
        score = 1.0  
        rulings.append("RULING: Security Negligence. Tooling lacks ephemeral sandboxing.")

    argument = " ".join(rulings) if rulings else "Engineering hygiene is exceptional."

    tech_lead_opinion = {
        "judge": "TechLead",
        "score": score,
        "commentary": argument,
        "statute": "Statute of Engineering v2.0"
    }

    # Use the existing opinions list and return the updated dictionary
    return {"opinions": [tech_lead_opinion]}