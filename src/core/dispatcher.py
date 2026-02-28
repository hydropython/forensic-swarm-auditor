from typing import Dict, Any
from src.core.state import AgentState

def dispatcher_node(state: AgentState) -> Dict[str, Any]:
    """
    The Traffic Controller: Coordinates the parallel Fan-Out.
    Ensures that forensic criteria are routed to the correct detectives.
    """
    # 1. THE EFFORT: Log the start of the parallel forensic sweep
    workspace = state.get("workspace_path", "Unknown")
    
    print(f"📡 DISPATCHER: Initiating parallel scan on {workspace}")
    
    # 2. THE RESULT: We return a status that the graph edges use to trigger 
    # repo_detective, docs_detective, and vision_detective simultaneously.
    return {
        "global_verdict": "DISPATCHING",
        "log": "Dispatcher active: Routing to Repo and Doc agents."
    }