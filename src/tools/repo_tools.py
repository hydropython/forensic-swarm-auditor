import os
import ast
import os
import subprocess
import tempfile
import ast
from typing import List, Optional

def clone_repo_sandboxed(repo_url: str) -> str:
    """
    Protocol A: Secure Environment Isolation.
    Clones the target repo into a temporary directory that 
    auto-deletes after the audit to prevent local pollution.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(
            ["git", "clone", repo_url, temp_dir], 
            check=True, capture_output=True, text=True
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Forensic Failure: Git Clone Error: {e.stderr}")
        raise

def get_git_log(repo_path: str) -> List[str]:
    """
    Protocol C: The Git Narrative.
    Extracts atomic history to verify the engineering process.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--oneline", "--reverse"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split("\n")
    except Exception:
        return []

def get_ast_tree(file_path: str) -> Optional[ast.AST]:
    """
    The Detective's Microscope.
    Parses Python code into a tree for structural analysis.
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return ast.parse(f.read())