import yaml
from git import Repo

def forensic_protocol_c(repo_path: str):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(reverse=True)) # Oldest first
    
    narrative = []
    for commit in commits:
        # Check if they built Scaffolding (folders/configs) before Logic (.py/.ts)
        files_changed = list(commit.stats.files.keys())
        narrative.append({"time": commit.authored_datetime, "files": files_changed})
    
    # Advanced logic: Compare timestamps of .orchestration vs src/
    return narrative