import re
from pathlib import Path
from pypdf import PdfReader 
from src.core.state import ForensicState, Evidence

class DocAnalystEngine:
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self._markdown_content: str = ""

    def ingest_pdf(self) -> bool:
        if not self.pdf_path.exists(): 
            return False
        try:
            # 🚀 Lightweight extraction: No AI models, no downloads
            reader = PdfReader(self.pdf_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            
            self._markdown_content = text
            return True
        except Exception as e:
            print(f"⚠️ Ingestion Error: {e}")
            return False

    def analyze_theoretical_depth(self, criteria: dict) -> list:
        depth_evidence = []
        for concept, aliases in criteria.items():
            found = False
            best_match = ""
            for alias in aliases:
                # Regex to find the sentence containing the keyword
                pattern = re.compile(f"([^.?!]*{re.escape(alias)}[^.?!]*)", re.IGNORECASE)
                matches = pattern.findall(self._markdown_content)
                if matches:
                    found = True
                    best_match = matches[0].strip()
                    break 
            
            depth_evidence.append(Evidence(
                goal=f"Theoretical Depth: {concept}",
                found=found,
                location=str(self.pdf_path.name),
                rationale=f"Verified via semantic match: '{best_match[:40]}...'" if found else f"Concept '{concept}' not found.",
                content=best_match if found else None
            ))
        return depth_evidence

    def extract_file_paths(self) -> list:
        # 🚀 More aggressive regex to catch paths like src.core.state or just filenames
        path_pattern = r"([a-zA-Z0-9_\-\./]+\.(?:py|toml|md|json))|([a-zA-Z0-9_\-]+\/[a-zA-Z0-9_\-\.]+)"
        raw_matches = re.findall(path_pattern, self._markdown_content)
        
        # Flatten and clean the results
        paths = list(set([match[0] or match[1] for match in raw_matches]))
        paths = [p for p in paths if p and ('.py' in p or '/' in p or 'src' in p)]

        return [Evidence(
            goal="Host Analysis Accuracy (Path Extraction)",
            found=len(paths) > 0,
            location=str(self.pdf_path.name),
            rationale=f"Extracted {len(paths)} paths: {', '.join(paths[:3])}" if paths else "No paths found.",
            content=str(paths)
        )]

def doc_analyst(state: ForensicState): 
    # Try multiple keys to find the document path
    path_val = state.get("rubric_path") or state.get("pdf_path")
    
    if not path_val:
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Path Check", found=False, location="State", rationale="No path provided.")]}}

    analyst = DocAnalystEngine(Path(path_val))
    if not analyst.ingest_pdf():
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Ingestion", found=False, location=str(path_val), rationale="Could not read document.")]}}
    
    semantic_criteria = {
        "Dialectical Synthesis": ["Synthesis", "debate", "prosecutor", "defense", "judicial"],
        "Fan-In / Fan-Out": ["Parallel", "edges", "graph", "orchestration", "fan-out"],
        "Metacognition": ["Self-reflection", "audit", "reasoning", "metacognition"],
        "State Synchronization": ["State", "TypedDict", "Pydantic", "synchronization"]
    }
    
    findings = analyst.analyze_theoretical_depth(semantic_criteria)
    findings.extend(analyst.extract_file_paths())
    
    return {"evidences": {"doc_detective": findings}}