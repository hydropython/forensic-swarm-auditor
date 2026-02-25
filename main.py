import os
from git import Repo
from src.core.graph import build_courtroom_swarm

def run_audit(repo_url: str):
    # 1. Setup Workspace
    target_dir = "data/input/temp_repo"
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir) # Clean slate for every audit
    
    print(f"🕵️‍♂️ Cloning {repo_url} for forensic analysis...")
    Repo.clone_from(repo_url, target_dir)

    # 2. Initialize State
    initial_state = {
        "repo_url": repo_url,
        "forensic_evidence": [],
        "judicial_opinions": [],
        "final_score": 0.0,
        "current_status": "Starting Audit"
    }

    # 3. Execute the Swarm
    courtroom = build_courtroom_swarm()
    final_state = courtroom.invoke(initial_state)

    # 4. The Verdict
    print("\n" + "="*50)
    print(f"⚖️ FINAL VERDICT: {final_state['final_score']:.2f}/5.00")
    print(f"STATUS: {final_state['current_status']}")
    print("="*50)
    
    for opinion in final_state['judicial_opinions']:
        print(f"\n[{opinion.judge_persona}]: {opinion.argument}")

if __name__ == "__main__":
    # Test it with your own repo or a sample
    sample_repo = "https://github.com/hydropython/forensic-swarm-auditor.git"
    run_audit(sample_repo)
