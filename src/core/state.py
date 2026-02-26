import operator
from typing import Annotated, Dict, List, Literal, Optional, Any
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
    confidence: float = Field(ge=0, le=1)

# --- Protocol A: Project Health (Git & Versioning) ---
class ProjectMetadata(BaseModel):
    """📊 High-level audit of the project's development history."""
    git_log: List[str] = Field(default_factory=list, description="Output of git log --oneline --reverse")
    has_uv_lock: bool = Field(default=False, description="Presence of uv.lock file")
    version: str = Field(default="0.0.0", description="Current version in pyproject.toml")
    progression_score: float = Field(default=0.0, description="Score based on Env -> Tool -> Graph evolution")

# --- Protocol B: Judicial Opinion (The Interpretation) ---
class JudicialOpinion(BaseModel):
    """⚖️ Interpretive judgment on a specific rubric criterion."""
    judge: Literal["Prosecutor", "Defense", "TechLead"]
    criterion_id: str
    score: int = Field(ge=1, le=5)
    argument: str
    cited_evidence: List[str]

# --- The Graph State: The Courtroom Record ---
class ForensicState(TypedDict):
    """🏛️ The global state governing the courtroom process."""
    repo_url: str
    pdf_path: str
    workspace_path: str  # Path to the cloned repo in the sandbox
    rubric_dimensions: List[Dict]
    
    # 🕵️ operator.ior merges dictionaries (Fan-In from Detectives)
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    
    # 🎯 Refined by the Aggregator
    refined_evidences: List[Evidence]
    
    # 📊 Audit data for git history
    metadata: ProjectMetadata
    
    # ⚖️ operator.add appends list items (Fan-In from Judges)
    opinions: Annotated[List[JudicialOpinion], operator.add]
    
    final_report: Optional[str]

# Alias for backward compatibility if needed
AgentState = ForensicState