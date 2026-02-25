import os
import shutil
import tempfile
from pathlib import Path
from contextlib import contextmanager

class ForensicSandbox:
    """
    Manages isolated environments for repository audits.
    Ensures 'Clean Room' conditions for every forensic run.
    """
    
    def __init__(self, base_path: str = "./temp_audits"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    @contextmanager
    def create_workspace(self, prefix: str = "audit_"):
        """
        Context manager to create and automatically cleanup a sandbox.
        Usage:
            with sandbox.create_workspace() as workspace_path:
                # do work here
        """
        workspace = Path(tempfile.mkdtemp(dir=self.base_path, prefix=prefix))
        try:
            yield workspace
        finally:
            self.cleanup(workspace)

    def cleanup(self, path: Path):
        """Securely removes the temporary workspace."""
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            print(f"🧹 Sandbox cleaned: {path}")

# Global instance for easy access across nodes
sandbox_manager = ForensicSandbox()