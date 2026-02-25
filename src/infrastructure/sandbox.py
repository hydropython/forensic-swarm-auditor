import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

class ForensicSandbox:
    """🛡️ Infrastructure Tier: Manages isolated 'Crime Scenes'."""
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.root_path: Path = None

    @contextmanager
    def create_workspace(self) -> Generator[Path, None, None]:
        tmp_dir = tempfile.mkdtemp(prefix="forensic_audit_")
        try:
            self.root_path = Path(tmp_dir)
            self._clone_repo()
            yield self.root_path
        finally:
            self._cleanup()

    def _clone_repo(self):
        """Full clone to enable longitudinal git analysis."""
        try:
            subprocess.run(
                ["git", "clone", self.repo_url, str(self.root_path)],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git Clone Failed: {e.stderr}")

    def _cleanup(self):
        if self.root_path and self.root_path.exists():
            shutil.rmtree(self.root_path)