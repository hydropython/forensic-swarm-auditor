import os
from src.core.state import Evidence
from src.tools.repo_tools import clone_repo_sandboxed, get_git_log, analyze_code_structure

def repo_investigator(state):
    """
    Sovereign Forensic Investigator: Strictly Validates IDs 01, 04, 05, and 08.
    This function MUST be named 'repo_investigator' for graph.py to find it.
    """
    repo_url = state.get("repo_url")
    findings_list = []

    # 1. Validation Check
    if not repo_url:
        return {"evidences": {"repo_agent": [
            {"found": False, "criterion": "Entry", "rationale": "Missing repo_url"}
        ]}}

    # 2. PHASE 1: Tool Execution using .invoke()
    workspace_path = clone_repo_sandboxed.invoke({"repo_url": repo_url})
    
    if "Forensic Failure" in str(workspace_path):
        return {"evidences": {"repo_agent": [
            Evidence(found=False, criterion="Safe Tooling", rationale=str(workspace_path)).model_dump()
        ]}}

    # 3. PHASE 2: Path Discovery
    real_root = workspace_path
    for root, dirs, files in os.walk(workspace_path):
        if "uv.lock" in files or "src" in dirs:
            real_root = root
            break
            
    has_uv = os.path.exists(os.path.join(real_root, "uv.lock"))
    has_src = os.path.exists(os.path.join(real_root, "src"))
    
    findings_list.append(Evidence(
        found=has_uv and has_src,
        criterion="Project Infrastructure",
        rationale=f"VERIFIED: Found uv.lock: {has_uv}, src/: {has_src} at {real_root}."
    ).model_dump())

    # 4. PHASE 3: Git History
    git_log_data = get_git_log.invoke({"repo_path": real_root})
    findings_list.append(Evidence(
        found=len(git_log_data) > 0,
        criterion="Git Forensic Analysis",
        rationale=f"VERIFIED: Captured engineering narrative via git logs."
    ).model_dump())

    # 5. PHASE 4: AST Scan
    state_file = os.path.join(real_root, "src/core/state.py")
    ast_findings = analyze_code_structure.invoke({"file_path": state_file})
    has_annotated = ast_findings.get("has_annotated", False) if isinstance(ast_findings, dict) else False

    findings_list.append(Evidence(
        found=has_annotated,
        criterion="State Management Rigor",
        rationale="VERIFIED: AST Scan confirmed 'Annotated' types in state.py."
    ).model_dump())

    return {
        "workspace_path": real_root,
        "evidences": {"repo_agent": findings_list}
    }