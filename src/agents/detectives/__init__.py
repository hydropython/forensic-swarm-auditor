from .repo import repo_investigator
from .docs import doc_analyst

# Stub or comment out vision_inspector if the file isn't ready
try:
    from .vision import vision_inspector
except ImportError:
    # A simple stub to prevent the graph from crashing during import
    def vision_inspector(state):
        return {"evidences": {"vision_agent": [{"found": False, "criterion": "Vision", "rationale": "Vision system offline (Poppler/Stub)"}]}}

__all__ = ["repo_investigator", "doc_analyst", "vision_inspector"]