import operator
from typing import Annotated, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# --- Forensic Evidence: The Fact Record ---
class Evidence(BaseModel):
    goal: str = Field(description="The specific forensic instruction from the rubric")
    found: bool = Field(description="Objective existence of the artifact")
    content: Optional[str] = Field(default=None, description="The raw code snippet or log entry")
    location: str = Field(description="File path, line number, or commit hash")
    rationale: str = Field(description="Technical explanation for the finding")
    confidence: float = Field(ge=0, le=1)

# --- Judicial Opinion: The Interpretation ---
class JudicialOpinion(BaseModel):
    judge: Literal["Prosecutor", "Defense", "TechLead"]
    criterion_id: str
    score: int = Field(ge=1, le=5)
    argument: str
    cited_evidence: List[str]

# --- The Graph State: The Courtroom Record ---
class AgentState(TypedDict):
    repo_url: str
    pdf_path: str
    rubric_dimensions: List[Dict]
    # operator.ior merges the detective findings maps
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    # operator.add ensures opinions are appended, never overwritten
    opinions: Annotated[List[JudicialOpinion], operator.add]
    final_report: Optional[str] = None