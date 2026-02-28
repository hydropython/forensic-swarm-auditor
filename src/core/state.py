from __future__ import annotations
from typing import Annotated, List, Dict, Any, Optional, Union
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator

# --- 1. Pydantic Forensic Schemas (Fixes ID-08: Structured Output Rigor) ---

class Evidence(BaseModel):
    """Represents a specific forensic finding from a Detective agent."""
    found: bool = False
    criterion: str
    rationale: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Opinion(BaseModel):
    """Represents a formal Judicial Opinion from a Judge agent."""
    judge: str
    score: float = Field(..., ge=1.0, le=5.0)
    statute: str = "Standard Forensic Protocol"
    commentary: str = "No detailed commentary provided."

# --- 2. The "Universal Bouncer" Reducers (Fixes ID-02: Fan-In/Fan-Out) ---

def merge_opinions(
    existing: List[Opinion], 
    new: List[Union[Opinion, Dict[str, Any]]]
) -> List[Opinion]:
    """Ensures parallel judges merge scores without overwriting each other."""
    opinion_map = {op.judge: op for op in (existing or [])}
    
    if new:
        for op_data in new:
            # Handle both raw dicts from LLMs and Pydantic objects
            if isinstance(op_data, dict):
                try:
                    op = Opinion(**op_data)
                except Exception: continue
            else:
                op = op_data
            opinion_map[op.judge] = op
                
    return list(opinion_map.values())

def merge_evidences(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic merger for Detective results."""
    merged = (existing or {}).copy()
    if new:
        merged.update(new)
    return merged

# --- 3. The Global State Definition ---

class AgentState(TypedDict):
    """
    The Official Judicial Record. 
    Annotated fields allow the graph to run in parallel (ID-03).
    """
    repo_url: str
    workspace_path: str
    pdf_path: str
    
    # Reducers prevent 'Last-Writer-Wins' bugs
    evidences: Annotated[Dict[str, Any], merge_evidences]
    opinions: Annotated[List[Opinion], merge_opinions]
    
    aggregated_score: float
    global_verdict: str
    judicial_overrides: List[str]
    metadata: Dict[str, Any]