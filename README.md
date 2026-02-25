# 🏛️ Forensic Swarm Auditor
> **Neuro-Symbolic Multi-Agent Judicial System for High-Integrity Code Auditing**

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Managed by uv](https://img.shields.io/badge/managed%20by-uv-arc.svg)](https://github.com/astral-sh/uv)
[![Orchestrated by LangGraph](https://img.shields.io/badge/orchestrated%20by-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Tracing](https://img.shields.io/badge/tracing-LangSmith-green.svg)](https://smith.langchain.com/)

## 📖 Overview
The **Forensic Swarm Auditor** is an advanced autonomous system designed to evaluate software repositories against complex PDF-based rubrics. By integrating **Structural AST Analysis** (Symbolic logic) with an **Adversarial Judicial Layer** (Neuro reasoning), the system provides verifiable, explainable audits that eliminate the subjectivity common in standard LLM code reviews.


## 📂 Detailed Project Structure
Following the modular architecture with dedicated infrastructure and core orchestration:

```text
forensic-swarm-auditor/
├── README.md
├── pyproject.toml
├── .env.example
├── main.py                     # CLI Entry Point
├── src/
│   ├── core/                   # ORCHESTRATION & SPECIFICATIONS
│   │   ├── engine.py           # LangGraph Workflow & Node Orchestration
│   │   ├── state.py            # Typed Graph State & Schema Contracts
│   │   └── config.py           # Pydantic V2 Settings Management
│   ├── agents/
│   │   ├── detectives/         # LAYER 1: DATA & EVIDENCE
│   │   │   ├── repo.py         # Git Forensics Node
│   │   │   └── analyst.py      # AST Structural Verification Node
│   │   ├── judges/             # LAYER 2: ADVERSARIAL TRIAL
│   │   │   ├── prosecutor.py   # Rubric Violation Analysis Node
│   │   │   └── defense.py      # Implementation Justification Node
│   │   └── chief_justice/      # LAYER 3: VERDICT SYNTHESIS
│   │       └── justice.py      # Final Score & Report Generation Node
│   ├── infrastructure/         # SYSTEM FOUNDATIONS
│   │   ├── sandbox.py          # Isolated Environment & Security Logic
│   │   └── observability.py    # LangSmith Tracing & Metric Exports
│   ├── tools/                  # REUSABLE AGENT CAPABILITIES
│   │   ├── repo_tools.py       # Git & AST Forensics Utility
│   │   └── doc_tools.py        # Semantic PDF/Rubric Ingestion
│   └── utils/
│       ├── formatters.py       # Markdown & PDF Report Export
│       └── logger.py           # Forensic Trace Logging
└── .github/
    └── workflows/              # CI/CD for Contract Validation
```


## 🏗️ Core Architecture (The Chimera Standard)
This project implements a neuro-symbolic approach to ensure every audit is grounded in concrete evidence:

### 🕵️ 1. The Detective Layer (Symbolic)
* **Structural Invariants**: Instead of simple regex searches, we utilize Python's **Abstract Syntax Tree (AST)** to verify the actual existence of classes, specific method signatures, and inheritance patterns.
* **Forensic Sandboxing**: Repositories are cloned and analyzed in isolated, temporary workspaces to ensure environment purity and safety.
* **Git Resilience**: Implements typed exceptions (`AuthError`, `RepoNotFoundError`) to handle infrastructure failures gracefully without crashing the swarm.

### ⚖️ 2. The Judicial Layer (Adversarial)
* **Prosecutor Agent**: Actively searches for non-compliance, technical debt, and rubric violations.
* **Defense Agent**: Contextualizes engineering decisions, identifying valid implementation patterns and workarounds.
* **Tech Lead Agent**: Evaluates the system for architectural maturity and best practices.

### 🏛️ 3. Synthesis Engine (Consensus)
* **Weighted Multi-Agent Consensus**: A final **Chief Justice** node performs a weighted synthesis of all judicial opinions, producing a deterministic score and an explainable verdict.

## 🚀 Setup & Installation

Follow these steps to initialize the forensic environment:

* **Step 1: Prerequisites**
    Ensure you have [uv](https://github.com/astral-sh/uv) installed for reproducible dependency management.
    ```vbash
    powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
    ```

* **Step 2: Clone & Sync**
    ```vbash
    git clone [https://github.com/your-username/forensic-swarm-auditor.git](https://github.com/your-username/forensic-swarm-auditor.git)
    cd forensic-swarm-auditor
    uv sync
    ```

* **Step 3: Configure Environment Variables**
    Create your local environment file:
    ```vbash
    cp .env.example .env
    ```
    Populate your `.env` file with the following required API keys:
    * **OPENAI_API_KEY**: Your primary judicial brain.
    * **GITHUB_TOKEN**: For authenticated repository access.
    * **LANGCHAIN_API_KEY**: For LangSmith forensic tracing.

## ⚖️ Execution

To run a full forensic audit against a target repository and a PDF rubric, execute the following command:

```vbash
uv run python main.py --repo "[https://github.com/example/target-repo](https://github.com/example/target-repo)" --rubric "./docs/rubric.pdf"
