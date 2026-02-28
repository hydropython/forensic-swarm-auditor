from __future__ import annotations
from typing import Annotated, List, Dict, Any, Union
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator

# --- Protocol A.1: Structured Schemas ---
class Evidence(BaseModel):
    """Forensic proof captured by Detectives."""
    found: bool
    criterion: str
    rationale: str
    metadata: Dict[str, Any] = {}

class Opinion(BaseModel):
    judge: str
    criterion: str  
    score: float
    argument: str   
    statute: str

# --- Protocol B.2: State Reducers ---
def merge_evidences(existing: Dict[str, List[Any]], new: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    """Deep merge for parallel detective results."""
    merged = (existing or {}).copy()
    for key, val in new.items():
        if key in merged:
            merged[key].extend(val)
        else:
            merged[key] = val
    return merged

class AgentState(TypedDict):
    """The central state of the Forensic Swarm."""
    repo_url: str
    workspace_path: str
    pdf_path: str
    # Reducers are mandatory for parallel Fan-Out
    evidences: Annotated[Dict[str, List[Any]], merge_evidences]
    opinions: Annotated[List[Dict[str, Any]], operator.add]
    aggregated_score: float
    global_verdict: str