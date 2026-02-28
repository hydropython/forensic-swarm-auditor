from typing import Dict, Any, List
from src.core.state import AgentState, Opinion

def tech_lead_node(state: AgentState) -> Dict[str, Any]:
    """
    The Tech Lead: Final Arbitrator for Engineering Standards.
    Maps rulings directly to the 10-Point Rubric for Executive Grade reporting.
    """
    evidences = state.get("evidences", {})
    repo_findings = evidences.get("repo_agent", [])
    
    # --- FORENSIC CHECKS ---
    uses_dict_soup = any("dictionary" in str(f).lower() and "basemodel" not in str(f).lower() for f in repo_findings)
    is_sandboxed = any("temp_dir" in str(f).lower() or "tempfile" in str(f).lower() for f in repo_findings)
    has_error_handling = any("try" in str(f).lower() or "except" in str(f).lower() for f in repo_findings)

    new_opinions = []

    # --- RULING: Criterion #3 (State Management) ---
    new_opinions.append(Opinion(
        judge="TechLead",
        criterion="State Rigor",
        score=5.0 if not uses_dict_soup else 2.5,
        argument="[arch] VERDICT: Schema Integrity is sound." if not uses_dict_soup else 
                 "[arch] RULING: Architectural Fragility. Detected 'Dict Soups' in agent returns. ACTION: Enforce Pydantic BaseModels.",
        statute="Technical Standard 4.1"
    ))

    # --- RULING: Criterion #9 (Security Hygiene) ---
    new_opinions.append(Opinion(
        judge="TechLead",
        criterion="General",
        score=5.0 if is_sandboxed else 1.0,
        argument="[security] VERDICT: Ephemeral workspace verified." if is_sandboxed else
                 "[security] RULING: Security Negligence. Tooling lacks sandboxing. ACTION: Migrate to tempfile.TemporaryDirectory().",
        statute="Technical Standard 5.2"
    ))

    # --- RULING: Criterion #10 (Swarm Resilience) ---
    new_opinions.append(Opinion(
        judge="TechLead",
        criterion="General",
        score=4.5 if has_error_handling else 1.5,
        argument="[resilience] VERDICT: Robust try/except blocks detected in node logic." if has_error_handling else
                 "[resilience] RULING: Fragile Orchestration. Missing global error handlers in graph nodes.",
        statute="Technical Standard 6.0"
    ))

    print(f"⚖️ TechLead: Filed {len(new_opinions)} Executive Rulings.")
    return {"opinions": new_opinions}