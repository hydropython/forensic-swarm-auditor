import os
import ast
import subprocess
import tempfile
from typing import List, Optional, Dict, Any
from langchain_core.tools import tool

@tool
def clone_repo_sandboxed(repo_url: str) -> str:
    """
    Protocol A: Secure Environment Isolation.
    Clones the target repo into a temporary directory to prevent local pollution.
    Removes --depth 1 to capture the full 'Progression Story' for Protocol C.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        # MANDATORY: Full clone for Forensic History (Score 5)
        subprocess.run(
            ["git", "clone", repo_url, temp_dir], 
            check=True, capture_output=True, text=True
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        return f"Forensic Failure: Git Clone Error: {e.stderr}"

@tool
def analyze_code_structure(file_path: str) -> Dict[str, Any]:
    """
    The Detective's Microscope (Deep AST).
    Verifies State Management Rigor by hunting for Pydantic BaseModels 
    and mandatory operator reducers (add/ior) in Annotated types.
    """
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found."}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        findings = {
            "pydantic_models": [],
            "has_annotated": False,
            "reducers_found": [],
            "state_rigor_score": 1
        }
        
        for node in ast.walk(tree):
            # 1. Check for Pydantic BaseModel (Protocol B.2)
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'BaseModel':
                        findings["pydantic_models"].append(node.name)
            
            # 2. Deep Reducer Check (The 'Smoking Gun' for Score 5)
            if isinstance(node, ast.Name) and node.id == "Annotated":
                findings["has_annotated"] = True
            
            # Specifically hunt for operator.add or operator.ior in the code
            if isinstance(node, ast.Attribute):
                if node.attr in ["add", "ior"] and isinstance(node.value, ast.Name) and node.value.id == "operator":
                    findings["reducers_found"].append(f"operator.{node.attr}")

        # Deterministic Internal Scoring
        if findings["pydantic_models"] and findings["reducers_found"]:
            findings["state_rigor_score"] = 5
        elif findings["pydantic_models"]:
            findings["state_rigor_score"] = 3

        return findings
    except Exception as e:
        return {"error": f"AST Parsing failed: {str(e)}"}

@tool
def get_detailed_git_log(repo_path: str) -> List[Dict[str, str]]:
    """
    Protocol C: The Git Narrative Extraction.
    Captures Hash, ISO Timestamp, and Message to prove Engineering Velocity.
    """
    try:
        # We use %ai for ISO 8601 strict timestamping
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%h|%ai|%s", "--reverse"],
            capture_output=True, text=True, check=True
        )
        log_entries = []
        for line in result.stdout.strip().split("\n"):
            if "|" in line:
                h, ts, msg = line.split("|")
                log_entries.append({"hash": h, "timestamp": ts, "message": msg})
        return log_entries
    except Exception as e:
        return [{"error": f"Forensic History Unavailable: {str(e)}"}]