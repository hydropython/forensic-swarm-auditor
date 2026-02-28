from langgraph.graph import StateGraph, END
from src.core.state import AgentState

# Direct imports from the agent files to avoid __init__ confusion
from src.agents.judges.prosecutor import prosecutor
from src.agents.judges.defense import defense_node as defense
from src.agents.judges.tech_lead import tech_lead_node as tech_lead
from src.agents.justice.chief_justice import chief_justice_node as chief_justice

# 1. Initialize the StateGraph
builder = StateGraph(AgentState)

# 2. Add your Judicial Nodes (Preserving your specific effort & logic)
builder.add_node("prosecutor", prosecutor)
builder.add_node("defense", defense)
builder.add_node("tech_lead", tech_lead)
builder.add_node("chief_justice", chief_justice)

# 3. Define the Flow: The "Judicial Chamber" Sequence
builder.set_entry_point("prosecutor") 
builder.add_edge("prosecutor", "defense")
builder.add_edge("defense", "tech_lead")
builder.add_edge("tech_lead", "chief_justice")
builder.add_edge("chief_justice", END)

# 4. COMPILE THE APP
# This MUST be named forensic_app for main.py to see it
forensic_app = builder.compile()