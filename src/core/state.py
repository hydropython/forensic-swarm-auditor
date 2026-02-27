import operator
from typing import Annotated, Dict, List, Literal, Optional, Any, Union
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

def merge_evidences(existing: Dict[str, List[Any]], new: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    """Custom reducer: Combines findings from parallel detectives without collision."""
    combined = existing.copy() if existing else {}
    for key, value in new.items():
        if key in combined:
            combined[key].extend(value)
        else:
            combined[key] = value
    return combined

class Evidence(BaseModel):
    goal: str
    found: bool
    content: Optional[str] = None
    location: str
    rationale: str
    confidence: float = Field(default=1.0, ge=0, le=1)

class ProjectMetadata(BaseModel):
    git_log: List[str] = Field(default_factory=list)
    has_uv_lock: bool = Field(default=False)
    version: str = Field(default="0.1.0")
    progression_score: float = Field(default=0.0)
    model: str = Field(default="unknown")
    rubric: str = Field(default="forensic")

class JudicialOpinion(BaseModel):
    judge: Literal["Prosecutor", "Defense", "TechLead"]
    score: float = Field(ge=0, le=5)
    argument: str
    cited_evidence: List[str] = Field(default_factory=list)

class ForensicState(TypedDict):
    repo_url: Optional[str]
    pdf_path: Optional[str]
    workspace_path: str 
    rubric_dimensions: List[Dict[str, Any]]
    # Annotated tells LangGraph to use our merge function instead of 'Last Value Wins'
    evidences: Annotated[Dict[str, List[Evidence]], merge_evidences]
    refined_evidences: List[Evidence]
    metadata: ProjectMetadata
    opinions: Annotated[List[JudicialOpinion], operator.add]
    final_report: Optional[str]
    verdict: Optional[str]

AgentState = ForensicState