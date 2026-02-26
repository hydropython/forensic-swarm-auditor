from typing import List
# Ensure these match your src/core/state.py exactly
from src.core.state import ForensicState, Evidence, ProjectMetadata

def check_evidence_quality(state: ForensicState) -> str:
    """
    🔀 THE ROUTER: This tells the graph where to go next.
    Matches the keys in your engine's conditional_edges mapping.
    """
    # Look at the refined_evidences list we just created in the aggregator node
    evidences = state.get("refined_evidences", [])
    
    # Logic: If we found any evidence at all, move to Judicial Phase
    if len(evidences) > 0:
        print(f"✅ Evidence sufficient ({len(evidences)} items). Moving to Judicial Phase...")
        return "sufficient"
    
    # If the detectives came up empty, loop back to the Repo Investigator
    print("⚠️ Evidence incomplete. Re-routing to Detectives for deeper scan...")
    return "incomplete"

def evidence_aggregator(state: ForensicState):
    """
    🎯 THE NODE: Aggregates raw findings into a refined list.
    Ensures Pydantic models are preserved to avoid 'AttributeError'.
    """
    print("🎯 Aggregator: Processing detective findings...")
    
    all_findings = []
    
    # 'evidences' is a Dict[str, List[Evidence]] thanks to operator.ior in state.py
    raw_evidences = state.get("evidences", {})
    
    # Flatten all dictionary values into a single list of Evidence objects
    for source_key, findings_list in raw_evidences.items():
        if isinstance(findings_list, list):
            all_findings.extend(findings_list)
        else:
            # Handle cases where a detective might have sent a single Evidence object
            all_findings.append(findings_list)
    
    # 🛡️ FIX: Ensure metadata remains a Pydantic object
    current_metadata = state.get("metadata")
    
    # If metadata is missing or was passed as a dict, convert it back to the Model
    if current_metadata is None:
        current_metadata = ProjectMetadata()
    elif isinstance(current_metadata, dict):
        current_metadata = ProjectMetadata(**current_metadata)
    
    # Return the updated state keys
    return {
        "refined_evidences": all_findings,
        "metadata": current_metadata
    }