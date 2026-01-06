import yaml, csv
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.logger import get_logger
import os
import pandas as pd # Using pandas for easier CSV handling

logger = get_logger(__name__)

class PlannerAgent:
    """Agent responsible for strategic planning based on user queries and company data."""

    def __init__(self, config_path: str = "config/agent_configs/planner_config.yml"):
        """
        Initialize the Planner Agent by loading its YAML configuration.
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.agent_id = "planner_agent"
        self.status = "idle"
        self.companies_df = self._load_companies_data() # Load the sample data
        logger.info(f"Initialized {self.agent_id} with config from {config_path}")

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration from a YAML file."""
        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from {path}")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise

    def _load_companies_data(self) -> pd.DataFrame:
        """Load company data from the sample CSV file."""
        csv_path = "data/companies.csv"
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded company data from {csv_path}, shape: {df.shape}")
            return df
        except FileNotFoundError:
            logger.error(f"Companies CSV file not found: {csv_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"Companies CSV file is empty: {csv_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading companies CSV: {e}")
            raise

    def plan_monitoring_strategy(self, user_query: str) -> Dict[str, Any]:
        """
        Create a strategic plan for monitoring ESG risks based on a user query and company data.
        """
        self.status = "planning"
        logger.info(f"Received user query: '{user_query}'")

        # Parse user query - simplified example
        query_lower = user_query.lower()
        focus_companies = [] # Default to empty list
        focus_sectors = []

        if "portfolio" in query_lower:
            # If query mentions 'portfolio', get all companies from the CSV
            focus_companies = self.companies_df['ticker'].tolist() # Assuming 'ticker' column exists
            focus_sectors = self.companies_df['sector'].unique().tolist() # Get unique sectors
        elif "specific company" in query_lower: # Example for a specific company query
             # Extract company name/s from query (simplified)
             # This logic would need to be more sophisticated for real use
             potential_tickers = [word.upper() for word in query_lower.split() if len(word) <= 10 and word.isalpha()] # Basic guess
             focus_companies = [ticker for ticker in potential_tickers if ticker in self.companies_df['ticker'].values]

        # Determine monitoring parameters based on config and parsed query
        # For news assessment, focus on 'S' (Social) and 'G' (Governance) aspects often reported in news
        esg_dimensions = self.config.get("focus_dimensions", ["S", "G"])
        time_frame = self.config.get("default_timeframe_days", 30)
        update_frequency = self.config.get("update_frequency_seconds", 3600)
        risk_threshold = self.config.get("risk_threshold", 7.0)

        # Decompose into specific tasks based on focus companies
        tasks = self._decompose_tasks(focus_companies, esg_dimensions, time_frame)

        # Assign priorities (could be more sophisticated, maybe based on sector from CSV)
        priorities = self._assign_priorities(esg_dimensions)

        plan = {
            "plan_id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_query": user_query,
            "companies_from_csv": focus_companies, # Explicitly state the companies used
            "sectors_from_csv": focus_sectors,
            "dimensions": esg_dimensions,
            "time_frame_days": time_frame,
            "risk_threshold": risk_threshold,
            "update_frequency_seconds": update_frequency,
            "tasks": tasks,
            "priorities": priorities,
            "generated_at": datetime.now().isoformat()
        }

        self.status = "idle"
        logger.info(f"Strategy plan created: {plan['plan_id']}")
        logger.info(f"Plan details: Companies={focus_companies}, Sectors={focus_sectors}, Dimensions={esg_dimensions}, Tasks={len(tasks)}")
        return plan

    def _decompose_tasks(self, companies: List[str], dimensions: List[str], time_frame_days: int) -> List[Dict[str, Any]]:
        """Decompose the high-level plan into specific, executable tasks."""
        tasks = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=time_frame_days)

        for company in companies:
            # Get sector info from the loaded CSV (assuming it has a 'sector' column)
            company_row = self.companies_df[self.companies_df['ticker'] == company]
            sector = company_row['sector'].iloc[0] if not company_row.empty else "Unknown"

            for dimension in dimensions:
                # Task for Executor: Fetch news for this company/dimension
                news_task = {
                    "task_id": f"news_{company}_{dimension}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}",
                    "type": "fetch_news",
                    "company": company,
                    "company_sector": sector, # Pass sector info to executor
                    "dimension": dimension,
                    "source": "news_api",
                    "parameters": {
                        "query": f"{company} {dimension} ESG", # Use company from CSV
                        "from_date": start_date.strftime('%Y-%m-%d'),
                        "to_date": end_date.strftime('%Y-%m-%d'),
                        "language": "en"
                    },
                    "priority": "high" if dimension in self.config.get("high_priority_dimensions", ["E", "G"]) else "medium"
                }
                tasks.append(news_task)

        return tasks

    def _assign_priorities(self, dimensions: List[str]) -> Dict[str, int]:
        """Assign default priority scores to ESG dimensions based on config."""
        default_priorities = {
            "E": 10,
            "S": 8,
            "G": 9
        }
        config_priorities = self.config.get("dimension_priorities", {})
        default_priorities.update(config_priorities)
        return default_priorities

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status
