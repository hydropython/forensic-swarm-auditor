# src/agents/judge.py
from src.core.state import JudicialOpinion, AgentState

def tech_lead_synthesis_node(state: AgentState) -> AgentState:
    """🛠️ Final Synthesis: Combines weighted math with judicial nuance."""
    evidence = state.get("forensic_evidence", [])
    opinions = state.get("judicial_opinions", [])
    
    # 1. Base Weighted Math (Your Core Logic)
    weights = {"Security": 0.40, "Arch": 0.30, "Logic": 0.20, "Env": 0.10}
    class_scores = {key: 1.0 for key in weights.keys()} # No-fail base
    
    for e in evidence:
        if e.status == "confirmed":
            val = 5 if e.category == "Advanced" else 3 if e.category == "Essential" else 1
            # Class Mapping
            target = "Env"
            if "key" in e.criterion.lower() or "secure" in e.criterion.lower(): target = "Security"
            elif "modular" in e.criterion.lower() or "src" in e.criterion.lower(): target = "Arch"
            
            if val > class_scores[target]: class_scores[target] = val

    raw_score = sum(class_scores[c] * weights[c] for c in weights)

    # 2. Judicial Adjustment (The "Real Judge" Part)
    # If Prosecutor is extremely harsh, we apply a 'Technical Debt' penalty
    prosecutor_score = next((o.score for o in opinions if o.judge_persona == "Prosecutor"), 3)
    defense_score = next((o.score for o in opinions if o.judge_persona == "Defense"), 3)
    
    # The Tech Lead acts as a mediator
    final_score = (raw_score + prosecutor_score + defense_score) / 3

    opinion = JudicialOpinion(
        judge_persona="TechLead",
        tier="Advanced" if final_score >= 4.0 else "Essential" if final_score >= 2.5 else "Basic",
        score=round(final_score),
        argument=f"Synthesis: Math yields {raw_score:.2f}, but Judicial debate adjusts verdict to {final_score:.2f}.",
        evidence_referenced=["Prosecutor Argument", "Defense Argument"]
    )

    return {
        **state,
        "judicial_opinions": [opinion],
        "final_score": final_score,
        "current_status": f"⚖️ Final Verdict: {final_score:.2f}"
    }