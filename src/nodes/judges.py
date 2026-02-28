# src/nodes/judges.py
# FINAL BRIDGE: No logic loss, only export alignment.

from src.agents.judges.prosecutor import prosecutor
from src.agents.judges.defense import defense_node as defense
from src.agents.judges.tech_lead import tech_lead_node as tech_lead

# Now the graph finds: prosecutor, defense, and tech_lead
__all__ = ["prosecutor", "defense", "tech_lead"]