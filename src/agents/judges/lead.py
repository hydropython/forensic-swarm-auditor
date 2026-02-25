def tech_lead_node(state: AgentState):
    """
    🔧 Statute of Engineering (Tech Lead's Handbook)
    Standard: Pydantic Rigor vs Dict Soups.
    """
    llm = ChatOpenAI(model="gpt-4o").with_structured_output(JudicialOpinion)
    
    # Logic to check if metadata shows a uv.lock
    security_status = "SECURE" if state["metadata"].has_uv_lock else "NEGLIGENT"
    
    prompt = f"""
    SYSTEM: You are the TECH LEAD. Review the evidence for architectural debt.
    SECURITY AUDIT: {security_status}
    ...
    """
    opinion = llm.invoke(prompt)
    return {"opinions": [opinion]}