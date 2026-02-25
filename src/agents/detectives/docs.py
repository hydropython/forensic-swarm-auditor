from pathlib import Path
from docling.document_converter import DocumentConverter
from src.core.state import AgentState, Evidence

class DocAnalyst:
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()
        self._markdown_content: str = ""

    def ingest_pdf(self):
        if not self.pdf_path.exists(): return False
        result = self.converter.convert(str(self.pdf_path))
        self._markdown_content = result.document.export_to_markdown()
        return True

    def find_claim(self, keyword: str) -> Evidence:
        found = keyword.lower() in self._markdown_content.lower()
        snippet = None
        if found:
            idx = self._markdown_content.lower().find(keyword.lower())
            snippet = self._markdown_content[max(0, idx-100) : idx+300]
        return Evidence(goal=f"Claim: {keyword}", found=found, content=snippet,
                        location=str(self.pdf_path), rationale="Docling Scan", 
                        confidence=0.9 if found else 0.2)

def doc_analyst_node(state: AgentState):
    """🕵️ Protocol A.2: Documentation Analysis"""
    analyst = DocAnalyst(Path(state["pdf_path"]))
    if not analyst.ingest_pdf():
        return {"evidences": {"doc_detective": [Evidence(goal="PDF Ingestion", found=False, location="N/A", rationale="File missing", confidence=1.0)]}}
    
    claims = ["Fan-In / Fan-Out", "Dialectical Synthesis"]
    findings = [analyst.find_claim(c) for c in claims]
    return {"evidences": {"doc_detective": findings}}