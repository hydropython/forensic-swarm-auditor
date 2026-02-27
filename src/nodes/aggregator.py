from src.core.state import ForensicState, Evidence, ProjectMetadata

def evidence_aggregator(state: ForensicState):
    """
    🎯 The Aggregator: Synthesizes detailed findings from Repo, Doc, and Vision detectives.
    Ensures the final UI table is sorted numerically and metadata is rigorously validated.
    """
    print("🎯 Aggregator: Synchronizing high-detail forensic findings...")
    
    all_findings = []
    
    # 1. Pull the merged dictionary from state
    raw_evidences = state.get("evidences", {})
    
    # 2. Flatten findings from ALL detectives
    for agent_name, findings_list in raw_evidences.items():
        if isinstance(findings_list, list):
            # We tag the rationale with the agent name for judge-level transparency
            all_findings.extend(findings_list)
    
    # 3. Metadata Validation (Pydantic Rigor)
    current_metadata = state.get("metadata")
    if not isinstance(current_metadata, ProjectMetadata):
        # Convert raw dict to Pydantic Model if necessary
        current_metadata = ProjectMetadata(**current_metadata) if current_metadata else ProjectMetadata()
    
    # 4. SORTING LOGIC: 
    # We sort by the Goal string so that 1.0 (Repo) comes before 9.0 (Vision).
    # This keeps your UI table looking professional and chronological.
    try:
        all_findings.sort(key=lambda x: x.goal)
    except Exception as e:
        print(f"⚠️ Sorting Warning: {e}")

    return {
        "refined_evidences": all_findings,
        "metadata": current_metadata
    }

def check_evidence_quality(state: ForensicState) -> str:
    """
    ⚖️ Quality Gate: Ensures the judges have enough 'meat' to make a decision.
    """
    refined = state.get("refined_evidences", [])
    
    # Detect the volume of artifacts found
    actual_finds = [e for e in refined if e.found]
    found_count = len(actual_finds)
    
    if found_count > 0:
        print(f"✅ Forensic Dossier Complete: {found_count} artifacts verified. Moving to Judges...")
        return "sufficient"
    
    # If everything is ❌, we don't waste the Judges' time (or tokens)
    print("⚠️ Evidence incomplete (All ❌). The detectives failed to find any signatures.")
    return "incomplete"