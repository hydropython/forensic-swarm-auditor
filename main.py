import os
from dotenv import load_dotenv
from src.engine import graph

def run_forensic_audit(repo_url: str, pdf_path: str):
    load_dotenv()
    
    # Initial State
    initial_state = {
        "repo_url": repo_url,
        "pdf_path": pdf_path,
        "workspace_path": "./temp_audit", # Local sandbox
        "rubric_dimensions": [], # To be populated by doc_analyst
        "evidences": {},
        "refined_evidences": [],
        "opinions": [],
        "metadata": None 
    }

    print(f"🕵️‍♂️ Starting Swarm Audit for: {repo_url}")
    
    # Run the Graph
    final_state = graph.invoke(initial_state)
    
    print("\n--- 🏛️ JUDICIAL VERDICT ---")
    print(final_state.get("final_report", "Audit failed to reach a verdict."))

if __name__ == "__main__":
    # Test it with a real repo
    REPO = "https://github.com/example/target-repo"
    RUBRIC = "rubrics/week2_criteria.pdf"
    run_forensic_audit(REPO, RUBRIC)