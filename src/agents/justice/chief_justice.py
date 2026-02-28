from typing import Dict, Any
from src.core.state import AgentState

def chief_justice_node(state: AgentState) -> Dict[str, Any]:
    """
    Sovereign Chief Justice: The Final Arbiter of Fact Supremacy.
    Optimized for High-Visibility Terminal Logging.
    """
    opinions = state.get("opinions", [])
    
    if not opinions:
        print("🚨 [CRITICAL] Chief Justice: No judicial opinions found in state. Abortion protocol active.")
        return {"aggregated_score": 0.0, "global_verdict": "VOID: No Opinions Filed"}

    # Calculate average score from all judges
    scores = [getattr(op, 'score', 0.0) for op in opinions]
    score = sum(scores) / len(scores)

    # Determine Verdict with default safety
    verdict = "INCONCLUSIVE" 
    if score >= 4.5:
        verdict = "ELITE: Sovereign Grade"
    elif score >= 3.5:
        verdict = "APPROVED: Engineering Grade"
    elif score >= 2.0:
        verdict = "PROBATION: Narrative Gaps Detected"
    else:
        verdict = "REJECTED: Forensic Failure"

    # --- VIDEO-READY LOGGING BLOCK ---
    # This creates a visual "Box" in your PowerShell to mark the end of the process
    print("\n" + "═"*60)
    print(f"🏛️  SOVEREIGN JUDICIAL VERDICT")
    print(f"   Final Forensic Score: {score:.2f} / 5.00")
    print(f"   Adjudication:         {verdict}")
    print(f"   Timestamp:            {state.get('timestamp', 'LIVE')}")
    print("═"*60 + "\n")
    
    return {
        "aggregated_score": score, 
        "global_verdict": verdict
    }