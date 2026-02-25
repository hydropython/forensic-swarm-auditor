import ast
import subprocess
import tomllib  # Built-in for parsing pyproject.toml
from pathlib import Path
from src.core.state import AgentState, Evidence, ProjectMetadata

def repo_investigator_node(state: AgentState):
    """🎯 Protocol A.1: Finalized Git & Versioning Forensic Node"""
    path = Path(state["workspace_path"]) 
    
    # 1. Git Forensic Check
    git_cmd = subprocess.run(
        ["git", "-C", str(path), "log", "--oneline", "--reverse"], 
        capture_output=True, text=True
    )
    commits = git_cmd.stdout.strip().split("\n") if git_cmd.returncode == 0 else []
    
    # 2. Version & Environment Audit
    version = "0.0.0"
    pyproject_path = path / "pyproject.toml"
    if pyproject_path.exists():
        try:
            data = tomllib.loads(pyproject_path.read_text())
            version = data.get("project", {}).get("version", "0.0.0")
        except: pass

    # 3. Progression Scoring (Evolution Logic)
    # Check if they actually evolved the code across commits
    history = git_cmd.stdout.lower()
    prog_score = 0.0
    if "env" in history: prog_score += 0.3
    if "agent" in history or "node" in history: prog_score += 0.4
    if "graph" in history or "workflow" in history: prog_score += 0.3

    # 4. AST Check (Your logic)
    inv = ASTInvestigator(path)
    graph_evidence = inv.verify_langgraph_usage()

    return {
        "metadata": ProjectMetadata(
            git_log=commits, 
            has_uv_lock=(path / "uv.lock").exists(),
            version=version,
            progression_score=prog_score
        ),
        "evidences": {"repo_detective": [graph_evidence]}
    }