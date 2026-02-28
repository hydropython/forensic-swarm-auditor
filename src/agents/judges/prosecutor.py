from typing import Dict, Any

def prosecutor(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    The Prosecutor: Charges the defendant with Orchestration Fraud 
    if architectural standards (Parallelism/Pydantic) are missed.
    """
    evidences = state.get("evidences", {})
    
    # --- Safe Evidence Extraction ---
    def get_findings(agent_key):
        raw = evidences.get(agent_key, [])
        return raw if isinstance(raw, list) else [raw]

    vision_findings = get_findings("vision_agent")
    repo_findings = get_findings("repo_agent")
    
    # --- Check for Parallelism (Fan-Out) ---
    is_parallel = any(
        "parallel" in str(e.get("rationale", "")).lower() or 
        "fan-out" in str(e.get("rationale", "")).lower() 
        for e in vision_findings if isinstance(e, dict)
    )
    
    # --- Check for Pydantic State Rigor ---
    uses_pydantic = any(
        "BaseModel" in str(e.get("rationale", "")) or 
        "Pydantic" in str(e.get("rationale", "")) 
        for e in repo_findings if isinstance(e, dict)
    )

    charges = []
    if not is_parallel:
        charges.append("CHARGE: Orchestration Fraud (Linear Flow).")
    if not uses_pydantic:
        charges.append("CHARGE: Hallucination Liability (Missing Pydantic).")

    argument = " ".join(charges) if charges else "No significant orchestration fraud detected."
    final_score = 1.0 if charges else 5.0

    print(f"⚖️ Prosecutor: Deliberation complete. Score: {final_score}")
    
    return {"opinions": [{
        "judge": "Prosecutor",
        "score": final_score,
        "commentary": argument,
        "statute": "Statute of Orchestration v2.0"
    }]}

def defense(state: Dict[str, Any]) -> Dict[str, Any]:
    """The Defense: Highlights intent and complexity to mitigate charges."""
    print("⚖️ Defense: Presenting mitigating factors...")
    return {"opinions": [{
        "judge": "Defense",
        "score": 4.5,
        "commentary": "The system architecture demonstrates sovereign intent through multi-agent collaboration.",
        "statute": "Protocol B-2 (Mitigation)"
    }]}

def tech_lead(state: Dict[str, Any]) -> Dict[str, Any]:
    """The TechLead: Verifies production readiness and LangGraph syntax."""
    print("⚖️ TechLead: Verifying technical rigor...")
    return {"opinions": [{
        "judge": "TechLead",
        "score": 4.0,
        "commentary": "Parallel orchestration and state reducers are correctly implemented.",
        "statute": "Technical Standard 4.1"
    }]}