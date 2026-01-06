"""Strategic planning agent for ESG monitoring tasks."""

import json
from typing import Dict, List, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class PlannerAgent:
    """Agent responsible for strategic planning and task decomposition."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Planner Agent.
        
        Args:
            config: Configuration dictionary for the planner agent
        """
        self.config = config
        self.agent_id = "planner_agent"
        self.status = "idle"
        logger.info(f"Initialized {self.agent_id}")

    def plan_monitoring_strategy(self, companies: List[str], esg_dimensions: List[str]) -> Dict[str, Any]:
        """
        Create a strategic plan for monitoring ESG risks.
        
        Args:
            companies: List of companies to monitor
            esg_dimensions: ESG dimensions to focus on (E, S, G)
            
        Returns:
            Strategy plan dictionary with tasks and priorities
        """
        self.status = "planning"
        plan = {
            "plan_id": "plan_001",
            "companies": companies,
            "dimensions": esg_dimensions,
            "tasks": self._decompose_tasks(companies, esg_dimensions),
            "priorities": self._assign_priorities(esg_dimensions),
        }
        self.status = "idle"
        logger.info(f"Strategy plan created: {plan['plan_id']}")
        return plan

    def _decompose_tasks(self, companies: List[str], dimensions: List[str]) -> List[Dict[str, Any]]:
        """Decompose monitoring into sub-tasks."""
        tasks = []
        for company in companies:
            for dimension in dimensions:
                task = {
                    "task_id": f"{company}_{dimension}_monitor",
                    "type": "monitor",
                    "company": company,
                    "dimension": dimension,
                    "priority": "high" if dimension == "E" else "medium",
                }
                tasks.append(task)
        return tasks

    def _assign_priorities(self, dimensions: List[str]) -> Dict[str, int]:
        """Assign priority scores to ESG dimensions."""
        return {
            "E": 10,  # Environmental
            "S": 8,   # Social
            "G": 9    # Governance
        }

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status
