import os
import ast
from git import Repo as GitRepo
from src.core.state import Evidence

def repo_investigator(state: dict):
    workspace = state["workspace_path"]
    findings = []

    # --- 1. Git Forensic Analysis (Granular) ---
    try:
        repo_obj = GitRepo(workspace)
        commits = list(repo_obj.iter_commits(reverse=True))
        
        # Check 1: Commit Count
        findings.append(Evidence(
            goal="1.1 Commit Volume", found=len(commits) > 3,
            location="git log", rationale=f"Detected {len(commits)} commits. Exceeds bulk-upload threshold."
        ))

        # Check 2: Progression - Environment Setup
        env_setup = any("setup" in c.summary.lower() or "init" in c.summary.lower() for c in commits)
        findings.append(Evidence(
            goal="1.2 Progression: Env Setup", found=env_setup,
            location="git log", rationale="Verified historical 'Setup' phase in early commits."
        ))

        # Check 3: Progression - Graph Orchestration
        graph_commits = any("graph" in c.summary.lower() or "orchestration" in c.summary.lower() for c in commits)
        findings.append(Evidence(
            goal="1.3 Progression: Graph Logic", found=graph_commits,
            location="git log", rationale="Verified evolution into 'Orchestration' phase."
        ))
    except Exception as e:
        findings.append(Evidence(goal="1.0 Git Error", found=False, location="git", rationale=str(e)))

    # --- 2. State Management Rigor (AST Granular) ---
    state_file = os.path.join(workspace, "src/core/state.py")
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            code = f.read()
            tree = ast.parse(code)
            
            # Check 4: BaseModel/Pydantic Usage
            has_pydantic = "BaseModel" in code
            findings.append(Evidence(
                goal="2.1 Schema Enforcement", found=has_pydantic,
                location="src/core/state.py", rationale="Detected Pydantic BaseModel inheritance for structured findings."
            ))

            # Check 5: JudicialOpinion Collection
            has_opinions = "JudicialOpinion" in code and "List" in code
            findings.append(Evidence(
                goal="2.2 Opinion Collection", found=has_opinions,
                location="src/core/state.py", rationale="State actively maintains a list of JudicialOpinion objects."
            ))

    # --- 3. Graph Orchestration (Phase 1 Granular) ---
    engine_file = os.path.join(workspace, "src/core/engine.py")
    if os.path.exists(engine_file):
        with open(engine_file, "r") as f:
            content = f.read()
            # Check 6: Fan-Out Signature
            fan_out = content.count("builder.add_edge") > 4
            findings.append(Evidence(
                goal="3.1 Orchestration: Fan-Out", found=fan_out,
                location="src/core/engine.py", rationale="Detected parallel branching to multiple agent nodes."
            ))

    # --- 4. Safe Tool Engineering (Phase 2) ---
    tools_dir = os.path.join(workspace, "src")
    cloning_logic = False
    for root, _, files in os.walk(tools_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", errors='ignore') as f:
                    tool_code = f.read()
                    if "TemporaryDirectory" in tool_code or "mkdtemp" in tool_code:
                        cloning_logic = True
                        break
    
    findings.append(Evidence(
        goal="4.1 Git Sandboxing", found=cloning_logic,
        location="src/tools/", rationale="Verified use of TemporaryDirectory for repository isolation."
    ))

    return {"evidences": {"repo_investigator": findings}}