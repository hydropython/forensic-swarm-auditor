from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.detectives import repo_investigator, doc_analyst
from src.nodes.judges import prosecutor, defense, tech_lead
from src.nodes.justice import chief_justice

# 1. Initialize the Graph with our typed AgentState
workflow = StateGraph(AgentState)

# 2. Add Forensic Detective Nodes
workflow.add_node("repo_investigator", repo_investigator)
workflow.add_node("doc_analyst", doc_analyst)

# 3. Add Judicial Nodes
workflow.add_node("prosecutor", prosecutor)
workflow.add_node("defense", defense)
workflow.add_node("tech_lead", tech_lead)

# 4. Add the Final Synthesis Node
workflow.add_node("chief_justice", chief_justice)

# --- THE WIRING (Orchestration) ---

# FAN-OUT: Start both detectives at the same time
workflow.add_edge(START, "repo_investigator")
workflow.add_edge(START, "doc_analyst")

# FAN-IN & FAN-OUT: Once detectives finish, trigger all judges in parallel
# Note: In LangGraph, we use a 'wait' or aggregator node here
workflow.add_edge(["repo_investigator", "doc_analyst"], "prosecutor")
workflow.add_edge(["repo_investigator", "doc_analyst"], "defense")
workflow.add_edge(["repo_investigator", "doc_analyst"], "tech_lead")

# FAN-IN: Chief Justice waits for all opinions before ruling
workflow.add_edge(["prosecutor", "defense", "tech_lead"], "chief_justice")
workflow.add_edge("chief_justice", END)

app = workflow.compile()