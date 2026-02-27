import operator
from typing import Annotated, Dict, List, Literal, Optional, Any, Union
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# --- Protocol A: Forensic Evidence (The Fact Record) ---
class Evidence(BaseModel):
    """🔍 Individual finding from a detective (Repo, Doc, or Vision)."""
    goal: str = Field(description="The specific forensic instruction from the rubric")
    found: bool = Field(description="Objective existence of the artifact")
    content: Optional[str] = Field(default=None, description="The raw code snippet or log entry")
    location: str = Field(description="File path, line number, or commit hash")
    rationale: str = Field(description="Technical explanation for the finding")
    # Default 1.0 to satisfy Pydantic when confidence isn't manually calculated
    confidence: float = Field(default=1.0, ge=0, le=1)

# --- Protocol B: Project Health (Git & Versioning) ---
class ProjectMetadata(BaseModel):
    """📊 High-level audit of the project's development history."""
    git_log: List[str] = Field(default_factory=list, description="Output of git log --oneline")
    has_uv_lock: bool = Field(default=False, description="Presence of uv.lock file")
    version: str = Field(default="0.1.0", description="Current version in pyproject.toml")
    progression_score: float = Field(default=0.0, description="Score based on Env -> Tool -> Graph evolution")

# --- Protocol C: Judicial Opinion (The Interpretation) ---
class JudicialOpinion(BaseModel):
    """⚖️ Interpretive judgment on a specific rubric criterion."""
    judge: Literal["Prosecutor", "Defense", "TechLead"]
    criterion_id: str
    score: int = Field(ge=1, le=5)
    argument: str
    cited_evidence: List[str] = Field(default_factory=list)

# --- The Graph State: The Courtroom Record ---
class ForensicState(TypedDict):
    """🏛️ The global state governing the courtroom process."""
    # Inputs
    repo_url: Optional[str]
    pdf_path: Optional[str]
    workspace_path: str 
    rubric_dimensions: List[Dict[str, Any]]
    
    # 🕵️ DETECTIVE REDUCER: Merges dictionaries from parallel detectives.
    # If Repo finds A and Doc finds B, operator.ior (Inclusive OR) merges them.
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    
    # 🎯 AGGREGATOR OUTPUT: Flattened and sorted list for the UI/Judges
    refined_evidences: List[Evidence]
    
    # 📊 METADATA: Project-wide context
    metadata: ProjectMetadata
    
    # ⚖️ JUDGE REDUCER: Appends opinions as they arrive from parallel judges.
    opinions: Annotated[List[JudicialOpinion], operator.add]
    
    # Final generated Markdown/PDF report
    final_report: Optional[str]
    verdict: Optional[str]

# Alias for backward compatibility across the repo
AgentState = ForensicState