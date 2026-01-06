"""Main coordinator for the multi-agent ESG monitoring system."""

import asyncio
from typing import Dict, List, Any
from pathlib import Path

from agents import PlannerAgent, ExecutorAgent, ValidatorAgent
from portfolio import DummyPortfolio, RiskCalculator
from models import ESGScoringModel
from data import SyntheticDataGenerator
from utils import ConfigLoader, get_logger
from communication import RPCHandler

logger = get_logger(__name__)


class AgentCoordinator:
    """Coordinate multiple agents in the ESG monitoring system."""

    def __init__(self, config_path: str = "config/settings.yml"):
        """
        Initialize the Agent Coordinator.
        
        Args:
            config_path: Path to main configuration file
        """
        self.config = ConfigLoader.load_config(config_path)
        self.agent_configs = ConfigLoader.load_all_agent_configs("config/agent_configs")
        
        # Initialize agents
        self.planner = PlannerAgent(self.agent_configs.get("planner_config", {}))
        self.executor = ExecutorAgent(self.agent_configs.get("executor_config", {}))
        self.validator = ValidatorAgent(self.agent_configs.get("validator_config", {}))
        
        # Initialize other components
        self.portfolio = DummyPortfolio()
        self.risk_calculator = RiskCalculator(self.portfolio)
        self.esg_scorer = ESGScoringModel()
        self.data_generator = SyntheticDataGenerator()
        
        # Initialize RPC handlers
        self.planner_rpc = RPCHandler("planner")
        self.executor_rpc = RPCHandler("executor")
        self.validator_rpc = RPCHandler("validator")
        
        self._register_rpc_methods()
        
        logger.info("Initialized Agent Coordinator")

    def _register_rpc_methods(self):
        """Register RPC methods for each agent."""
        # Planner RPC methods
        self.planner_rpc.register_method(
            "create_strategy", 
            self.planner.plan_monitoring_strategy
        )
        
        # Executor RPC methods
        self.executor_rpc.register_method(
            "execute_task",
            self.executor.execute_task
        )
        
        # Validator RPC methods
        self.validator_rpc.register_method(
            "validate_result",
            self.validator.validate_result
        )
        
        logger.info("Registered RPC methods")

    async def run_monitoring_cycle(self, companies: List[str] = None, dimensions: List[str] = None) -> Dict[str, Any]:
        """
        Run a complete ESG monitoring cycle.
        
        Args:
            companies: List of companies to monitor
            dimensions: ESG dimensions to monitor
            
        Returns:
            Results of the monitoring cycle
        """
        if not companies:
            companies = [c["name"] for c in self.portfolio.companies[:3]]
        
        if not dimensions:
            dimensions = ["E", "S", "G"]
        
        logger.info(f"Starting monitoring cycle for {companies} - dimensions {dimensions}")
        
        # Step 1: Planning
        logger.info("Step 1: Planning")
        plan = self.planner.plan_monitoring_strategy(companies, dimensions)
        
        # Step 2: Execution
        logger.info("Step 2: Execution")
        execution_results = []
        for task in plan["tasks"][:5]:  # Execute first 5 tasks for demo
            result = self.executor.execute_task(task)
            execution_results.append(result)
        
        # Step 3: Validation
        logger.info("Step 3: Validation")
        validation_results = []
        for result in execution_results:
            validation = self.validator.validate_result(result)
            validation_results.append(validation)
        
        # Step 4: ESG Scoring
        logger.info("Step 4: ESG Scoring")
        incidents = self.data_generator.generate_incidents(count=5)
        scoring_results = self.esg_scorer.batch_score(incidents)
        
        # Step 5: Risk Assessment
        logger.info("Step 5: Risk Assessment")
        portfolio_risk = self.risk_calculator.calculate_portfolio_risk()
        
        cycle_result = {
            "cycle_id": "cycle_001",
            "plan": plan,
            "execution_results": execution_results,
            "validation_results": validation_results,
            "scoring_results": scoring_results,
            "portfolio_risk": portfolio_risk,
            "status": "completed",
        }
        
        logger.info("Monitoring cycle completed")
        return cycle_result

    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get current portfolio status."""
        return {
            "portfolio": self.portfolio.get_portfolio_summary(),
            "risk_assessment": self.risk_calculator.calculate_portfolio_risk(),
            "agent_status": {
                "planner": self.planner.get_status(),
                "executor": self.executor.get_status(),
                "validator": self.validator.get_status(),
            },
        }

    def generate_test_data(self, incidents: int = 100, news: int = 50) -> Dict[str, Any]:
        """Generate synthetic test data."""
        return {
            "incidents": self.data_generator.generate_incidents(count=incidents),
            "news": self.data_generator.generate_news_data(count=news),
        }

    def get_configuration(self) -> Dict[str, Any]:
        """Get current system configuration."""
        return {
            "main_config": self.config,
            "agent_configs": self.agent_configs,
        }


async def main():
    """Main entry point."""
    print("=" * 60)
    print("ESG Monitor - Multi-Agent System")
    print("=" * 60)
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    # Display configuration
    print("\n📋 System Configuration:")
    config = coordinator.get_configuration()
    print(f"  - Planner Agent: {'Enabled' if config['main_config'].get('agents', {}).get('enable_planner') else 'Disabled'}")
    print(f"  - Executor Agent: {'Enabled' if config['main_config'].get('agents', {}).get('enable_executor') else 'Disabled'}")
    print(f"  - Validator Agent: {'Enabled' if config['main_config'].get('agents', {}).get('enable_validator') else 'Disabled'}")
    
    # Display portfolio
    print("\n📊 Portfolio Status:")
    portfolio = coordinator.portfolio.get_portfolio_summary()
    print(f"  - Total Companies: {portfolio['total_companies']}")
    print(f"  - Sectors: {', '.join(portfolio['sectors'])}")
    
    # Run monitoring cycle
    print("\n🔄 Running Monitoring Cycle...")
    print("-" * 60)
    
    try:
        result = await coordinator.run_monitoring_cycle()
        
        print("\n✅ Monitoring Cycle Results:")
        print(f"  - Tasks Executed: {len(result['execution_results'])}")
        print(f"  - Validations Passed: {len(result['validation_results'])}")
        print(f"  - Incidents Scored: {len(result['scoring_results'])}")
        
        portfolio_risk = result['portfolio_risk']
        print(f"\n⚠️  Portfolio Risk Assessment:")
        print(f"  - Average Overall Risk: {portfolio_risk.get('average_overall_risk', 'N/A'):.2f}")
        print(f"  - High Risk Companies: {portfolio_risk.get('companies_at_high_risk', 0)}")
        print(f"  - Medium Risk Companies: {portfolio_risk.get('companies_at_medium_risk', 0)}")
        print(f"  - Low Risk Companies: {portfolio_risk.get('companies_at_low_risk', 0)}")
        
    except Exception as e:
        logger.error(f"Error during monitoring cycle: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Coordinator shutdown complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
