import os
import tempfile
import shutil
import subprocess
from contextlib import contextmanager
from typing import Generator
from pathlib import Path

class ForensicSandbox:
    """
    Manages the isolated environment for repository auditing.
    Ensures that external code never touches the host's primary file system.
    """
    
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.root_path: Path = None

    @contextmanager
    def create_workspace(self) -> Generator[Path, None, None]:
        """Creates a temporary directory and clones the target repo into it."""
        tmp_dir = tempfile.mkdtemp(prefix="courtroom_audit_")
        try:
            self.root_path = Path(tmp_dir)
            self._clone_repo()
            yield self.root_path
        finally:
            self._cleanup()

    def _clone_repo(self):
        """Executes a shallow clone for speed and isolation."""
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", self.repo_url, str(self.root_path)],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git Clone Failed: {e.stderr}")

    def _cleanup(self):
        """Wipes the forensic evidence after the audit is complete."""
        if self.root_path and self.root_path.exists():
            shutil.rmtree(self.root_path)

# --- COMMIT: Initialized Forensic Sandbox Infrastructure ---