"""Test suite for agent interactions and communication."""

import unittest
from agents import PlannerAgent, ExecutorAgent, ValidatorAgent
from communication import RPCHandler, MessageProtocol
from utils import get_logger

logger = get_logger(__name__)


class TestAgentInteractions(unittest.TestCase):
    """Test agent interactions and task workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.planner_config = {
            "agent_id": "test_planner",
            "planning_horizon": 30,
        }
        self.executor_config = {
            "agent_id": "test_executor",
            "parallel_tasks": 3,
        }
        self.validator_config = {
            "agent_id": "test_validator",
            "validation_threshold": 0.8,
        }
        
        self.planner = PlannerAgent(self.planner_config)
        self.executor = ExecutorAgent(self.executor_config)
        self.validator = ValidatorAgent(self.validator_config)

    def test_planner_creates_strategy(self):
        """Test that planner agent creates valid strategy."""
        companies = ["TechCorp", "GreenEnergy"]
        dimensions = ["E", "S", "G"]
        
        plan = self.planner.plan_monitoring_strategy(companies, dimensions)
        
        self.assertIn("plan_id", plan)
        self.assertEqual(plan["companies"], companies)
        self.assertGreater(len(plan["tasks"]), 0)

    def test_executor_executes_task(self):
        """Test that executor agent completes tasks."""
        task = {
            "task_id": "TEST_001",
            "type": "monitor",
            "company": "TestCorp",
            "dimension": "E",
        }
        
        result = self.executor.execute_task(task)
        
        self.assertEqual(result["status"], "completed")
        self.assertIn("data", result)
        self.assertIn("metrics", result)

    def test_validator_validates_result(self):
        """Test that validator agent validates results."""
        result = {
            "task_id": "TEST_001",
            "status": "completed",
            "data": {"company": "TestCorp"},
            "metrics": {
                "risk_score": 6.5,
                "materiality_score": 7.2,
                "severity": 8.0,
            },
        }
        
        validation = self.validator.validate_result(result)
        
        self.assertIn("quality_score", validation)
        self.assertIn("checks", validation)
        self.assertGreater(len(validation["checks"]), 0)

    def tearDown(self):
        """Clean up after tests."""
        logger.info("Test fixtures cleaned up")


if __name__ == "__main__":
    unittest.main()
