import argparse
import sys
import os
from dotenv import load_dotenv
from src.engine import graph

# Load environment variables early
load_dotenv()

def run_swarm():
    # 1. CLI Interface (Matches Professional README Specs)
    parser = argparse.ArgumentParser(
        description="🏛️ Forensic Swarm Auditor: Neuro-Symbolic Code Review"
    )
    parser.add_argument("--repo", required=True, help="GitHub Repository URL to audit")
    parser.add_argument("--rubric", required=True, help="Path to the PDF rubric")
    parser.add_argument("--workspace", default="./temp_audit", help="Local sandbox path")
    
    args = parser.parse_args()

    # 2. Input Validation
    if not os.path.exists(args.rubric):
        print(f"❌ Error: Rubric file not found at {args.rubric}")
        sys.exit(1)

    print(f"🕵️ Starting Forensic Swarm...")
    print(f"📡 Target Repo: {args.repo}")
    print(f"📄 Using Rubric: {args.rubric}")

    # 3. Execution State
    initial_state = {
        "repo_url": args.repo,
        "pdf_path": args.rubric,
        "workspace_path": args.workspace,
        "evidences": {},
        "opinions": [],
        "final_report": ""
    }

    # 4. Stream Graph Execution
    try:
        # We stream the events so the user sees progress in the terminal
        for output in graph.stream(initial_state):
            for key, value in output.items():
                print(f"✔️ Node '{key}' completed investigation.")
        
        # Final Output
        # (Assuming your graph ends with a 'chief_justice' or similar node)
        print("\n" + "⚖️" * 20)
        print("FINAL JUDICIAL VERDICT")
        print("⚖️" * 20)
        # Note: You would print the actual state content here
        
    except Exception as e:
        print(f"\n❌ SWARM CRITICAL FAILURE: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_swarm()