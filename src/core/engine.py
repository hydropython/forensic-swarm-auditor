from langgraph.graph import StateGraph, START, END
from src.core.state import ForensicState as AgentState 

# --- Import Detectives ---
from src.agents.detectives.repo import repo_investigator
from src.agents.detectives.docs import doc_analyst 
from src.agents.detectives.vision import vision_inspector  # 🌟 ADD THIS

# --- Import Judicial Swarm ---
from src.agents.judges.prosecutor import prosecutor_node
from src.agents.judges.defense import defense_node
from src.agents.judges.Tech_lead import tech_lead_node
from src.agents.justice.chief_justice import chief_justice_node

# --- Import Utilities ---
from src.nodes.aggregator import evidence_aggregator

builder = StateGraph(AgentState)

# --- 1. Register Nodes ---
builder.add_node("repo_investigator", repo_investigator)
builder.add_node("doc_analyst", doc_analyst)
builder.add_node("vision_inspector", vision_inspector) # 🌟 REGISTER VISION
builder.add_node("clerk_aggregator", evidence_aggregator)

builder.add_node("prosecutor", prosecutor_node)
builder.add_node("defense", defense_node)
builder.add_node("tech_lead", tech_lead_node)
builder.add_node("chief_justice", chief_justice_node)

# --- 2. Orchestration Logic ---

# A. Parallel Forensic Investigation (Fan-Out)
# We now have THREE detectives running at once.
builder.add_edge(START, "repo_investigator")
builder.add_edge(START, "doc_analyst")
builder.add_edge(START, "vision_inspector") # 🌟 ACTIVATE VISION

# B. Evidence Synchronization (Fan-In)
# All three must report to the aggregator before judges are allowed to see facts.
builder.add_edge("repo_investigator", "clerk_aggregator")
builder.add_edge("doc_analyst", "clerk_aggregator")
builder.add_edge("vision_inspector", "clerk_aggregator") # 🌟 CONNECT VISION

# C. Parallel Judicial Deliberation (Fan-Out)
builder.add_edge("clerk_aggregator", "prosecutor")
builder.add_edge("clerk_aggregator", "defense")
builder.add_edge("clerk_aggregator", "tech_lead")

# D. Final Verdict Synthesis (Fan-In)
builder.add_edge("prosecutor", "chief_justice")
builder.add_edge("defense", "chief_justice")
builder.add_edge("tech_lead", "chief_justice")

# E. Conclusion
builder.add_edge("chief_justice", END)

forensic_app = builder.compile()