from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def prosecutor_node(state: AgentState):
    """
    ⚖️ Statute of Orchestration: Penalizes linear flows and documentation-code gaps.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(JudicialOpinion)

    refined_evidences = state.get("refined_evidences", [])
    evidence_text = "\n".join([
        f"- {e.goal if not isinstance(e, dict) else e.get('goal')}: "
        f"{'FOUND' if (e.found if not isinstance(e, dict) else e.get('found')) else 'MISSING'}"
        for e in refined_evidences
    ])

    prompt = f"""
    ROLE: Lead Prosecutor.
    STATUTE: Protocol B-1 (Orchestration & Hallucination).
    
    FORENSIC EVIDENCE:
    {evidence_text}

    SENTENCING PRECEDENTS:
    1. ORCHESTRATION FRAUD: If 'Graph Orchestration' (Phase 1) is MISSING or the flow is linear, Max Score = 1.
    2. HALLUCINATION LIABILITY: If 'Structured Output' (Phase 3) is MISSING, Max Score = 2.
    3. STRUCTURAL NEGLIGENCE: Penalize if core files or state definitions are absent.

    TASK: Issue formal charges based on evidence. 
    FORMAT: [CHARGE]: Reason. [PENALTY]: Specific score reduction.
    CONSTRAINT: Professional brevity only. No fluff. Max 3 sentences.
    """

    opinion = structured_llm.invoke(prompt)
    opinion.judge = "Prosecutor"
    return {"opinions": [opinion]}