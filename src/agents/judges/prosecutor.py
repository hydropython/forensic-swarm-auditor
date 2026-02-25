from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def prosecutor_node(state: AgentState):
    """
    ⚖️ Statute of Orchestration (Prosecutor's Handbook)
    Charges: Orchestration Fraud, Hallucination Liability.
    """
    # 1. Initialize with strict schema enforcement
    llm = ChatOpenAI(model="gpt-4o", temperature=0) # Temp 0 for judicial consistency
    structured_llm = llm.with_structured_output(JudicialOpinion)

    # 2. Extract context from the "Fact Record"
    evidence_text = "\n".join([
        f"- GOAL: {e.goal} | FOUND: {e.found} | RATIONALE: {e.rationale} | LOC: {e.location}" 
        for e in state["refined_evidences"]
    ])
    
    git_context = "\n".join(state['metadata'].git_log[-10:]) # Last 10 commits

    system_prompt = f"""
    SYSTEM: You are the PROSECUTOR. Your goal is to identify "Orchestration Fraud" and technical gaps.
    
    CRIMINAL STATUTES:
    1. Orchestration Fraud: Claiming a multi-agent system when the code is actually linear.
    2. Hallucination Liability: Claiming features in documentation that do not exist in code.
    3. Structural Negligence: Missing core files (pyproject.toml, .env.example).

    FORENSIC EVIDENCE PROVIDED BY CLERK:
    {evidence_text}
    
    RECENT GIT HISTORY:
    {git_context}
    
    TASK: Analyze the evidence objectively. If a requirement is missing, you MUST penalize. 
    Provide a score (1-5) where 1 is "Major Violation" and 5 is "Compliant".
    """

    # 3. Invoke and return
    # The return is wrapped in a list because the state uses operator.add
    opinion = structured_llm.invoke(system_prompt)
    
    # Ensure the 'judge' field is correctly set to Prosecutor
    opinion.judge = "Prosecutor"
    
    return {"opinions": [opinion]}