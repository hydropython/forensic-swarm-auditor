import asyncio
from src.infrastructure.sandbox import ForensicSandbox
from src.core.engine import graph

async def main():
    repo = "https://github.com/example/student-repo"
    sandbox = ForensicSandbox(repo)
    
    with sandbox.create_workspace() as workspace:
        initial_state = {
            "workspace_path": str(workspace),
            "repo_url": repo,
            "evidences": {},
            "refined_evidences": [],
            "metadata": {"version": "1.0.0", "progression_score": 0.0},
            "opinions": []
        }
        
        print(f"⚖️  Trial starting for {repo}...")
        final_state = await graph.ainvoke(initial_state)
        print("📜 Final Verdict Generated.")

if __name__ == "__main__":
    asyncio.run(main())