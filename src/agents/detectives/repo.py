import ast
from pathlib import Path
from src.core.state import Evidence

class ASTInvestigator:
    """
    Interrogates Python source code to find structural proof of 
    LangGraph implementations and Pydantic models.
    """
    
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path

    def verify_langgraph_usage(self) -> Evidence:
        """Checks for StateGraph instantiation in the source code."""
        found_graph = False
        rationale = "No StateGraph instantiation found in .py files."
        
        for py_file in self.workspace_path.rglob("*.py"):
            tree = ast.parse(py_file.read_text(errors='ignore'))
            for node in ast.walk(tree):
                # Look for 'StateGraph(' call
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == "StateGraph":
                        found_graph = True
                        rationale = f"Found StateGraph instantiation in {py_file.name}"
                        break
        
        return Evidence(
            goal="Verify StateGraph Implementation",
            found=found_graph,
            location=str(self.workspace_path),
            rationale=rationale,
            confidence=1.0 if found_graph else 0.5
        )

# --- COMMIT: Implemented AST Structural Interrogation Logic ---