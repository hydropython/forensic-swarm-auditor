import os
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.core.engine import forensic_app

console = Console()

def run_pretty_audit(repo_path=".", doc_path="report.pdf"):
    console.print(Panel("[bold cyan]🛡️ FORENSIC SWARM AUDITOR[/bold cyan]\n[dim]Week 2: Architectural Verification[/dim]", expand=False))
    
    # 1. Start investigation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Swarm Agents Active...", total=None)
        
        os.environ["PYTHONPATH"] = "."
        initial_state = {
            "workspace_path": repo_path,
            "pdf_path": doc_path,
            "evidences": {},
            "opinions": [],
            "metadata": None
        }
        
        # Invoke LangGraph
        final_state = forensic_app.invoke(initial_state)

    # 2. Display Verdict
    scores = [op.score for op in final_state['opinions']]
    avg_score = sum(scores)/len(scores) if scores else 0
    verdict_color = "green" if avg_score >= 3.0 else "red"
    
    console.print(f"\n[bold]Audit Score:[/bold] [{verdict_color}]{avg_score:.2f}/5.0[/{verdict_color}]")
    console.print(f"[bold]Verdict:[/bold] [{verdict_color}]{'✅ ACCEPTED' if avg_score >= 3.0 else '❌ REJECTED'}[/{verdict_color}]\n")

    # 3. Evidence Table
    table = Table(title="🕵️ Forensic Evidence Ledger", show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Check")
    table.add_column("Rationale", style="italic")

    for agent, ev_list in final_state['evidences'].items():
        for ev in ev_list:
            status = "[green]PASS[/green]" if ev.found else "[red]FAIL[/red]"
            table.add_row(agent.split('_')[0].upper(), status, ev.goal, ev.rationale)

    console.print(table)

    # 4. Judicial Summary
    console.print("\n[bold cyan]⚖️ Judicial Deliberation Summary[/bold cyan]")
    for op in final_state['opinions']:
        console.print(Panel(f"[bold]{op.judge}[/bold] (Score: {op.score}/5)\n[dim]{op.argument}[/dim]", border_style="blue"))

if __name__ == "__main__":
    run_pretty_audit()