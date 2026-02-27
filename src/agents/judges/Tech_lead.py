from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def tech_lead_node(state: AgentState):
    """
    ⚙️ Statute of Engineering: Evaluates typed rigor and system-level security.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    structured_llm = llm.with_structured_output(JudicialOpinion)

    refined_evidences = state.get("refined_evidences", [])
    evidence_text = "\n".join([
        f"- {e.goal if not isinstance(e, dict) else e.get('goal')}: "
        f"{e.rationale if not isinstance(e, dict) else e.get('rationale')}"
        for e in refined_evidences
    ])

    prompt = f"""
    ROLE: CTO / Expert Witness.
    STATUTE: Protocol B-2 (Engineering Standards).
    
    FORENSIC DATA:
    {evidence_text}

    PRECEDENTS:
    1. PYDANTIC RIGOR: If 'State Rigor' (Phase 0) uses Dictionaries instead of BaseModel, Ruling: 'Technical Debt', Score = 3.
    2. SANDBOXED TOOLING: If 'Safe Tooling' (Phase 2) lacks TemporaryDirectory usage, Ruling: 'Security Negligence', Override Score = 1.

    TASK: Provide technical engineering verdict.
    FORMAT: [RULING]: Analysis. [STATUS]: Maintainability report.
    CONSTRAINT: Dry, technical language. Max 3 sentences.
    """

    opinion = structured_llm.invoke(prompt)
    opinion.judge = "TechLead"
    return {"opinions": [opinion]}