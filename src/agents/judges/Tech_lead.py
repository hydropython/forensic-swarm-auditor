from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def tech_lead_node(state: AgentState):
    """
    🛠️ The Tech Lead (Engineering Excellence)
    Mission: Evaluate the progression score and technical depth.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(JudicialOpinion)

    prompt = f"""
    SYSTEM: You are the TECH LEAD. You focus on ARCHITECTURE.
    
    METADATA:
    - Version: {state['metadata'].version}
    - Has UV Lock: {state['metadata'].has_uv_lock}
    - Progression Score: {state['metadata'].progression_score}
    
    TASK: Analyze the project's health. Is it a professional setup (UV, structured folders, typing) 
    or just a messy script? Score it 1-5.
    """

    opinion = structured_llm.invoke(prompt)
    opinion.judge = "TechLead"
    
    return {"opinions": [opinion]}