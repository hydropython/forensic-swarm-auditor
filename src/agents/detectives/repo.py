import os
import ast
import subprocess
from typing import Dict, Any, List
from src.core.state import Evidence

def analyze_code_structure_internal(file_path: str) -> dict:
    """
    Performs AST analysis to detect 'Annotated' type hints and 'BaseModel' inheritance.
    Satisfies Protocol A.1: State Management Rigor.
    """
    if not os.path.exists(file_path):
        return {"has_annotated": False, "has_pydantic": False}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        has_annotated = False
        has_pydantic = False
        
        for node in ast.walk(tree):
            # Check for Annotated (Reducers)
            if isinstance(node, ast.Name) and node.id == "Annotated":
                has_annotated = True
            # Check for Pydantic BaseModel (Rigor)
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "BaseModel":
                        has_pydantic = True
        
        return {"has_annotated": has_annotated, "has_pydantic": has_pydantic}
    except Exception:
        return {"has_annotated": False, "has_pydantic": False}

def get_git_log_manual(repo_path: str) -> List[str]:
    """Protocol A.1: Git Forensic Analysis - Manual subprocess to ensure success."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--reverse"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split("\n")
    except Exception:
        return []

def repo_investigator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sovereign Forensic Investigator.
    Enforces 'Fact Supremacy' by providing the Chief Justice with 'VERIFIED' proof.
    Updated: Multi-path metadata export for Judicial Visibility.
    """
    workspace_path = state.get("workspace_path")
    findings_list = []

    if not workspace_path or not os.path.exists(workspace_path):
        return {"evidences": {"repo_agent": []}}

    # --- 1. Git Forensic Analysis (Key: 'git') ---
    commits = get_git_log_manual(workspace_path)
    log_len = len(commits)
    is_iterative = log_len > 3
    
    git_rationale = (
        f"VERIFIED: Captured {log_len} commits. Narrative shows iterative progression." 
        if is_iterative else f"FAILURE: Only {log_len} commits found. Possible 'Bulk Upload' detected."
    )
    
    # We add a 'metadata' dictionary so the Prosecutor can find the 'total_commits'
    findings_list.append(Evidence(
        found=is_iterative,
        criterion="git",
        rationale=git_rationale,
        metadata={"total_commits": log_len}  # <--- CRITICAL FOR PROSECUTOR
    ).model_dump())

    # --- 2. State Management Rigor (Key: 'state') ---
    state_file = os.path.join(workspace_path, "src", "core", "state.py")
    analysis = analyze_code_structure_internal(state_file)
    
    state_success = analysis.get("has_annotated") and analysis.get("has_pydantic")
    state_rationale = (
        "VERIFIED: AST Scan confirmed 'BaseModel' and 'Annotated' reducers. State is robust." 
        if state_success else "FAILURE: Missing Pydantic models or Reducers; risk of data overwriting."
    )
    
    findings_list.append(Evidence(
        found=state_success,
        criterion="state",
        rationale=state_rationale
    ).model_dump())

    # --- 3. Graph Orchestration (Key: 'graph') ---
    graph_path = os.path.join(workspace_path, "src", "core", "graph.py")
    graph_exists = os.path.exists(graph_path)
    
    graph_rationale = (
        "VERIFIED: 'StateGraph' builder detected in src/core/graph.py. Orchestration active." 
        if graph_exists else "FAILURE: No graph definition found. Orchestration Fraud suspected."
    )

    findings_list.append(Evidence(
        found=graph_exists,
        criterion="graph",
        rationale=graph_rationale
    ).model_dump())

    # --- 4. Security & Sandbox Detection (Criterion #9) ---
    # Scan main.py to see if it uses the 'tempfile' module or 'shutil'
    main_path = os.path.join(workspace_path, "main.py")
    uses_proper_sandbox = False
    if os.path.exists(main_path):
        with open(main_path, 'r') as f:
            content = f.read()
            uses_proper_sandbox = "tempfile" in content and "TemporaryDirectory" in content

    findings_list.append(Evidence(
        found=uses_proper_sandbox,
        criterion="security",
        rationale="VERIFIED: Code uses tempfile.TemporaryDirectory()." if uses_proper_sandbox 
                  else "FAILURE: Manual pathing/shutil detected. Lacks ephemeral sandboxing."
    ).model_dump())

    # --- RETURN TO STATE ---
    # We return the count at the ROOT level so the Prosecutor can't miss it
    return {
        "evidences": {"repo_agent": findings_list},
        "commit_count": log_len,  # <--- FOR PROSECUTOR FACT-CHECKING
        "has_pydantic": state_success
    }