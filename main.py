import os
import shutil
import stat
import sys
from datetime import datetime
from src.core.engine import forensic_app

def remove_readonly(func, path, _):
    """🛠️ Windows Fix: Resets file permissions for .git folders."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def generate_professional_markdown(report_data, evidences):
    """
    Constructs a high-fidelity audit report with a Forensic Evidence Ledger.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Header & Meta
    md = f"# ⚖️ Forensic Swarm Audit Report\n"
    md += f"**Audit Timestamp:** {timestamp}  \n"
    md += f"**Framework:** LangGraph Hierarchical Swarm  \n\n"
    md += "---\n\n"

    # Executive Summary Section
    if isinstance(report_data, str):
        md += report_data
    else:
        md += f"## 🏆 Final Verdict: {getattr(report_data, 'overall_score', 'N/A')}/5\n"
        md += f"### Executive Summary\n{getattr(report_data, 'executive_summary', 'No summary provided.')}\n\n"
        
        md += "## 🔍 Criterion Breakdown\n"
        md += "| Criterion | Score | Dissent/Nuance | Remediation |\n"
        md += "| :--- | :---: | :--- | :--- |\n"
        for crit in getattr(report_data, 'criteria', []):
            md += f"| {crit.dimension_name} | {crit.final_score}/5 | {crit.dissent_summary or 'Unanimous'} | {crit.remediation} |\n"

    # 🕵️ Forensic Evidence Ledger
    md += "\n---\n\n## 🕵️ Forensic Evidence Ledger\n"
    md += "The following raw artifacts were collected by the Detective Layer and verified by the Clerk Aggregator.\n\n"
    md += "| # | Status | Artifact/Goal | Source | Rationale |\n"
    md += "| :--- | :---: | :--- | :--- | :--- |\n"
    
    for i, e in enumerate(evidences, 1):
        def get_val(obj, attr, default=None):
            if isinstance(obj, dict): return obj.get(attr, default)
            return getattr(obj, attr, default)

        status = "✅" if get_val(e, "found") else "❌"
        goal = get_val(e, "goal") or get_val(e, "dimension_id") or "Unknown"
        src = get_val(e, "location") or "N/A"
        rat = str(get_val(e, "rationale") or "")[:100].replace("\n", " ")
        
        md += f"| {i} | {status} | {goal} | `{src}` | {rat}... |\n"

    md += f"\n\n---\n*Report generated automatically by Gemini-Powered Forensic Swarm Auditor.*"
    return md

def run_audit():
    print("🚀 Initializing Professional Forensic Audit Swarm...")
    
    repo_url = "https://github.com/hydropython/project-chimera-agent-factory"
    rubric_path = r"D:\10 ACADAMY KIFIYA\TRP_Training\week 2\Interim_Report_Kidist_Demessie_Wk2_02-24-2026.docx"
    workspace = os.path.join(os.getcwd(), "temp_audit_workspace")

    if os.path.exists(workspace):
        shutil.rmtree(workspace, onerror=remove_readonly)
    os.makedirs(workspace, exist_ok=True)

    initial_state = {
        "repo_url": repo_url,
        "pdf_path": rubric_path,
        "workspace_path": workspace,
        "rubric_dimensions": [], "evidences": {}, "refined_evidences": [],
        "opinions": [], "final_report": None,
        "metadata": {"git_log": [], "has_uv_lock": False, "version": "1.0.0"}
    }

    final_accumulated_state = initial_state

    try:
        print("🕵️ Deploying Detective and Judicial Agents...")
        for output in forensic_app.stream(initial_state, config={"recursion_limit": 35}):
            for node_name, state_update in output.items():
                print(f"  [COMPLETED]: {node_name}")
                final_accumulated_state.update(state_update)

        # 1. Inspect Evidence (Terminal)
        evidences = final_accumulated_state.get("refined_evidences", [])
        print(f"\n📊 Forensic Analysis Complete: {len(evidences)} artifacts secured.")

        # 2. Render Professional Report
        report_data = final_accumulated_state.get("final_report")
        if report_data:
            full_md = generate_professional_markdown(report_data, evidences)
            
            output_dir = "audit/report_onself_generated"
            os.makedirs(output_dir, exist_ok=True)
            report_file = os.path.join(output_dir, "final_audit_report.md")

            with open(report_file, "w", encoding="utf-8") as f:
                f.write(full_md)
            
            print(f"\n✅ Professional Audit Report Rendered to: {report_file}")
            print(f"⚖️ Final Verdict Score: {getattr(report_data, 'overall_score', 'N/A')}/5")

    except Exception as e:
        print(f"\n❌ Swarm Critical Failure: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    run_audit()