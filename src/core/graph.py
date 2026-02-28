from langgraph.graph import StateGraph, END
from src.core.state import AgentState

# --- 1. Infrastructure Imports ---
from src.core.context_builder import context_builder_node
from src.core.dispatcher import dispatcher_node
from src.nodes.detective import detective_node as aggregator # Your detective.py file

# --- 2. Detective & Judge Imports ---
from src.agents.detectives.repo import repo_investigator
from src.agents.detectives.docs import doc_analyst
from src.agents.detectives.vision import vision_inspector
from src.agents.judges.prosecutor import prosecutor
from src.agents.judges.defense import defense_node as defense
from src.agents.judges.tech_lead import tech_lead_node as tech_lead
from src.agents.justice.chief_justice import chief_justice_node

builder = StateGraph(AgentState)

# --- 3. Register Nodes ---
builder.add_node("context_builder", context_builder_node)
builder.add_node("dispatcher", dispatcher_node)
builder.add_node("repo_detective", repo_investigator)
builder.add_node("docs_detective", doc_analyst)
builder.add_node("vision_detective", vision_inspector)
builder.add_node("aggregator", aggregator) # The 'Clerk'
builder.add_node("prosecutor", prosecutor)
builder.add_node("defense", defense)
builder.add_node("tech_lead", tech_lead)
builder.add_node("chief_justice", chief_justice_node)

# --- 4. Define the Sovereign Parallel Flow ---

# STEP A: Setup
builder.set_entry_point("context_builder")
builder.add_edge("context_builder", "dispatcher")

# STEP B: Detective Fan-Out (Parallel Evidence Collection)
builder.add_edge("dispatcher", "repo_detective")
builder.add_edge("dispatcher", "docs_detective")
builder.add_edge("dispatcher", "vision_detective")

# STEP C: Detective Fan-In (The Aggregator barrier)
# This ensures ALL evidence is collected before Judges see it
builder.add_edge("repo_detective", "aggregator")
builder.add_edge("docs_detective", "aggregator")
builder.add_edge("vision_detective", "aggregator")

# STEP D: Judicial Fan-Out (The Dialectical Debate)
# Now the Judges run in parallel on the SAME aggregated evidence
builder.add_edge("aggregator", "prosecutor")
builder.add_edge("aggregator", "defense")
builder.add_edge("aggregator", "tech_lead")

# STEP E: Final Synthesis
builder.add_edge("prosecutor", "chief_justice")
builder.add_edge("defense", "chief_justice")
builder.add_edge("tech_lead", "chief_justice")
builder.add_edge("chief_justice", END)

forensic_app = builder.compile()