from src.core.state import ForensicState, Evidence, ProjectMetadata

def evidence_aggregator(state: ForensicState):
    print("🎯 Aggregator: Synchronizing findings...")
    
    all_findings = []
    
    # 1. Pull the merged dictionary from state
    raw_evidences = state.get("evidences", {})
    
    # 2. Flatten findings from ALL detectives (Repo, Doc, etc.)
    for findings_list in raw_evidences.values():
        if isinstance(findings_list, list):
            all_findings.extend(findings_list)
    
    # 3. Ensure Metadata is a Pydantic Model (Satisfies 'Rigor' criterion)
    current_metadata = state.get("metadata")
    if not isinstance(current_metadata, ProjectMetadata):
        current_metadata = ProjectMetadata(**current_metadata) if current_metadata else ProjectMetadata()
    
    # 4. Sort: Validated findings (found=True) move to the top
    all_findings.sort(key=lambda x: x.found, reverse=True)

    return {
        "refined_evidences": all_findings,
        "metadata": current_metadata
    }

def check_evidence_quality(state: ForensicState) -> str:
    # Look at the list the aggregator just built
    refined = state.get("refined_evidences", [])
    
    # ✅ PASS CRITERIA: At least one actual artifact must be found
    # to stop the loop and go to the judges.
    actual_finds = [e for e in refined if e.found]
    
    if len(actual_finds) > 0:
        print(f"✅ Evidence sufficient. Moving to Judges...")
        return "sufficient"
    
    print("⚠️ Evidence incomplete (All ❌). Retrying detectives...")
    return "incomplete"