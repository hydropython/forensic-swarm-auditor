import os
import uvicorn
import tkinter as tk
import tempfile
import shutil
import stat
import warnings
from pathlib import Path
from tkinter import filedialog
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from jinja2 import Template
from git import Repo  

# --- COMPATIBILITY & ENV SETUP ---
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
os.environ["PYTHONPATH"] = os.getcwd()

from src.core.engine import forensic_app

app = FastAPI()

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# --- SINGLE SCREEN MISSION CONTROL ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <title>SwarmAuditor Mission Control</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #f0f9f6; color: #166534; overflow-x: hidden; }
        .glass-card { background: #ffffff; border: 1px solid #d1fae5; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.08); }
        .input-field { width: 100%; background: #fdfdfd; border: 1px solid #e0e7ff; border-radius: 0.75rem; padding: 0.75rem 1rem; outline: none; }
        .input-field:focus { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1); }
        .status-badge { padding: 2px 8px; border-radius: 99px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #d1fae5; border-radius: 10px; }
    </style>
</head>
<body class="h-screen flex flex-col">

    <header class="p-4 border-b border-emerald-100 flex justify-between items-center bg-white">
        <h1 class="text-2xl font-black tracking-tighter text-emerald-950">🛡️ Swarm<span class="text-emerald-600">Auditor</span> <span class="text-xs font-normal text-emerald-400 ml-2">v2.0 Forensic Suite</span></h1>
        <div class="flex gap-4">
            <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-100 uppercase">System Ready</span>
        </div>
    </header>

    <main class="flex-grow flex overflow-hidden">
        
        <aside class="w-1/3 p-6 border-r border-emerald-100 overflow-y-auto bg-slate-50/30">
            <h2 class="text-xs font-black text-emerald-800 uppercase tracking-widest mb-6">Audit Parameters</h2>
            
            <form action="/audit" method="post" class="space-y-6">
                <div>
                    <label class="block text-[10px] font-bold text-emerald-700 uppercase mb-2">Target Repository</label>
                    <input name="repo_path" type="text" placeholder="URL or Local Path" value="." class="input-field text-sm">
                </div>

                <div>
                    <label class="block text-[10px] font-bold text-emerald-700 uppercase mb-2">Evaluation Rubric (PDF)</label>
                    <div class="flex gap-2">
                        <input id="doc_path" name="doc_path" type="text" placeholder="Select file..." class="input-field text-sm" required>
                        <button type="button" onclick="pickFile()" class="bg-emerald-50 text-emerald-700 px-3 rounded-xl border border-emerald-200 hover:bg-emerald-100">📂</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-4">
                    <div>
                        <label class="block text-[10px] font-bold text-emerald-700 uppercase mb-2">Rubric Type</label>
                        <select name="rubric" class="input-field text-sm">
                            <option value="forensic">Forensic Rubric (Core)</option>
                            <option value="peer_eval">Peer Evaluation Rubric</option>
                            <option value="my_interest">My Interest Rubric</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-emerald-700 uppercase mb-2">Auditor Model</label>
                        <select name="model_choice" class="input-field text-sm">
                            <optgroup label="Google Gemini">
                                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                            </optgroup>
                            <optgroup label="OpenAI">
                                <option value="gpt-4o">GPT-4o</option>
                                <option value="gpt-4o-mini">GPT-4o-Mini</option>
                            </optgroup>
                            <optgroup label="Anthropic">
                                <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                            </optgroup>
                            <optgroup label="Meta (Llama)">
                                <option value="llama-3.1-405b">Llama 3.1 405b</option>
                                <option value="llama-3.1-70b">Llama 3.1 70b</option>
                            </optgroup>
                            <optgroup label="Local">
                                <option value="ollama-llama3">Ollama: Llama3</option>
                            </optgroup>
                        </select>
                    </div>
                </div>

                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-black py-4 rounded-xl transition-all uppercase tracking-widest shadow-lg shadow-emerald-500/20 text-sm">
                    🚀 Run Forensic Audit
                </button>
            </form>
        </aside>

        <section class="w-2/3 p-6 overflow-y-auto bg-white">
            {% if not results %}
            <div class="h-full flex flex-col items-center justify-center text-center opacity-40">
                <div class="text-6xl mb-4">🕵️‍♂️</div>
                <h3 class="text-lg font-bold text-emerald-950">Awaiting Investigation</h3>
                <p class="text-sm text-emerald-700">Configure parameters on the left to initiate the swarm.</p>
            </div>
            {% else %}
            
            <div class="flex justify-between items-center mb-8">
                <div>
                    <span class="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">Global Verdict</span>
                    <h2 class="text-4xl font-black text-emerald-950 tracking-tighter leading-none">{{ verdict }}</h2>
                </div>
                <div class="text-right">
                    <span class="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">Aggregated Score</span>
                    <div class="text-4xl font-black text-emerald-900 leading-none">{{ score }}<span class="text-lg text-emerald-400">/5.0</span></div>
                </div>
            </div>

            <h3 class="text-xs font-black text-emerald-800 uppercase tracking-widest mb-4">Forensic Evidence Table</h3>
            <div class="glass-card rounded-2xl overflow-hidden mb-8">
                <table class="w-full text-left text-sm">
                    <thead class="bg-emerald-50 text-[10px] uppercase text-emerald-800 font-bold border-b border-emerald-100">
                        <tr><th class="p-4">Agent</th><th class="p-4 text-center">Found</th><th class="p-4">Criterion</th><th class="p-4">Rationale</th></tr>
                    </thead>
                    <tbody class="divide-y divide-emerald-50">
                        {{ table_rows | safe }}
                    </tbody>
                </table>
            </div>

            <h3 class="text-xs font-black text-emerald-800 uppercase tracking-widest mb-4">Judicial Opinions</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                {{ judicial_cards | safe }}
            </div>
            
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
async def run_audit(repo_path: str = Form(...), doc_path: str = Form(...), rubric: str = Form(...), model_choice: str = Form(...)):
    target_workspace = repo_path.strip()
    temp_dir = None
    if target_workspace.startswith("http"):
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(target_workspace, temp_dir)
        target_workspace = temp_dir

    res = forensic_app.invoke({
        "workspace_path": target_workspace, "pdf_path": doc_path, 
        "evidences": {}, "opinions": [], 
        "metadata": {"model": model_choice, "rubric": rubric}
    })

    if temp_dir: shutil.rmtree(temp_dir, onerror=remove_readonly)

    scores = [op.score for op in res.get('opinions', [])]
    avg = sum(scores)/len(scores) if scores else 0
    verdict = "ACCEPTED" if avg >= 3.0 else "REJECTED"

    rows = ""
    for agent, evs in res.get('evidences', {}).items():
        for e in evs:
            status = "<span class='status-badge bg-emerald-100 text-emerald-700'>YES</span>" if e.found else "<span class='status-badge bg-rose-100 text-rose-700'>NO</span>"
            rows += f"<tr class='hover:bg-emerald-50/50'><td class='p-4 font-mono text-[10px] text-emerald-600 font-bold'>{agent.split('_')[0].upper()}</td><td class='p-4 text-center'>{status}</td><td class='p-4 font-bold text-emerald-950 text-xs'>{e.goal}</td><td class='p-4 text-[11px] text-emerald-700 leading-relaxed'>{e.rationale}</td></tr>"

    cards = ""
    for op in res.get('opinions', []):
        cards += f"<div class='glass-card p-4 rounded-xl border-t-2 border-emerald-500'><h4 class='text-emerald-800 font-bold text-xs'>{op.judge}</h4><p class='text-[10px] text-emerald-500 mb-2 uppercase'>Score: {op.score}/5</p><p class='text-[11px] text-emerald-900 italic'>\\\"{op.argument}\\\"</p></div>"

    return Template(HTML_TEMPLATE).render(results=True, score=f"{avg:.2f}", verdict=verdict, table_rows=rows, judicial_cards=cards)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)