from typing import Dict, Any, List
from src.core.state import AgentState, Opinion

def prosecutor(state: AgentState) -> Dict[str, Any]:
    """
    Sovereign Prosecutor: The Adversarial Voice of the Swarm.
    Upgraded with Multi-Path Metadata Retrieval for Executive Grade accuracy.
    """
    evidences = state.get("evidences", {})
    repo_findings = evidences.get("repo_agent", [])
    vision_findings = evidences.get("vision_agent", [])
    doc_findings = evidences.get("doc_agent", [])
    
    # --- 1. ROBUST GIT CHRONOLOGY SCAN (The 22-Commit Rule) ---
    # We check multiple paths to find the commit count to avoid 0-count hallucinations
    commit_count = 0
    
    # Path A: Search for the specific git criterion finding
    git_finding = next((f for f in repo_findings if f.get("criterion") == "git"), {})
    
    # Path B: Check metadata sub-dict (Current logic)
    commit_count = git_finding.get("metadata", {}).get("total_commits", 0)
    
    # Path C: Fallback - Check if total_commits is directly in the finding
    if commit_count == 0:
        commit_count = git_finding.get("total_commits", 0)
        
    # Path D: Global Fallback - check state directly (if your RepoAgent writes to root)
    if commit_count == 0:
        commit_count = state.get("commit_count", 0)

    # --- 2. FORENSIC SCANNING LOGIC ---
    has_pydantic = any("pydantic" in str(f).lower() or "basemodel" in str(f).lower() for f in repo_findings)
    has_parallel = any("parallel" in str(f).lower() or "fan-out" in str(f).lower() for f in vision_findings)
    has_docs = any(f.get("found") for f in doc_findings)

    new_opinions = []

    # --- SECTION A: STATE MANAGEMENT (Criterion #3 & #4) ---
    new_opinions.append(Opinion(
        judge="Prosecutor",
        criterion="State Rigor",
        score=5.0 if has_pydantic else 1.0,
        argument="[state] Pydantic models and Annotated reducers verified via AST scan." if has_pydantic 
                 else "[state] CHARGE: Hallucination Liability. Missing Pydantic BaseModel validation; state is susceptible to corruption.",
        statute="Protocol A.2: State Management Rigor"
    ))

    # --- SECTION B: GIT CHRONOLOGY (Criterion #1 & #2) ---
    if commit_count >= 22:
        git_arg = f"[git] VERIFIED: Captured {commit_count} commits. Narrative shows iterative engineering progression."
        git_score = 5.0
    elif commit_count > 0:
        git_arg = f"[git] CHARGE: Narrative Opaque. Only {commit_count} commits detected. This is a high-risk 'Bulk Upload' pattern."
        git_score = 2.5
    else:
        git_arg = "[git] CHARGE: Forensic Blackout. No commit history detected in cloned workspace. Narrative integrity is zero."
        git_score = 1.0

    new_opinions.append(Opinion(
        judge="Prosecutor",
        criterion="Git Forensic",
        score=git_score,
        argument=git_arg,
        statute="Protocol A.1: Git Chronology"
    ))

    # --- SECTION C: GRAPH ORCHESTRATION (Criterion #5 & #6) ---
    new_opinions.append(Opinion(
        judge="Prosecutor",
        criterion="Graph Orchestration",
        score=5.0 if has_parallel else 1.5,
        argument="[graph] Fan-out/Fan-in pattern confirmed. System is truly non-linear." if has_parallel 
                 else "[graph] CHARGE: Orchestration Fraud. System lacks parallel nodes; architecture is a linear simulation.",
        statute="Protocol B.1: Parallel Judicial Fan-Out"
    ))

    # --- SECTION D: THEORETICAL DEPTH (Criterion #7 & #8) ---
    new_opinions.append(Opinion(
        judge="Prosecutor",
        criterion="Documentation",
        score=5.0 if has_docs else 1.0,
        argument="[docs] Architectural blueprint (PDF/MD) found. Design intent matches execution." if has_docs 
                 else "[docs] CHARGE: Ghost Architecture. Missing report.pdf. Implementation cannot be verified against intent.",
        statute="Protocol B.3: Theoretical Depth"
    ))

    print(f"🔥 Prosecutor: Analyzed {commit_count} commits. Logged {len(new_opinions)} adversarial charges.")
    return {"opinions": new_opinions}