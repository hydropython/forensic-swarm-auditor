from src.core.state import AgentState

def chief_justice_node(state: AgentState):
    """
    ⚖️ The Chief Justice Node
    Function: Collects the list of 'opinions' and synthesizes the Final Report.
    """
    opinions = state["opinions"]
    
    # 1. Calculation Logic
    scores = [o.score for o in opinions]
    final_score = sum(scores) / len(scores) if scores else 0
    
    # 2. Reasoning Synthesis
    # It looks at the Prosecutor's complaints vs the Defense's justifications
    summary_brief = "\n".join([f"⚖️ {o.judge}: {o.argument}" for o in opinions])
    
    report = f"""
    FINAL FORENSIC VERDICT
    ======================
    Weighted Score: {final_score}/5
    
    COURTROOM SUMMARY:
    {summary_brief}
    
    FINAL DETERMINATION: {"APPROVED" if final_score >= 3.5 else "REJECTED"}
    """
    
    # This updates the 'final_report' key in your AgentState
    return {"final_report": report}