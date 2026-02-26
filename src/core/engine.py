from langgraph.graph import StateGraph, START, END
# Synchronize with your state.py naming convention
from src.core.state import ForensicState as AgentState 

# 🕵️ Detectives
from src.agents.detectives.repo import repo_investigator
from src.agents.detectives.docs import doc_analyst

# ⚖️ Judges
from src.agents.judges.prosecutor import prosecutor_node
from src.agents.judges.defense import defense_node
from src.agents.judges.Tech_lead import tech_lead_node

# 🏛️ Justice & Aggregator
from src.agents.justice.chief_justice import chief_justice_node
from src.nodes.aggregator import evidence_aggregator, check_evidence_quality

# 1. Initialize Graph
builder = StateGraph(AgentState)

# 2. Add All Nodes
builder.add_node("repo_investigator", repo_investigator)
builder.add_node("doc_analyst", doc_analyst)
builder.add_node("clerk_aggregator", evidence_aggregator)
builder.add_node("prosecutor", prosecutor_node)
builder.add_node("defense", defense_node)
builder.add_node("tech_lead", tech_lead_node)
builder.add_node("chief_justice", chief_justice_node)

# --- PHASE 1: DETECTIVE FAN-OUT ---
# Start both detectives in parallel
builder.add_edge(START, "repo_investigator")
builder.add_edge(START, "doc_analyst")

# Wait for both to finish before aggregating
builder.add_edge("repo_investigator", "clerk_aggregator")
builder.add_edge("doc_analyst", "clerk_aggregator")

# --- PHASE 2: THE BROADCAST ROUTER ---
# ✅ FIX: Removed the list from the dictionary to stop the TypeError.
# If quality is sufficient, we go to the Prosecutor.
builder.add_conditional_edges(
    "clerk_aggregator",
    check_evidence_quality,
    {
        "incomplete": "repo_investigator",
        "sufficient": "prosecutor" 
    }
)

# --- PHASE 3: PARALLEL JUDICIAL TRIGGER ---
# Since "sufficient" triggered the Prosecutor, we add these edges 
# to ensure Defense and Tech Lead also start once the Aggregator is done.
builder.add_edge("clerk_aggregator", "defense")
builder.add_edge("clerk_aggregator", "tech_lead")

# --- PHASE 4: THE JUDICIAL FAN-IN ---
# All three judges must finish before the Chief Justice starts.
# This works because state['opinions'] uses operator.add.
builder.add_edge("prosecutor", "chief_justice")
builder.add_edge("defense", "chief_justice")
builder.add_edge("tech_lead", "chief_justice")

# Final Exit from the courtroom
builder.add_edge("chief_justice", END)

# 3. Compile
# This should now bypass the unhashable list error!
forensic_app = builder.compile()