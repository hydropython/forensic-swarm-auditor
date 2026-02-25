# Automaton Auditor: Multi-Agent Digital Courtroom

Automaton Auditor is a high-fidelity **LangGraph** orchestration engine designed to evaluate the structural and conceptual integrity of AI-generated repositories. By implementing a **Dialectical Synthesis** architecture, the system isolates objective forensic discovery from subjective judicial deliberation.

---

## Architectural Topology

The system is built on a **Fan-Out/Fan-In** orchestration model. As of the Phase 2 milestone, the **Forensic Detective Layer** is fully implemented, allowing for parallel interrogation of code, documentation, and visual artifacts.

### 🧬 State Management & Reducers
The system's "Constitution" is defined in `src/state.py`. We utilize **Reducers** to handle concurrent agent outputs without race conditions:
* **`operator.ior` (In-place OR):** Merges forensic evidence dictionaries from multiple agents into the global state.
* **`operator.add`:** Accumulates judicial opinions into a unified consensus stream for final synthesis.



---

## Layer 1: Forensic Detectives (Phase 2)

Each detective node is a specialized agent that interrogates a specific artifact using high-precision tooling:

1. **RepoInvestigator (The AST Specialist):** - **Method:** Traverses the Abstract Syntax Tree (AST) to verify functional wiring.
   - **Verification:** Validates Typed State inheritance (`BaseModel`) and structural parallelism in `graph.py`.
2. **DocAnalyst (The Context Hunter):** - **Method:** Uses RAG-lite to verify documentation claims.
   - **Verification:** Cross-references cited file paths against physical disk telemetry to flag architectural hallucinations.
3. **VisionInspector (The Flow Auditor):** - **Status:** Integrated for Phase 3 multimodal diagram verification via Gemini Pro Vision.


---

## 🛠️ Infrastructure

### 1. Dependency Management
This project utilizes **uv** for reproducible, sub-second dependency resolution.
```bash
pip install uv
uv sync

