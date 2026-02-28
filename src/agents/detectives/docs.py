import os
import fitz
import re

def doc_analyst(state):
    """
    Sovereign Doc Analyst.
    Clears ID-06 (Theoretical Depth) and ID-07 (Host Analysis).
    """
    pdf_path = state.get("pdf_path", "")
    workspace_path = state.get("workspace_path", ".")
    evidence_list = []
    
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        text = " ".join([page.get_text() for page in doc])
        
        # --- ID-06: THEORETICAL DEPTH ---
        # We look for the "Why" behind the swarm
        keywords = ["Metacognition", "Dialectical Synthesis", "Fan-In", "State Synchronization"]
        found_theory = []
        for word in keywords:
            match = re.search(fr"([^.]*?{word}[^.]*\.)", text, re.IGNORECASE)
            if match:
                found_theory.append(match.group(0).strip())

        evidence_list.append({
            "found": len(found_theory) > 0,
            "goal": "Theoretical Depth",
            "rationale": f"VERIFIED: Captured {len(found_theory)} theoretical markers including: {', '.join(keywords[:2])}." if found_theory else "FAILED: Design doc lacks architectural theory."
        })

        # --- ID-07: HOST ANALYSIS (HALLUCINATION CHECK) ---
        # 1. Extract mentioned paths from PDF
        found_paths = list(set(re.findall(r'[a-zA-Z0-9_/]+\.py', text)))
        real_count = 0
        hallucinations = []

        # 2. Check reality against the actual physical workspace
        for p in found_paths:
            full_path = os.path.join(workspace_path, p.replace("/", os.sep))
            if os.path.exists(full_path):
                real_count += 1
            else:
                hallucinations.append(p)

        status = len(found_paths) > 0 and len(hallucinations) == 0
        evidence_list.append({
            "found": status,
            "goal": "Host Analysis Accuracy",
            "rationale": f"VERIFIED: All {real_count} paths mentioned in PDF exist in the workspace." if status else f"FAILED: Detected {len(hallucinations)} path hallucinations (e.g., {hallucinations[0] if hallucinations else 'N/A'})."
        })
            
    return {"evidences": {"doc_agent": evidence_list}}