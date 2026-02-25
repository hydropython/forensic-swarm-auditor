from pathlib import Path
from docling.document_converter import DocumentConverter
from src.core.state import Evidence

class DocAnalyst:
    """
    🕵️ The Context Detective: Parses PDFs to extract architectural claims.
    """
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()
        self._markdown_content: str = ""

    def ingest_pdf(self):
        """📄 Converts the PDF into a structured Markdown format."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Missing PDF at: {self.pdf_path}")
        
        # Convert PDF to Markdown to keep headers and structure intact
        result = self.converter.convert(str(self.pdf_path))
        self._markdown_content = result.document.export_to_markdown()

    def find_claim(self, keyword: str) -> Evidence:
        """🔍 Scans the Markdown for specific technical claims."""
        # Simple RAG-lite: Check for keyword presence and extract context
        found = keyword.lower() in self._markdown_content.lower()
        
        # Logic to grab a small snippet around the keyword if found
        snippet = None
        if found:
            start_idx = self._markdown_content.lower().find(keyword.lower())
            snippet = self._markdown_content[max(0, start_idx-100) : start_idx+300]

        return Evidence(
            goal=f"Check for claim: {keyword}",
            found=found,
            content=snippet,
            location=str(self.pdf_path),
            rationale=f"Performed structural scan for '{keyword}' in PDF.",
            confidence=0.9 if found else 0.1
        )