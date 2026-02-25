from langchain_openai import ChatOpenAI
from src.core.state import AgentState

def justice_synthesis_node(state: AgentState):
    """
    📜 The Chief Justice: Final Verdict & Markdown Generation.
    Synthesizes Prosecutor, Defense, and Tech Lead opinions.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    
    # 1. Gather all judicial opinions
    opinions_summary = ""
    for op in state["opinions"]:
        opinions_summary += f"### {op.judge} (Score: {op.score}/5)\n- Argument: {op.argument}\n\n"

    # 2. Final Synthesis Prompt
    prompt = f"""
    SYSTEM: You are the CHIEF JUSTICE. Your task is to provide the final sentencing.
    
    PROJECT METADATA:
    - Version: {state['metadata'].version}
    - Git Progression: {state['metadata'].progression_score}
    
    JUDICIAL OPINIONS:
    {opinions_summary}
    
    TASK:
    1. Resolve conflicts between the Prosecutor and Defense.
    2. Provide a Final Weighted Score.
    3. Output a professional Markdown report including a "Forensic Summary".
    """

    response = llm.invoke(prompt)
    
    return {"final_report": response.content}