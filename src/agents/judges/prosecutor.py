from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion, Evidence

def prosecutor_node(state: AgentState):
    """
    ⚖️ Statute of Orchestration (Prosecutor's Handbook)
    Charges: Orchestration Fraud, Hallucination Liability.
    """
    # 1. Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(JudicialOpinion)

    # 2. Robust Evidence Extraction (Handles Dict or Pydantic Object)
    refined_evidences = state.get("refined_evidences", [])
    evidence_list = []

    for e in refined_evidences:
        # Check if it's a dictionary or a Pydantic object
        if isinstance(e, dict):
            goal = e.get("goal", "Unknown")
            found = e.get("found", False)
            rationale = e.get("rationale", "No rationale provided")
            location = e.get("location", "Unknown location")
        else:
            goal = getattr(e, "goal", "Unknown")
            found = getattr(e, "found", False)
            rationale = getattr(e, "rationale", "No rationale provided")
            location = getattr(e, "location", "Unknown location")
        
        status = "✅ FOUND" if found else "❌ MISSING"
        evidence_list.append(f"- [{status}] GOAL: {goal} | LOC: {location} | RATIONALE: {rationale}")

    evidence_text = "\n".join(evidence_list)
    
    # Handle metadata (also checking if it's a dict or object)
    metadata = state.get('metadata')
    if isinstance(metadata, dict):
        git_log = metadata.get("git_log", [])
    else:
        git_log = getattr(metadata, "git_log", [])
    
    git_context = "\n".join(git_log[-10:]) if git_log else "No Git history found."

    # 3. Judicial Instructions
    system_prompt = f"""
    SYSTEM: You are the PROSECUTOR in a forensic code audit. Your goal is to identify "Orchestration Fraud" and technical gaps.
    
    CRIMINAL STATUTES:
    1. Orchestration Fraud: Claiming a multi-agent system when the code is actually linear.
    2. Hallucination Liability: Claiming features in documentation that do not exist in code.
    3. Structural Negligence: Missing core files (pyproject.toml, .env.example).

    FORENSIC EVIDENCE PROVIDED BY DETECTIVES:
    {evidence_text}
    
    RECENT GIT HISTORY:
    {git_context}
    
    TASK: Analyze the evidence objectively. If a requirement is missing, you MUST penalize. 
    Provide a score (1-5) where 1 is "Major Violation" and 5 is "Compliant".
    You must cite specific evidence (the 'GOAL' text) in your cited_evidence list.
    """

    # 4. Invoke LLM
    print("⚖️ Prosecutor: Examining evidence for violations...")
    opinion = structured_llm.invoke(system_prompt)
    
    # 5. Final validation of the structured output
    opinion.judge = "Prosecutor"
    
    return {"opinions": [opinion]}