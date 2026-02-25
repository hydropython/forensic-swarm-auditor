from pathlib import Path
from docling.document_converter import DocumentConverter
from src.core.state import Evidence

class DocAnalyst:
    """
    🕵️ The Context Detective: Parses PDFs and extracts specific claims
    to compare against the structural reality found in the repo.
    """
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()
        self._content = None

    def ingest_pdf(self):
        """📄 Converts PDF to a structured format for analysis."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found at {self.pdf_path}")
        
        result = self.converter.convert(str(self.pdf_path))
        # Exporting to markdown provides a clean structure for the LLM
        self._content = result.document.export_to_markdown()

    def extract_claim(self, goal: str) -> Evidence:
        """🔍 Search the document for specific architectural claims."""
        # In a full RAG implementation, we would use embeddings here.
        # For our 'RAG-lite' version, we'll focus on structured parsing.
        
        found = goal.lower() in self._content.lower() if self._content else False
        
        return Evidence(
            goal=goal,
            found=found,
            content=self._content[:500] if found else None, # Return a snippet
            location=str(self.pdf_path),
            rationale=f"Searched document for: {goal}",
            confidence=0.8 if found else 0.2
        )