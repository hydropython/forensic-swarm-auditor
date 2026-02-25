from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def prosecutor_node(state: AgentState):
    """
    ⚖️ Statute of Orchestration (Prosecutor's Handbook)
    Charges: Orchestration Fraud, Hallucination Liability.
    """
    # 1. Initialize the LLM with Structured Output (Requirement Phase 3)
    llm = ChatOpenAI(model="gpt-4o")
    structured_llm = llm.with_structured_output(JudicialOpinion)

    # 2. Prepare the "Evidence Brief"
    # We feed the judge the refined evidence and the metadata
    evidence_text = "\n".join([f"- {e.goal}: {e.rationale} (Found: {e.found})" 
                              for e in state["refined_evidences"]])
    
    prompt = f"""
    SYSTEM: You are the PROSECUTOR. Your goal is to find "Orchestration Fraud".
    
    FORENSIC EVIDENCE:
    {evidence_text}
    
    GIT LOG HISTORY:
    {state['metadata'].git_log}
    
    STATUTE OF ORCHESTRATION:
    - Violation: If the flow is linear (A -> B -> C) instead of parallel.
    - Violation: If documentation claims features (like AST) that aren't in the code.
    
    TASK: Render a verdict with a score (1-5) and specific arguments citing the evidence.
    """

    # 3. Invoke the LLM
    opinion = structured_llm.invoke(prompt)
    
    # 4. Return as an appended list (thanks to operator.add in state)
    return {"opinions": [opinion]}