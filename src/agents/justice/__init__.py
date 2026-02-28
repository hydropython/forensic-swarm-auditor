# Import the actual logic from their sub-files
from src.agents.judges.prosecutor import prosecutor
from src.agents.judges.defense import defense_node as defense
from src.agents.judges.tech_lead import tech_lead_node as tech_lead
from src.agents.justice.chief_justice import chief_justice_node as chief_justice

# This list tells Python exactly what is available for export
__all__ = ["prosecutor", "defense", "tech_lead", "chief_justice"]