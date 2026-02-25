from pypdf import PdfReader

def semantic_pdf_ingestion(pdf_path: str, chunk_size: int = 1500):
    """
    📄 Intelligent PDF Ingestion
    Chinks the rubric by logical sections to maintain criteria context.
    """
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    
    # Split by double newlines to preserve rubric paragraphs
    raw_chunks = full_text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for section in raw_chunks:
        if len(current_chunk) + len(section) < chunk_size:
            current_chunk += section + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = section + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks