import os
from typing import Dict, Any, List
# Syncing with the standardized state name to avoid ImportErrors
from src.core.state import AgentState 

def detective_node(state: AgentState) -> Dict[str, Any]:
    """
    The Lead Detective (formerly Aggregator): 
    Directively evaluates the findings of the Repo, Doc, and Vision agents
    to determine the final score and populate the Forensic Ledger.
    """
    evidences = state.get("evidences", {})
    
    # 1. Initialize Forensic Counters
    total_criteria = 0
    passed_criteria = 0
    detailed_rationale = []
    
    # 2. Mapping agent keys to their specific forensic weight
    agent_keys = ["repo_agent", "doc_agent", "vision_agent"]
    
    # We create a refined ledger specifically for the Report Generator
    refined_ledger = {}

    for agent in agent_keys:
        # Handling both list of findings or a single finding dict
        raw_data = evidences.get(agent, [])
        findings = raw_data if isinstance(raw_data, list) else [raw_data]
        
        # Filter out empty or None results
        findings = [f for f in findings if f]
        
        if not findings:
            # Log empty agent results
            refined_ledger[agent] = [{
                "found": False, 
                "criterion": "Scan", 
                "rationale": f"No artifacts found for {agent}."
            }]
            continue
            
        agent_refined_findings = []
        for item in findings:
            if not isinstance(item, dict): continue
            
            total_criteria += 1
            # Check for "found" status
            is_found = item.get("found", False)
            goal = item.get("goal") or item.get("criterion") or "Unknown Goal"
            
            if is_found:
                passed_criteria += 1
                detailed_rationale.append(f"✅ PASSED [{agent.upper()}]: {goal}")
            else:
                detailed_rationale.append(f"❌ FAILED [{agent.upper()}]: {goal}")

            # Standardizing finding structure for the markdown report
            agent_refined_findings.append({
                "found": is_found,
                "criterion": goal,
                "rationale": item.get("rationale") or item.get("reasoning") or "Verified by agent."
            })
        
        refined_ledger[agent] = agent_refined_findings

    # 3. Calculate Weighted Score (1.0 - 5.0 Scale)
    if total_criteria > 0:
        raw_ratio = passed_criteria / total_criteria
        # (ratio * 4) + 1 converts 0-1 to 1-5 scale
        calc_score = round((raw_ratio * 4) + 1, 2)
    else:
        calc_score = 1.0

    # 4. Final Mission Control Summary
    verdict = "ACCEPTED" if calc_score >= 3.0 else "REJECTED"
    summary = f"Audit complete. Processed {total_criteria} forensic criteria. "
    summary += f"Found {passed_criteria} matches across Repository, Documentation, and Vision layers."

    print(f"🕵️ Detective: Finalizing record with Score {calc_score}")

    return {
        "aggregated_score": calc_score, 
        "global_verdict": verdict,
        "evidences": refined_ledger,    # Reducer will merge this into the state
        "log": summary,                 # Added for graph logging
        "metadata": {
            "summary": summary,
            "detailed_logs": detailed_rationale,
            "total_count": total_criteria
        }
    }