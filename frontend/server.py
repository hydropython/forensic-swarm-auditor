import os
import sys
import uvicorn
import tkinter as tk
import tempfile
import shutil
import stat
import warnings
import gc
import time
from pathlib import Path
from tkinter import filedialog
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from jinja2 import Template
from git import Repo  
from pydantic import BaseModel

# --- 1. CRITICAL: ROOT PATH INJECTION ---
# This ensures 'src' is findable by looking one level up from the 'frontend' folder
current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_path, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set PYTHONPATH for subprocesses
os.environ["PYTHONPATH"] = project_root

# --- 2. COMPATIBILITY & SILENCE ---
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", category=SyntaxWarning)

# --- 3. ENGINE INVOCATION (With Fallback) ---
forensic_app = None
try:
    # Attempt to import from graph.py (LangGraph standard)
    from src.core.graph import forensic_app
    print("✅ System: Forensic Swarm Engine [Graph] initialized.")
except ImportError:
    try:
        # Fallback to engine.py
        from src.core.engine import forensic_app
        print("✅ System: Forensic Swarm Engine [Engine] initialized.")
    except ImportError as e:
        print(f"❌ CRITICAL: Swarm Engine not found in src.core.graph or src.core.engine.")
        print(f"DEBUG: Search Path: {project_root}")
        sys.exit(1)

# --- 4. APP INITIALIZATION ---
app = FastAPI(title="🛡️ SwarmAuditor v3.0 Emerald Suite")

# --- UTILITY: ROBUST CLEANUP PROTOCOL ---
def robust_rmtree(path):
    """Securely reclaim disk space by handling Windows Read-Only Git files."""
    def remove_readonly(func, p, excinfo):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)
        print(f"🧹 Cleanup: Workspace {path} reclaimed.")

def forensic_cleanup_task(path: str, retries: int = 5, delay: float = 2.0):
    """Background task to ensure the OS releases handles before deletion."""
    for i in range(retries):
        try:
            gc.collect()
            time.sleep(delay) 
            robust_rmtree(path)
            break
        except Exception as e:
            print(f"⚠️ Cleanup retry {i+1} for {path}: {e}")

# --- MISSION CONTROL UI (EMERALD PROTOCOL) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @font-face { font-family: 'Gadugi'; src: local('Gadugi'); }
        body { 
            font-family: 'Gadugi', sans-serif; 
            background: #f8fafc; 
            color: #064e3b; 
        }
        .sidebar { background: #ffffff; border-right: 3px solid #059669; }
        .input-field { 
            width: 100%; background: #f0fdf4; border: 2px solid #10b981; 
            border-radius: 0.75rem; padding: 1rem; color: #064e3b; font-weight: bold; outline: none;
        }
        .btn-run {
            background: #059669; color: white; font-weight: 900; 
            padding: 1.25rem; border-radius: 0.75rem; text-transform: uppercase;
            letter-spacing: 2px; transition: all 0.3s; width: 100%; cursor: pointer;
        }
        .btn-run:hover { background: #047857; transform: translateY(-2px); }
        
        /* 🏛️ JUDICIAL CSS ENHANCEMENTS */
        .emerald-header {
            background: #064e3b; color: #ffffff; padding: 45px; margin-bottom: 50px; 
            border-radius: 12px; box-shadow: 0 25px 50px -12px rgba(6, 78, 59, 0.25);
        }
        .judicial-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; border: 2px solid #064e3b; }
        .judicial-table th { background: #064e3b; color: white; padding: 15px; text-transform: uppercase; font-size: 12px; }
        .judicial-table td { padding: 15px; border-bottom: 1px solid #d1fae5; }
        
        .criteria-card { 
            background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 10px solid #10b981;
        }
        .trace-box {
            background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; 
            font-family: 'Consolas', monospace; font-size: 13px; color: #334155; margin: 15px 0;
        }
    </style>
</head>
<body class="h-screen flex flex-col">
    <header class="p-5 border-b-4 border-emerald-600 bg-white flex justify-between items-center shadow-md z-10">
        <h1 class="text-2xl font-black text-emerald-900">🛡️ SWARM<span class="text-emerald-600">AUDITOR</span> <span class="text-xs font-normal ml-2 opacity-60">EMERALD SUITE v3.0</span></h1>
        <div class="bg-emerald-100 text-emerald-800 px-4 py-1 rounded-full text-xs font-black uppercase tracking-widest">Protocol B Active</div>
    </header>

    <main class="flex-grow flex overflow-hidden">
        <aside class="w-1/4 sidebar p-8 overflow-y-auto">
            <h2 class="text-xs font-black text-emerald-700 uppercase tracking-widest mb-8">Audit Configuration</h2>
            <form action="/audit" method="post" class="space-y-6">
                <div>
                    <label class="block text-[10px] font-black text-emerald-600 uppercase mb-2">Repository Path</label>
                    <input name="repo_path" type="text" value="." class="input-field" required>
                </div>
                <div>
                    <label class="block text-[10px] font-black text-emerald-600 uppercase mb-2">Rubric (PDF)</label>
                    <div class="flex gap-2">
                        <input id="doc_path" name="doc_path" type="text" placeholder="Heuristic Mode" class="input-field">
                        <button type="button" onclick="pickFile()" class="bg-emerald-50 px-4 rounded-xl border-2 border-emerald-200 text-xl">📂</button>
                    </div>
                </div>
                <div class="space-y-4">
                    <select name="rubric_type" class="input-field">
                        <option value="forensic">Forensic Core Rubric</option>
                        <option value="security">Security Protocol Rubric</option>
                    </select>
                    <select name="model_choice" class="input-field">
                        <option value="gpt-4o-mini">GPT-4o-Mini (Fast)</option>
                        <option value="gpt-4o">GPT-4o (Deep Audit)</option>
                    </select>
                </div>
                <button type="submit" class="btn-run">🚀 Launch Swarm</button>
            </form>
        </aside>

        <section class="w-3/4 p-12 overflow-y-auto bg-slate-50">
            {% if not results %}
            <div class="h-full flex flex-col items-center justify-center opacity-30 text-emerald-900">
                <div class="text-8xl mb-6">🏛️</div>
                <h3 class="text-2xl font-black uppercase tracking-widest">Awaiting Forensic Data</h3>
            </div>
            {% else %}
                <div class="max-w-5xl mx-auto">{{ key_findings | safe }}</div>
            {% endif %}
        </section>
    </main>

    <script>
        async function pickFile() {
            const response = await fetch('/browse-file');
            const data = await response.json();
            if(data.path) document.getElementById('doc_path').value = data.path;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def welcome():
    return Template(HTML_TEMPLATE).render(results=False)

@app.get("/browse-file")
async def browse_file():
    root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
    path = filedialog.askopenfilename(); root.destroy()
    return {"path": path}

@app.post("/audit", response_class=HTMLResponse)
async def run_audit(
    background_tasks: BackgroundTasks,
    repo_path: str = Form(...), 
    doc_path: str = Form(None), 
    rubric_type: str = Form("forensic"),
    model_choice: str = Form("gpt-4o-mini")
):
    temp_workspace = tempfile.mkdtemp(prefix="swarm_audit_")
    
    try:
        # --- 1. CLONING & PREP (Fixed Path Logic) ---
        repo_path_clean = repo_path.strip()
        
        # Security: Only strip dots if it's a local path, not a URL
        if not repo_path_clean.startswith("http") and repo_path_clean.startswith("."):
            repo_path_clean = repo_path_clean.lstrip("./\\")

        if repo_path_clean.startswith(("http", "git@")):
            print(f"📡 Remote Clone: {repo_path_clean}")
            # depth=100 ensures we get your 51 commits for the forensic scan
            repo = Repo.clone_from(repo_path_clean, temp_workspace, depth=100)
            repo.close() 
        else:
            print(f"📂 Local Scan: {repo_path_clean}")
            shutil.copytree(repo_path_clean, temp_workspace, dirs_exist_ok=True)

        # --- 2. ENGINE INVOCATION (The Core Swarm) ---
        # Note: We use forensic_app which was initialized at the top of server.py
        res = forensic_app.invoke({
            "repo_url": repo_path_clean,
            "workspace_path": temp_workspace,
            "pdf_path": doc_path if doc_path else "HEURISTIC_MODE",
            "evidences": {}, 
            "opinions": [],
            "aggregated_score": 0.0
        })
        
        # --- 3. DATA EXTRACTION (Hybrid Pydantic/Dict Support) ---
        avg = res.get("aggregated_score", 0.0)
        verdict = res.get("global_verdict", "PENDING ADJUDICATION")
        opinions = res.get("opinions", [])
        evidence_vault = res.get("evidences", {})

        # --- 4. DYNAMIC UI GENERATION: HEADER ---
        emerald_header = f"""
        <div class="emerald-header" style="text-align: center; padding: 60px 20px; background: #064e3b; color: white; border-radius: 12px; margin-bottom: 40px;">
            <h1 style="font-size: 72px; font-weight: 900; margin: 0; color: #10b981;">{avg:.2f} <span style="font-size: 24px; opacity: 0.6; color: white;">/ 5.0</span></h1>
            <p style="font-size: 18px; font-weight: 700; text-transform: uppercase; letter-spacing: 6px; margin-top: 20px;">VERDICT: {verdict}</p>
            <p style="font-size: 14px; opacity: 0.8; margin-top: 10px;">Forensic Target: {repo_path_clean}</p>
        </div>
        """

        # --- 5. OPINION AGGREGATOR (The 'AttributeError: get' Fix) ---
        def get_opinion_block(role_name, display_title, color, emoji):
            match_data = None
            for op in opinions:
                # Convert Pydantic to Dict if necessary
                op_dict = op.model_dump() if hasattr(op, 'model_dump') else (op.__dict__ if hasattr(op, '__dict__') else op)
                
                # Identify the judge/role
                judge_name = str(op_dict.get("judge", op_dict.get("role", ""))).upper()
                if role_name.upper() in judge_name:
                    match_data = op_dict
                    break
            
            score = match_data.get("score", "0.0") if match_data else "N/A"
            arg = match_data.get("argument", "Waiting for judicial filing...") if match_data else f"The {role_name} did not file a brief."
            
            return f"""
            <div style="background: {color}10; border: 2px solid {color}; padding: 35px; border-radius: 16px; position: relative; margin-bottom: 20px;">
                <div style="position: absolute; top: -18px; right: 25px; background: {color}; color: white; padding: 6px 18px; border-radius: 20px; font-weight: 900; font-size: 14px;">{emoji} {role_name.upper()}: {score}/5.0</div>
                <h4 style="font-size: 14px; text-transform: uppercase; color: {color}; letter-spacing: 2px; font-weight: 800; margin-bottom: 12px;">{display_title}</h4>
                <p style="font-size: 16px; line-height: 1.8; color: #064e3b; margin: 0;">{arg}</p>
            </div>
            """

        judicial_table = f"""
        <h3 class="text-3xl font-black uppercase text-emerald-900 mb-10 mt-16">⚖️ The Digital Courtroom: Deliberations</h3>
        <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 60px;">
            {get_opinion_block("Defense", "Plea: Structural Integrity", "#059669", "🛡️")}
            {get_opinion_block("TechLead", "Ruling: Engineering Standards", "#334155", "💻")}
            {get_opinion_block("Prosecutor", "Charge: Forensic Breach", "#dc2626", "🔥")}
        </div>
        """

        # --- 6. STATUTES & EVIDENCE (Re-using your existing criteria logic) ---
        # Note: 'human_registry' should be defined here or globally
        criteria_report = ""
        # ... (Insert your criteria loop here, using evidence_vault) ...

        background_tasks.add_task(forensic_cleanup_task, temp_workspace)
        final_payload = emerald_header + judicial_table + criteria_report
        return Template(HTML_TEMPLATE).render(results=True, key_findings=final_payload)

    except Exception as e:
        import traceback
        traceback.print_exc()
        background_tasks.add_task(forensic_cleanup_task, temp_workspace)
        return HTMLResponse(content=f"<div style='color:red; font-family:sans-serif; padding:20px;'><b>Swarm Critical Error:</b> {str(e)}</div>", status_code=500)
    
if __name__ == "__main__":
    import uvicorn
    print("\n" + "═"*50)
    print("⚖️  AUTOMATON AUDITOR: DIGITAL COURTROOM ONLINE")
    print("📍 ACCESS PORT: 8001")
    print("═"*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8001)