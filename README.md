# 🏛️ Automaton Auditor: Digital Courtroom

## Setup
1. Install `uv`: `pip install uv`
2. Sync dependencies: `uv sync`
3. Setup environment: Create `.env` with `GOOGLE_API_KEY`

## Usage
To run the Forensic Detectives against a target repository:
```bash
python main.py --repo [https://github.com/user/target-repo](https://github.com/user/target-repo) --pdf reports/target.pdf
