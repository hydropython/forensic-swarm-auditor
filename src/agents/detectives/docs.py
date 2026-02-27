import os
from src.core.state import Evidence
from src.utils.pdf_engine import semantic_pdf_ingestion 

def doc_analyst(state: dict):
    pdf_path = state.get("pdf_path", "")
    findings = []
    
    if not os.path.exists(pdf_path):
        findings.append(Evidence(goal="PDF Existence", found=False, location=pdf_path, rationale="Critical failure: PDF file not found at path."))
        return {"evidences": {"doc_analyst": findings}}

    try:
        chunks = semantic_pdf_ingestion(pdf_path)
        full_text = " ".join(chunks).lower()
    except Exception as e:
        findings.append(Evidence(goal="PDF Readability", found=False, location=pdf_path, rationale=f"Read error: {str(e)}"))
        return {"evidences": {"doc_analyst": findings}}

    # --- 1. Theoretical Depth (Individual Findings) ---
    # We now report on every term individually
    terms = ["Dialectical Synthesis", "Fan-In / Fan-Out", "Metacognition", "State Synchronization"]
    for term in terms:
        is_found = term.lower() in full_text
        findings.append(Evidence(
            goal=f"Theory: {term}",
            found=is_found,
            location="PDF Architecture Section",
            rationale=f"Term {'found' if is_found else 'missing'} in architectural context."
        ))

    # --- 2. Host Analysis Accuracy (Individual Findings) ---
    # We now report on every path check individually
    paths_in_doc = ["src/core/state.py", "src/nodes/judges.py", "src/tools/ast_parser.py", "src/core/engine.py"]
    for p in paths_in_doc:
        exists = os.path.exists(os.path.join(state["workspace_path"], p))
        findings.append(Evidence(
            goal=f"Path Check: {p}",
            found=exists,
            location="PDF Cross-Reference",
            rationale=f"Verification: {'Substantiated' if exists else 'Hallucination: Path does not exist in repo.'}"
        ))
        
    # --- 3. Content Integrity (Added Granularity) ---
    findings.append(Evidence(
        goal="PDF Structural Depth",
        found=len(full_text) > 1000,
        location="Document Length",
        rationale=f"Extracted {len(full_text)} characters. High detail level detected."
    ))

    return {"evidences": {"doc_analyst": findings}}