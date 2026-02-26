from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def tech_lead_node(state: AgentState):
    """
    ⚖️ The Tech Lead: Evaluates the stack, scalability, and 
    engineering "cleanliness" of the implementation.
    """
    print("⚖️ Tech Lead: Evaluating technical feasibility and stack choices...")
    
    # 1. Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2) 
    structured_llm = llm.with_structured_output(JudicialOpinion)

    # 2. DATA SHIELD: Handle Dict or Pydantic Object
    refined_evidences = state.get("refined_evidences", [])
    evidence_list = []

    for e in refined_evidences:
        if isinstance(e, dict):
            goal = e.get("goal", "Unknown")
            location = e.get("location", "N/A")
            found = e.get("found", False)
        else:
            goal = getattr(e, "goal", "Unknown")
            location = getattr(e, "location", "N/A")
            found = getattr(e, "found", False)
        
        evidence_list.append(f"- Requirement: {goal} | File: {location} | Validated: {found}")
    
    evidence_text = "\n".join(evidence_list)

    # 3. Judicial Tech Prompt
    prompt = f"""
    SYSTEM: You are the TECH LEAD. Focus on best practices, code structure, and technical debt.
    Is the project using modern tools (uv, langgraph, pydantic)? 
    Is the code organized in a way that is maintainable?
    
    EVIDENCE FROM SCAN:
    {evidence_text}
    
    TASK: Provide a technical score (1-5) based on engineering excellence.
    """
    
    # 4. Invoke and Return
    opinion = structured_llm.invoke(prompt)
    opinion.judge = "TechLead"
    
    return {"opinions": [opinion]}