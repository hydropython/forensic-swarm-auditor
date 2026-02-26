from pathlib import Path
from docling.document_converter import DocumentConverter
# Import the shared state and evidence model
from src.core.state import ForensicState, Evidence

class DocAnalyst:
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
        except Exception:
            return False

    def find_claim(self, keyword: str) -> Evidence:
        found = keyword.lower() in self._markdown_content.lower()
        snippet = None
        if found:
            idx = self._markdown_content.lower().find(keyword.lower())
            # Capture context around the keyword
            snippet = self._markdown_content[max(0, idx-100) : idx+300]
            
        return Evidence(
            goal=f"Claim: {keyword}", 
            found=found, 
            content=snippet,
            location=str(self.pdf_path), 
            rationale="Docling automated scan of rubric documentation.", 
            confidence=0.9 if found else 0.2
        )

def doc_analyst(state: ForensicState): 
    """🕵️ Protocol A.2: Documentation Analysis Node"""
    # Detect which path key is being used in the state
    path_val = state.get("pdf_path") or state.get("rubric_path")
    
    if not path_val:
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Path Check", found=False, location="State", rationale="No path provided in state", confidence=1.0)]}}

    analyst = DocAnalyst(Path(path_val))
    
    if not analyst.ingest_pdf():
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Ingestion", found=False, location=str(path_val), rationale="File missing or corrupt", confidence=1.0)]}}
    
    # Keywords the detective is looking for
    claims = ["Fan-In / Fan-Out", "Dialectical Synthesis"]
    findings = [analyst.find_claim(c) for c in claims]
    
    return {"evidences": {"doc_detective": findings}}