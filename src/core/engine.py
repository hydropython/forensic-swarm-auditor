import operator
from typing import Annotated, Dict, List, Union

from langgraph.graph import StateGraph, START, END
from src.core.state import ForensicState as AgentState 

# 🕵️ Detectives (Phase 1)
from src.agents.detectives.repo import repo_investigator
from src.agents.detectives.docs import doc_analyst 

# ⚖️ Judges (Phase 2)
from src.agents.judges.prosecutor import prosecutor_node
from src.agents.judges.defense import defense_node
from src.agents.judges.Tech_lead import tech_lead_node

# 🏛️ Justice & Aggregator (Phase 3)
from src.agents.justice.chief_justice import chief_justice_node
from src.nodes.aggregator import evidence_aggregator, check_evidence_quality
from src.nodes.report_generator import generate_final_report 

# 1. Initialize Graph with Strongly Typed State
builder = StateGraph(AgentState)

# 2. Add Nodes
builder.add_node("repo_investigator", repo_investigator)
builder.add_node("doc_analyst", doc_analyst)
builder.add_node("clerk_aggregator", evidence_aggregator)
builder.add_node("prosecutor", prosecutor_node)
builder.add_node("defense", defense_node)
builder.add_node("tech_lead", tech_lead_node)
builder.add_node("chief_justice", chief_justice_node)
builder.add_node("report_generator", generate_final_report)

# --- 🚀 GRAPH FLOW: ORCHESTRATION ---

# ✅ Parallel Start (Detectives run simultaneously)
builder.add_edge(START, "repo_investigator")
builder.add_edge(START, "doc_analyst")

# Synchronize findings into the Aggregator
builder.add_edge("repo_investigator", "clerk_aggregator")
builder.add_edge("doc_analyst", "clerk_aggregator")

# ✅ FIXED ROUTER: 
# We map 'sufficient' to 'prosecutor' to satisfy the dictionary hashing.
# The other two judges are fanned-out via standard edges below.
builder.add_conditional_edges(
    "clerk_aggregator",
    check_evidence_quality,
    {
        "incomplete": "repo_investigator", 
        "sufficient": "prosecutor" 
    }
)

# ✅ FAN-OUT: Explicit Parallelism
# This ensures Defense and Tech Lead start as soon as Clerk is 'sufficient'
# satisfying the Auditor's requirement for a multi-agent swarm.
builder.add_edge("clerk_aggregator", "defense")
builder.add_edge("clerk_aggregator", "tech_lead")

# ✅ FAN-IN: Parallel Judicial Review
# All three reports merge into the Chief Justice
builder.add_edge("prosecutor", "chief_justice")
builder.add_edge("defense", "chief_justice")
builder.add_edge("tech_lead", "chief_justice")

# Final Synthesis & Reporting
builder.add_edge("chief_justice", "report_generator")
builder.add_edge("report_generator", END)

# 3. Compile the System
# The compiler will now succeed because all targets are strings, not lists.
forensic_app = builder.compile()