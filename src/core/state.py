from typing import Annotated, List, Literal, TypedDict
from pydantic import BaseModel, Field
import operator

# --- 1. EVIDENCE MODEL ---
# Detectives must use this to report facts.
class Evidence(BaseModel):
    category: Literal["Basic", "Essential", "Advanced"]
    criterion: str
    finding: str
    status: Literal["confirmed", "missing", "hallucinated"]
    source_citation: str  # e.g., "Line 45 in hooks.py"
    confidence: float = Field(default=1.0, ge=0, le=1)

# --- 2. JUDICIAL OPINION MODEL ---
# Judges must use this to argue their perspective.
class JudicialOpinion(BaseModel):
    judge_persona: Literal["Prosecutor", "Defense", "TechLead"]
    tier: Literal["Basic", "Essential", "Advanced"]
    score: int = Field(ge=1, le=5)
    argument: str
    evidence_referenced: List[str]

# --- 3. THE GLOBAL AGENT STATE ---
# The shared memory of the swarm.
class AgentState(TypedDict):
    repo_url: str
    pdf_path: str
    
    # Discovery Layer (Parallel Detectives append here)
    forensic_evidence: Annotated[List[Evidence], operator.add]
    
    # Judicial Layer (Parallel Judges append here)
    judicial_opinions: Annotated[List[JudicialOpinion], operator.add]
    
    # Final Executive Layer
    final_score: float
    final_audit_report: str
    
    current_status: str
    