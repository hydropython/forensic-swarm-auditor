import os
import json
from src.core.state import AgentState

def context_builder_node(state: AgentState):
    """
    The Constitutional Layer: Loads the rubric and maps it to the workspace.
    """
    # 1. THE EFFORT: Get absolute path to the config file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    rubric_path = os.path.join(base_dir, "src", "config", "rubric.json")
    
    # 2. THE RESULT: Load the law or fail gracefully
    if not os.path.exists(rubric_path):
        raise FileNotFoundError(f"⚖️ CONSTITUTION MISSING: Please create {rubric_path}")

    with open(rubric_path, "r") as f:
        rubric_data = json.load(f)

    print("📜 CONTEXT: Rubric loaded. Law of Fact Supremacy active.")
    
    return {
        "log": "Rubric successfully bound to state.",
        "metadata": {"rubric_version": rubric_data.get("version")}
    }