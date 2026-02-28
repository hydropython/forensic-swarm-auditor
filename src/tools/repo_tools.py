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
    Returns the local path to the cloned repository.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(
            ["git", "clone", repo_url, temp_dir], 
            check=True, capture_output=True, text=True
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        return f"Forensic Failure: Git Clone Error: {e.stderr}"

@tool
def get_git_log(repo_path: str) -> List[str]:
    """
    Protocol C: The Git Narrative.
    Extracts commit history to verify if the engineering process followed 
    the required sequence of development.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--oneline", "--reverse"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split("\n")
    except Exception:
        return ["Error: Could not retrieve git log."]

@tool
def analyze_code_structure(file_path: str) -> Dict[str, Any]:
    """
    The Detective's Microscope.
    Uses AST to check for Pydantic models and LangGraph state reducers.
    """
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found."}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        findings = {
            "classes": [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
            "imports": [],
            "has_annotated": False
        }
        
        # Look for 'Annotated' which is the smoking gun for high-quality state management
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == "Annotated":
                findings["has_annotated"] = True
                
        return findings
    except Exception as e:
        return {"error": f"AST Parsing failed: {str(e)}"}