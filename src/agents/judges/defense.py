from langchain_openai import ChatOpenAI
from src.core.state import AgentState, JudicialOpinion

def defense_node(state: AgentState):
    """
    ⚖️ The Public Defender (Engineering Intent)
    Mission: Highlight mitigation, effort, and unconventional logic.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3) # Slightly higher temp for creative reasoning
    structured_llm = llm.with_structured_output(JudicialOpinion)

    evidence_text = "\n".join([
        f"- {e.goal}: {e.rationale} (Found: {e.found})" 
        for e in state["refined_evidences"]
    ])

    prompt = f"""
    SYSTEM: You are the DEFENSE ATTORNEY. Your goal is to find reasons why the project is VALID.
    
    FORENSIC EVIDENCE:
    {evidence_text}
    
    YOUR MANDATE:
    1. Contextualize Gaps: Is a missing 'AST' replaced by high-quality regex or custom logic?
    2. Effort Analysis: Does the Git log show significant iteration and learning?
    3. Advocacy: Argue for a 5/5 score if the core intent of the rubric is met, even if the implementation is non-standard.
    
    TASK: Render a verdict (Score 1-5) citing evidence that justifies the developer's choices.
    """

    opinion = structured_llm.invoke(prompt)
    opinion.judge = "Defense" # Ensure correct labeling
    
    return {"opinions": [opinion]}