import os
from langsmith import Client
from uuid import uuid4
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()

class ObservabilityManager:
    def __init__(self):
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        self.project_name = os.getenv("LANGCHAIN_PROJECT", "Forensic-Swarm-Auditor-W2")
        self.client = Client()

    def initialize_courtroom(self):
        """
        Forces a heartbeat trace to LangSmith. 
        This ensures the project exists in the dashboard before the Audit starts.
        """
        if not self.api_key:
            print("❌ CRITICAL: LANGCHAIN_API_KEY is missing from environment.")
            return False
        
        try:
            run_id = uuid4()
            # Send a 'System Ready' signal to LangSmith
            self.client.create_run(
                name="Forensic_Infrastructure_Check",
                run_type="chain",
                inputs={"status": "initializing_agent_swarm"},
                project_name=self.project_name,
                id=run_id
            )
            self.client.update_run(run_id, outputs={"result": "Infrastructure Verified"})
            print(f"✅ Handshake Success: Project '{self.project_name}' is now active.")
            return True
        except Exception as e:
            print(f"❌ Handshake Failed: {str(e)}")
            return False

# Self-test logic
if __name__ == "__main__":
    obs = ObservabilityManager()
    obs.initialize_courtroom()