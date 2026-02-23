import os
from src.core.state import Evidence, AgentState

def environment_detective(state: AgentState) -> AgentState:
    """🕵️‍♂️ Specialized node to check the 'Env' class of the matrix."""
    repo_path = "data/input/temp_repo"
    new_evidence = []

    # 1. Check: .gitignore exists (Basic/Essential/Advanced)
    if os.path.exists(os.path.join(repo_path, ".gitignore")):
        new_evidence.append(Evidence(
            category="Basic",
            criterion=".gitignore exists",
            finding="Found .gitignore in root. Project has basic version control hygiene.",
            status="confirmed",
            source_citation=".gitignore",
            confidence=1.0
        ))

    # 2. Check: .env is hidden (Essential/Advanced)
    # We check if .env is inside the .gitignore file
    env_ignored = False
    gitignore_path = os.path.join(repo_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            if ".env" in f.read():
                env_ignored = True
    
    if env_ignored:
        new_evidence.append(Evidence(
            category="Essential",
            criterion=".env is hidden",
            finding=".env is correctly ignored. Security risk is mitigated.",
            status="confirmed",
            source_citation=".gitignore",
            confidence=1.0
        ))

    # 3. Check: UV is used (Advanced)
    if os.path.exists(os.path.join(repo_path, "uv.lock")):
        new_evidence.append(Evidence(
            category="Advanced",
            criterion="UV is used",
            finding="Found uv.lock. Project uses ultra-fast UV package manager.",
            status="confirmed",
            source_citation="uv.lock",
            confidence=1.0
        ))

    # We return the NEW findings. LangGraph's operator.add will merge them automatically.
    return {**state, "forensic_evidence": new_evidence, "current_status": "Environment Audit Complete"}