from typing import Dict
from src.core.state import AgentState, Evidence

def evidence_aggregator(state: AgentState) -> Dict:
    """
    🎯 The 'Clerk of Court' node: Deduplicates findings and prepares 
    the 'Final Fact Record' for the Judges.
    """
    # 1. Flatten all evidence from all parallel detectives
    all_raw_evidence = []
    for detective_name, evidence_list in state["evidences"].items():
        all_raw_evidence.extend(evidence_list)

    # 2. Conflict Resolution: Keep only the highest confidence evidence per goal
    # This prevents the DocAnalyst and RepoInvestigator from clashing
    best_findings: Dict[str, Evidence] = {}
    
    for ev in all_raw_evidence:
        # If we find a match, the one with higher confidence (0.0 to 1.0) wins
        if ev.goal not in best_findings or ev.confidence > best_findings[ev.goal].confidence:
            best_findings[ev.goal] = ev

    # 3. Protocol A.1 Check: Merge Git Metadata into rationale if needed
    # (Optional: You can add logic here to explicitly flag if 'progression_score' is low)

    return {"refined_evidences": list(best_findings.values())}