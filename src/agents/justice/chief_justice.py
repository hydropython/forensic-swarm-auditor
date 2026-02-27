import os
from datetime import datetime
from src.core.state import AgentState

def chief_justice_node(state: AgentState):
    """
    ⚖️ The Chief Justice Node: Synthesizes verdict and generates a forensic MD report.
    Handles both Pydantic objects and Dicts to prevent 'AttributeError'.
    """
    opinions = state.get("opinions", [])
    evidences = state.get("refined_evidences", [])
    
    if not opinions:
        return {"final_report": "Error: No judicial opinions provided."}

    # 1. Weighted Scoring Logic (Protocol B)
    weights = {"Prosecutor": 0.4, "TechLead": 0.4, "Defense": 0.2}
    weighted_total = 0
    total_weight = 0
    for o in opinions:
        w = weights.get(o.judge, 0.33)
        weighted_total += (o.score * w)
        total_weight += w
    final_score = weighted_total / total_weight if total_weight > 0 else 0
    status = "ACCEPTED" if final_score >= 3.0 else "REJECTED"

    # 2. Build Judicial Table
    opinion_table = "| Judge | Score | Argument |\n| :--- | :--- | :--- |\n"
    for o in opinions:
        opinion_table += f"| {o.judge.upper()} | {o.score}/5 | {o.argument} |\n"

    # 3. 🛡️ ROBUST Evidence Table (Fixes the 500 Error)
    evidence_table = "| Agent | Found | Criterion | Rationale |\n| :--- | :--- | :--- | :--- |\n"
    for e in evidences:
        # Check if it's a dict (e.get) or a Pydantic object (getattr)
        is_dict = isinstance(e, dict)
        
        goal = e.get("goal", "Unknown") if is_dict else getattr(e, "goal", "Unknown")
        found = e.get("found", False) if is_dict else getattr(e, "found", False)
        rationale = e.get("rationale", "N/A") if is_dict else getattr(e, "rationale", "N/A")
        
        # We can detect the agent by the prefix in the goal or just label it 'Detective'
        status_icon = "✅ YES" if found else "❌ NO"
        evidence_table += f"| Detective | {status_icon} | {goal} | {rationale} |\n"

    # 4. Assemble Report
    report_content = f"""# 🛡️ SwarmAuditor v2.0 Forensic Record
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🏛️ COURTROOM VERDICT: {status}
**Final Weighted Score:** {final_score:.2f} / 5.0

### 👨‍⚖️ Judicial Opinions (Protocol B)
{opinion_table}

---

### 🔍 Forensic Evidence Table
{evidence_table}

---
#### 📋 Chief Justice Final Determination:
Evaluated under **Protocol B Forensic Precedents**.
"""

    # 5. Save to the path you specified
    save_path = r"D:\10 ACADAMY KIFIYA\TRP_Training\week 2\forensic-swarm-auditor\audit\report_onself_generated\final_audit_report.md"
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(report_content)
    except Exception as e:
        print(f"File Save Error: {e}")

    return {"final_report": report_content}