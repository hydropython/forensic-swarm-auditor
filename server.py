import os
import uvicorn
import tkinter as tk
from tkinter import filedialog
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from jinja2 import Template
from src.core.engine import forensic_app

app = FastAPI()

# --- THE INTERACTIVE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <title>Forensic Swarm Auditor</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #020617; color: #e2e8f0; }
        .glass { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        .tab-btn.active { border-bottom: 2px solid #22d3ee; color: #22d3ee; }
        .input-field { width: 100%; background: #020617; border: 1px solid #1e293b; border-radius: 0.75rem; padding: 0.75rem 1rem; outline: none; transition: border 0.2s; }
        .input-field:focus { border-color: #06b6d4; }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-5xl mx-auto">
        
        {% if not results %}
        <div class="max-w-2xl mx-auto mt-10">
            <h1 class="text-5xl font-black mb-4 text-white tracking-tighter text-center">🛡️ Swarm<span class="text-cyan-400">Auditor</span></h1>
            <p class="text-slate-400 text-center mb-10 text-lg">Input a Repo link and browse for your local PDF or Word doc.</p>
            
            <form action="/audit" method="post" class="glass p-8 rounded-3xl space-y-6">
                
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-500 mb-2">Repository (Link or Path)</label>
                    <input name="repo_path" type="text" placeholder="https://github.com/user/repo or ." value="." class="input-field">
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase text-slate-500 mb-2">Local Documentation (PDF, Word, or Text)</label>
                    <div class="flex gap-2">
                        <input id="doc_path" name="doc_path" type="text" placeholder="C:/Users/Documents/design_spec.docx" value="report.pdf" class="input-field">
                        <button type="button" onclick="pickFile()" class="bg-slate-800 px-4 rounded-xl hover:bg-slate-700 border border-slate-700 transition-colors" title="Browse Local File">📂</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-xs font-bold uppercase text-slate-500 mb-2">Audit Rubric</label>
                        <select name="rubric" class="input-field cursor-pointer">
                            <option value="week2">Week 2 Training (Core)</option>
                            <option value="prod_ready">Production Readiness</option>
                            <option value="security">Security Audit</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase text-slate-500 mb-2">LLM Model</label>
                        <select name="model_choice" class="input-field cursor-pointer">
                            <optgroup label="OpenAI">
                                <option value="gpt-4o">GPT-4o</option>
                                <option value="gpt-4o-mini">GPT-4o-Mini</option>
                            </optgroup>
                            <optgroup label="Google">
                                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                            </optgroup>
                        </select>
                    </div>
                </div>

                <button type="submit" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-4 rounded-xl transition-all uppercase tracking-widest mt-4 shadow-lg shadow-cyan-500/20">🚀 Initiate Analysis</button>
            </form>
        </div>
        {% endif %}

        {% if results %}
        <header class="flex justify-between items-end mb-10 border-b border-slate-800 pb-6">
            <div>
                <h1 class="text-3xl font-black text-white">AUDIT REPORT</h1>
                <p class="text-cyan-400 font-mono text-sm tracking-widest uppercase">Verdict: {{ verdict }} | Score: {{ score }}/5.0</p>
            </div>
            <a href="/" class="text-xs text-cyan-500 hover:text-white underline font-bold tracking-widest">RESET AUDIT</a>
        </header>

        <div class="flex gap-8 mb-8 border-b border-slate-800 text-sm font-bold uppercase tracking-wider">
            <button onclick="showTab('evidence')" id="btn-evidence" class="tab-btn pb-4 active">🕵️ Aggregator Evidence</button>
            <button onclick="showTab('judicial')" id="btn-judicial" class="tab-btn pb-4">⚖️ Judicial Opinions</button>
        </div>

        <div id="tab-evidence">
            <div class="glass rounded-3xl overflow-hidden mb-10">
                <table class="w-full text-left">
                    <thead class="bg-slate-800/50 text-[10px] uppercase text-slate-400 tracking-widest">
                        <tr><th class="p-4">Agent</th><th class="p-4 text-center">Status</th><th class="p-4">Criterion</th><th class="p-4">Rationale</th></tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {{ table_rows | safe }}
                    </tbody>
                </table>
            </div>
        </div>

        <div id="tab-judicial" class="hidden">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {{ judicial_cards | safe }}
            </div>
            <div class="mt-8 p-10 glass rounded-3xl text-center border-2 border-dashed border-cyan-500/20">
                <h2 class="text-4xl font-black {{ verdict_color }}">{{ verdict }}</h2>
            </div>
        </div>
        {% endif %}

    </div>

    <script>
        async function pickFile() {
            const response = await fetch('/browse-file');
            const data = await response.json();
            if(data.path) {
                document.getElementById('doc_path').value = data.path;
            }
        }

        function showTab(tabId) {
            document.getElementById('tab-evidence').classList.add('hidden');
            document.getElementById('tab-judicial').classList.add('hidden');
            document.getElementById('btn-evidence').classList.remove('active');
            document.getElementById('btn-judicial').classList.remove('active');
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).classList.add('active');
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
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    # UPDATED: Added Word (.doc, .docx) support to the file picker
    file_path = filedialog.askopenfilename(filetypes=[
        ("Documents", "*.pdf;*.doc;*.docx;*.txt;*.md"), 
        ("PDF Files", "*.pdf"),
        ("Word Files", "*.doc;*.docx"),
        ("All files", "*.*")
    ])
    root.destroy()
    return {"path": file_path}

@app.post("/audit", response_class=HTMLResponse)
async def run_audit(
    repo_path: str = Form(...), 
    doc_path: str = Form(...),
    rubric: str = Form(...),
    model_choice: str = Form(...)
):
    os.environ["PYTHONPATH"] = "."
    initial_state = {
        "workspace_path": repo_path, 
        "pdf_path": doc_path, 
        "evidences": {}, 
        "opinions": [], 
        "metadata": {"model": model_choice, "rubric": rubric}
    }
    
    res = forensic_app.invoke(initial_state)

    scores = [op.score for op in res['opinions']]
    avg = sum(scores)/len(scores) if scores else 0
    verdict = "ACCEPTED" if avg >= 3.0 else "REJECTED"
    v_color = "text-emerald-400" if avg >= 3.0 else "text-rose-500"

    rows = ""
    for agent, evs in res['evidences'].items():
        for e in evs:
            status = "✅" if e.found else "❌"
            rows += f"<tr class='hover:bg-slate-800/30'><td class='p-4 font-mono text-cyan-400'>{agent.split('_')[0].upper()}</td><td class='p-4 text-center'>{status}</td><td class='p-4 font-bold text-sm text-slate-200'>{e.goal}</td><td class='p-4 text-xs text-slate-500 italic'>{e.rationale}</td></tr>"

    cards = ""
    for op in res['opinions']:
        cards += f"<div class='glass p-6 rounded-3xl border-t-2 border-cyan-500/20'><h4 class='text-cyan-400 font-bold mb-1'>{op.judge}</h4><p class='text-[10px] text-slate-500 uppercase mb-4 text-slate-500'>Score: {op.score}/5</p><p class='text-sm text-slate-400'>{op.argument}</p></div>"

    return Template(HTML_TEMPLATE).render(
        results=True, score=f"{avg:.2f}", verdict=verdict, 
        verdict_color=v_color, table_rows=rows, judicial_cards=cards
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) # Changed from 8000 to 8001