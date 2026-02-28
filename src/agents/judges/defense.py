from typing import Dict, Any, List
from src.core.state import AgentState, Opinion

def defense_node(state: AgentState) -> Dict[str, Any]:
    """
    The Defense: Maps specific technical effort to rubric items.
    Focuses on 'Engineering Grit' and 'Structural Intent'.
    """
    evidences = state.get("evidences", {})
    repo_findings = evidences.get("repo_agent", [])
    
    # --- FORENSIC SCANNING LOGIC ---
    # 1. State Rigor Check
    has_ast = any("ast" in str(f).lower() or "parsing" in str(f).lower() for f in repo_findings)
    
    # 2. Git Chronology Check (Focusing on the 51-commit win)
    git_finding = next((f for f in repo_findings if f.get("criterion") == "git"), {})
    commit_count = git_finding.get("metadata", {}).get("total_commits", 0)
    
    new_opinions = []

    # --- ARGUMENT 1: STATE MANAGEMENT ---
    new_opinions.append(Opinion(
        judge="Defense",
        criterion="State Rigor",
        score=4.8 if has_ast else 3.8,
        argument="[state] The defense highlights the use of AST-based state tracking as proof of sovereign intent. This exceeds basic dict-based state management." if has_ast 
                 else "[state] The defendant demonstrated clear structural intent. Foundational engineering is sound and baseline state is stable.",
        statute="Protocol B-2: Statute of Effort"
    ))

    # --- ARGUMENT 2: GRAPH ARCHITECTURE ---
    new_opinions.append(Opinion(
        judge="Defense",
        criterion="Graph Orchestration",
        score=4.5,
        argument="[graph] Multi-agent collaboration confirmed via LangGraph node separation. The architecture shows a clear commitment to non-linear swarm logic.",
        statute="Protocol B-2: Statute of Effort"
    ))

    # --- ARGUMENT 3: GIT CHRONOLOGY (The "Grit" Factor) ---
    if commit_count > 40:
        git_arg = f"[git] MITIGATION: {commit_count} commits demonstrate an elite level of iterative development. This is not a bulk-upload; it is a master-class in engineering chronology."
        git_score = 5.0
    else:
        git_arg = f"[git] The commit history shows consistent progress. Even with lower frequency, the technical delta between commits is high."
        git_score = 4.0

    new_opinions.append(Opinion(
        judge="Defense",
        criterion="Git Forensic",
        score=git_score,
        argument=git_arg,
        statute="Statute of Engineering Grit"
    ))

    # --- ARGUMENT 4: MITIGATION FOR DOCS ---
    new_opinions.append(Opinion(
        judge="Defense",
        criterion="Documentation",
        score=3.0,
        argument="[docs] While the PDF artifact is pending, the code itself is 'Self-Documenting'. The clarity of the graph nodes serves as a living blueprint.",
        statute="Statute of Practicality"
    ))

    print(f"🛡️ Defense: Filed {len(new_opinions)} mitigating arguments.")
    return {"opinions": new_opinions}