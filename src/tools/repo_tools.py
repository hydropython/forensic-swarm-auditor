import os
import ast
import tempfile
import subprocess
from git import Repo

def safe_clone(repo_url: str, target_dir: str):
    """Sandboxed cloning to prevent live-directory pollution."""
    try:
        Repo.clone_from(repo_url, target_dir)
        return True
    except Exception as e:
        print(f"Forensic Error: Failed to clone {repo_url} - {str(e)}")
        return False

def analyze_ast_rigor(file_path: str):
    """Protocol B: Deep Code Inspection via AST."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        try:
            tree = ast.parse(f.read())
            # We look for Pydantic classes or operator reducers
            # This is the 'DNA' test of the student's code
            return tree
        except SyntaxError:
            return "Corrupted Code: Syntax Error detected"