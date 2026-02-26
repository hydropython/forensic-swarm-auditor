import re
from pathlib import Path
from docling.document_converter import DocumentConverter
from src.core.state import ForensicState, Evidence

class DocAnalystEngine:
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()
        self._markdown_content: str = ""

    def ingest_pdf(self) -> bool:
        if not self.pdf_path.exists(): 
            return False
        try:
            result = self.converter.convert(str(self.pdf_path))
            self._markdown_content = result.document.export_to_markdown()
            return True
        except Exception as e:
            print(f"⚠️ Ingestion Error: {e}")
            return False

    def analyze_theoretical_depth(self, criteria: dict) -> list:
        """
        🕵️ Phase 3: Semantic Depth Check
        Matches concepts using a 'Cluster' of keywords to prevent false negatives.
        """
        depth_evidence = []
        for concept, aliases in criteria.items():
            found = False
            best_match = ""
            
            # Check for any alias in the document
            for alias in aliases:
                pattern = re.compile(f"([^.?!]*{re.escape(alias)}[^.?!]*)", re.IGNORECASE)
                matches = pattern.findall(self._markdown_content)
                
                if matches:
                    found = True
                    best_match = matches[0]
                    break # Stop at first match for this concept
            
            is_deep = len(best_match.split()) > 10 if found else False
            
            depth_evidence.append(Evidence(
                goal=f"Theoretical Depth: {concept}",
                found=found,
                location=str(self.pdf_path.name),
                rationale=f"Verified via semantic match: '{best_match[:40]}...'" if found else f"Concept '{concept}' not described in documentation.",
                content=best_match if found else None
            ))
        return depth_evidence

    def extract_file_paths(self) -> list:
        # Improved Regex: Looks for anything matching folder/file.ext or .py
        path_pattern = r"([a-zA-Z0-9_\-\./]+\.(?:py|json|yaml|md|docx|pdf))"
        paths = list(set(re.findall(path_pattern, self._markdown_content)))
        # Filter out common junk
        paths = [p for p in paths if '/' in p or p.endswith('.py')]
        
        return [Evidence(
            goal="Host Analysis Accuracy (Path Extraction)",
            found=len(paths) > 0,
            location=str(self.pdf_path.name),
            rationale=f"Extracted {len(paths)} unique file paths from documentation for cross-verification.",
            content=f"Detected: {', '.join(paths[:5])}" if paths else "No specific file paths detected."
        )]

def doc_analyst(state: ForensicState): 
    path_val = state.get("rubric_path") or state.get("pdf_path")
    
    if not path_val:
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Path Check", found=False, location="State", rationale="No path provided.")]}}

    analyst = DocAnalystEngine(Path(path_val))
    if not analyst.ingest_pdf():
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Ingestion", found=False, location=str(path_val), rationale="Could not read document.")]}}
    
    # --- SEMANTIC MAPPING ---
    # We look for clusters of words so you don't fail on exact wording
    semantic_criteria = {
        "Dialectical Synthesis": ["Synthesis", "debate", "prosecutor", "defense", "arguing", "judicial", "opinion"],
        "Fan-In / Fan-Out": ["Parallel", "edges", "graph", "orchestration", "concurrent", "multi-agent"],
        "Metacognition": ["Self-reflection", "feedback loop", "audit", "reasoning", "architectural explanation"],
        "State Synchronization": ["State", "TypedDict", "ForensicState", "data flow", "sync", "persistence"]
    }
    
    findings = analyst.analyze_theoretical_depth(semantic_criteria)
    findings.extend(analyst.extract_file_paths())
    
    return {"evidences": {"doc_detective": findings}}