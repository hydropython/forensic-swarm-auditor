# 🕵️ Detectives
from src.agents.detectives.repo import repo_investigator
from src.agents.detectives.docs import doc_analyst

# ⚖️ Judges (Updated Paths)
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
# Start both detectives at the same time
builder.add_edge(START, "repo_investigator")
builder.add_edge(START, "doc_analyst")

# Wait for both to finish before aggregating
builder.add_edge("repo_investigator", "clerk_aggregator")
builder.add_edge("doc_analyst", "clerk_aggregator")

# --- PHASE 2: THE MIN-MAX LOOP (Conditional) ---
# This is where the loop happens. If evidence is low, it goes back to detectives.
builder.add_conditional_edges(
    "clerk_aggregator",
    check_evidence_quality,
    {
        "incomplete": "repo_investigator", # Loop back to start node of detectives
        "sufficient": ["prosecutor", "defense", "tech_lead"] # Parallel Judicial Fan-Out
    }
)

# --- PHASE 3: THE JUDICIAL FAN-IN ---
# The Chief Justice waits for ALL THREE judges (Fan-In)
builder.add_edge(["prosecutor", "defense", "tech_lead"], "chief_justice")

# Final Exit
builder.add_edge("chief_justice", END)

# 3. Compile
graph = builder.compile()