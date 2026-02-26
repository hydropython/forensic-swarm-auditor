from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def defense_node(state: AgentState):
    """
    ⚖️ The Defense Attorney: Focuses on effort, progress, and 
    mitigating circumstances for the developer.
    """
    print("⚖️ Defense: Building the case for the developers...")
    
    # 1. Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7) 
    structured_llm = llm.with_structured_output(JudicialOpinion)

    # 2. DATA SHIELD: Handle Dict or Pydantic Object
    refined_evidences = state.get("refined_evidences", [])
    evidence_list = []

    for e in refined_evidences:
        if isinstance(e, dict):
            goal = e.get("goal", "Unknown")
            rationale = e.get("rationale", "N/A")
            found = e.get("found", False)
        else:
            goal = getattr(e, "goal", "Unknown")
            rationale = getattr(e, "rationale", "N/A")
            found = getattr(e, "found", False)
        
        status = "Implemented" if found else "In-Progress/Missing"
        evidence_list.append(f"- {goal}: {status} | Context: {rationale}")
    
    evidence_text = "\n".join(evidence_list)

    # 3. Judicial Defense Prompt
    prompt = f"""
    SYSTEM: You are the DEFENSE ATTORNEY. Your job is to find the "Silver Lining" in the code.
    Highlight where the developer showed intent or partial progress. 
    Explain why technical debt might be justified for rapid prototyping.
    
    FORENSIC EVIDENCE:
    {evidence_text}
    
    TASK: Provide a score (1-5) and your argument defending the architectural choices.
    1 is "Negligent", 5 is "Exceptional Effort".
    """
    
    # 4. Invoke and Return
    opinion = structured_llm.invoke(prompt)
    opinion.judge = "Defense" # Ensure consistency for the Chief Justice
    
    return {"opinions": [opinion]}