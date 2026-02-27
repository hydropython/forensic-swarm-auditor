from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def defense_node(state: AgentState):
    """
    🛡️ Statute of Effort: Justifies technical debt and highlights underlying sophistication.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    structured_llm = llm.with_structured_output(JudicialOpinion)

    refined_evidences = state.get("refined_evidences", [])
    evidence_text = "\n".join([
        f"- {e.goal if not isinstance(e, dict) else e.get('goal')}: "
        f"{e.rationale if not isinstance(e, dict) else e.get('rationale')}"
        for e in refined_evidences
    ])

    prompt = f"""
    ROLE: Defense Counsel.
    STATUTE: Protocol B-3 (Mitigating Circumstances).
    
    FORENSIC EVIDENCE:
    {evidence_text}

    MITIGATION GUIDELINES:
    1. DEEP COMPREHENSION: If sophisticated AST parsing logic is detected (even if framework execution failed), boost 'Forensic Accuracy' to 3.
    2. DIALECTICAL TENSION: If distinct agent personas are successful, provide partial credit (Score 3 or 4) for 'Judicial Nuance'.
    3. RAPID PROTOTYPING: Argue for technical debt as a strategic choice for velocity.

    TASK: Defend architectural choices and request score adjustments based on intent.
    FORMAT: [MITIGATION]: Justification. [REQUEST]: Score adjustment.
    CONSTRAINT: Professional and pragmatic advocacy. Max 3 sentences.
    """

    opinion = structured_llm.invoke(prompt)
    opinion.judge = "Defense"
    return {"opinions": [opinion]}