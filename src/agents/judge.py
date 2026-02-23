from src.core.state import JudicialOpinion, AgentState

def advanced_weighted_judge(state: AgentState) -> AgentState:
    """⚖️ Real Judge Logic: Calculates a weighted average based on impact."""
    evidence = state.get("forensic_evidence", [])
    
    # 1. Define Weights
    weights = {
        "Security": 0.40,
        "Arch": 0.30,
        "Logic": 0.20,
        "Env": 0.10
    }
    
    # 2. Score each class (No-fail: 1.0 base)
    class_scores = {key: 1.0 for key in weights.keys()}
    
    # Map findings to the highest score per class
    for e in evidence:
        if e.status == "confirmed":
            # Map criterion string to class key (e.g., 'No hardcoded keys' -> 'Security')
            # For this demo, we'll assume the criterion prefix or a mapping
            score_val = 1
            if e.category == "Essential": score_val = 3
            if e.category == "Advanced": score_val = 5
            
            # Simple mapping logic for this example
            target_class = "Env"
            if "key" in e.criterion.lower(): target_class = "Security"
            elif "Modular" in e.criterion or "Swarm" in e.criterion: target_class = "Arch"
            elif "recovery" in e.criterion or "except" in e.criterion: target_class = "Logic"
            
            if score_val > class_scores[target_class]:
                class_scores[target_class] = score_val

    # 3. Calculate Weighted Final Grade
    # Formula: Final = Σ (Score_i * Weight_i)
    final_score = sum(class_scores[c] * weights[c] for c in weights)

    # 4. Judicial Argument (The 'Real Judge' part)
    pro_con_summary = " | ".join([f"{c}: {class_scores[c]}" for c in class_scores])
    
    opinion = JudicialOpinion(
        judge_persona="TechLead",
        tier="Advanced" if final_score >= 4.0 else "Essential" if final_score >= 2.5 else "Basic",
        score=round(final_score),
        argument=f"Final Weighted Grade: {final_score:.2f}. Breakdown: {pro_con_summary}",
        evidence_referenced=[e.criterion for e in evidence]
    )

    return {
        **state,
        "judicial_opinions": [opinion],
        "final_score": final_score,
        "current_status": f"⚖️ Weighted Verdict: {final_score:.2f}"
    }