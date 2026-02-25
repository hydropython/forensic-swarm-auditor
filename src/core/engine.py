from langgraph.graph import StateGraph, START, END
from src.core.state import AgentState
from src.nodes.aggregator import evidence_aggregator, check_evidence_quality
from src.agents.detectives import repo_investigator, doc_analyst
from src.agents.judges import prosecutor, defense, tech_lead
from src.agents.justice import chief_justice

# 1. Initialize Graph
builder = StateGraph(AgentState)

# 2. Add Forensic Nodes
builder.add_node("repo_investigator", repo_investigator)
builder.add_node("doc_analyst", doc_analyst)
builder.add_node("clerk_aggregator", evidence_aggregator)

# 3. Add Judicial Nodes
builder.add_node("prosecutor", prosecutor)
builder.add_node("defense", defense)
builder.add_node("tech_lead", tech_lead)
builder.add_node("chief_justice", chief_justice)

# 4. Define Edge Logic
builder.add_edge(START, "repo_investigator")
builder.add_edge(START, "doc_analyst")
builder.add_edge("repo_investigator", "clerk_aggregator")
builder.add_edge("doc_analyst", "clerk_aggregator")

# --- THE MIN-MAX FORENSIC LOOP ---
builder.add_conditional_edges(
    "clerk_aggregator",
    check_evidence_quality,
    {
        "incomplete": "repo_investigator", # Return to Detective Layer
        "approved": ["prosecutor", "defense", "tech_lead"] # Parallel Judicial Fan-Out
    }
)

builder.add_edge(["prosecutor", "defense", "tech_lead"], "chief_justice")
builder.add_edge("chief_justice", END)

graph = builder.compile()