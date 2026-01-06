import yaml
import requests
from typing import Dict, List, Any
from utils.logger import get_logger
import os
import json
import pandas as pd

logger = get_logger(__name__)

class ExecutorAgent:
    """Agent responsible for executing monitoring and data collection tasks based on the plan."""

    def __init__(self, config_path: str = "config/agent_configs/executor_config.yml"):
        """
        Initialize the Executor Agent by loading its YAML configuration.
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.agent_id = "executor_agent"
        self.status = "idle"
        self.news_api_key = self.config.get("api_keys", {}).get("news_api_key") or os.getenv("NEWS_API_KEY")
        self.companies_df = self._load_companies_data() # Load company data to potentially get more details
        logger.info(f"Initialized {self.agent_id}")

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
            logger.info(f"Executor loaded company data from {csv_path}")
            return df
        except FileNotFoundError:
            logger.warning(f"Companies CSV file not found for Executor: {csv_path}. Continuing without it.")
            return pd.DataFrame() # Return empty DataFrame if not found
        except Exception as e:
            logger.error(f"Error loading companies CSV for Executor: {e}")
            return pd.DataFrame() # Return empty DataFrame on error

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single monitoring task based on the plan.
        """
        self.status = "executing"
        task_id = task.get("task_id", "unknown")
        task_type = task.get("type", "unknown")
        logger.info(f"Executing task: {task_id} (Type: {task_type})")

        try:
            if task_type == "fetch_news":
                result_data = self._fetch_news_data(task)
            else:
                logger.warning(f"Unknown task type: {task_type}. Returning empty data.")
                result_data = {"raw_data": [], "processed_data": {}}

            # Calculate metrics based on the collected data
            metrics = self._calculate_metrics(result_data, task)

            result = {
                "task_id": task_id,
                "status": "completed",
                "data": result_data,
                "metrics": metrics,
                "timestamp": self._get_timestamp(),
            }

            if self.config.get("store_raw_data", True):
                self._store_raw_data(result_data, task_id)

        except Exception as e:
            logger.error(f"Error executing task {task_id}: {e}")
            result = {
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

        self.status = "idle"
        return result

    def _fetch_news_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch news data based on task parameters using a public API or synthetic data."""
        params = task.get("parameters", {})
        query = params.get("query", "")
        from_date = params.get("from_date", "")
        to_date = params.get("to_date", "")
        company = task.get("company", "") # Get company from task
        dimension = task.get("dimension", "") # Get dimension from task

        if not self.news_api_key:
            logger.warning("News API key not found. Generating synthetic news data.")
            return self._generate_synthetic_news_data(task) # Fallback using task details

        url = "https://newsapi.org/v2/everything"
        headers = {"X-Api-Key": self.news_api_key}
        api_params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 100
        }

        try:
            response = requests.get(url, params=api_params, headers=headers)
            response.raise_for_status()
            raw_news_data = response.json()

            # Process the raw data
            processed_articles = []
            for article in raw_news_data.get('articles', []):
                 processed_article = {
                     "title": article.get("title"),
                     "description": article.get("description"),
                     "url": article.get("url"),
                     "published_at": article.get("publishedAt"),
                     "source": article.get("source", {}).get("name"),
                     "company_ticker": company, # Link back to company from CSV
                     "esg_dimension": dimension, # Link back to dimension
                     "relevance_score": self._calculate_article_relevance(article, dimension)
                 }
                 processed_articles.append(processed_article)

            logger.info(f"Fetched {len(processed_articles)} relevant news articles for company {company} and task {task.get('task_id')}")
            return {"raw_data": raw_news_data, "processed_data": processed_articles}

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news data from API: {e}")
            return self._generate_synthetic_news_data(task) # Fallback

    def _generate_synthetic_news_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate synthetic news data using company and dimension info from the task."""
        import random
        company = task.get("company", "UNKNOWN")
        dimension = task.get("dimension", "UNKNOWN")
        synthetic_articles = []
        for i in range(random.randint(1, 3)):
            # Create more realistic synthetic titles based on company and dimension
            title_prefixes = {
                "E": f"{company} Environmental",
                "S": f"{company} Social",
                "G": f"{company} Governance"
            }
            prefix = title_prefixes.get(dimension, f"{company} ESG")
            synthetic_articles.append({
                "title": f"{prefix} News Update - {i+1}",
                "description": f"A simulated article discussing {dimension}-related aspects for {company}.",
                "url": f"https://example.com/synthetic_news_{company}_{i}",
                "published_at": self._get_timestamp(),
                "source": "Synthetic News Source",
                "company_ticker": company,
                "esg_dimension": dimension,
                "relevance_score": round(random.uniform(0.5, 0.9), 2)
            })
        logger.info(f"Generated {len(synthetic_articles)} synthetic news articles for company {company} and task {task.get('task_id')}")
        return {"raw_data": {"articles": synthetic_articles}, "processed_data": synthetic_articles}

    def _calculate_article_relevance(self, article: Dict[str, Any], dimension: str) -> float:
        """Calculate relevance score based on keywords."""
        title_desc = (article.get("title", "") + " " + article.get("description", "")).lower()
        keywords = {
            "E": ["environment", "climate", "emission", "pollution", "waste", "energy"],
            "S": ["social", "diversity", "labor", "human rights", "community", "stakeholder"],
            "G": ["governance", "board", "executive", "ethics", "compliance", "audit"]
        }
        score = 0.0
        if dimension in keywords:
            for kw in keywords[dimension]:
                if kw in title_desc:
                    score += 0.1
        return min(score, 1.0)

    def _calculate_metrics(self, data: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, float]:
        """Calculate relevant metrics based on collected data."""
        processed_data = data.get("processed_data", [])
        if not processed_data:
            return {"risk_score": 0.0, "materiality_score": 0.0, "severity": 0.0}

        # Calculate metrics based on processed news articles
        total_relevance = sum(item.get("relevance_score", 0.0) for item in processed_data)
        avg_relevance = total_relevance / len(processed_data) if processed_data else 0.0
        max_relevance = max((item.get("relevance_score", 0.0) for item in processed_data), default=0.0)

        # Use company sector info from the task (originally from CSV) for materiality
        company_sector = task.get("company_sector", "default")
        sector_weights = self.config.get("sector_materiality_weights", {})
        materiality_weight = sector_weights.get(company_sector, 1.0) # Default weight if sector not found

        return {
            "risk_score": round(avg_relevance * 10.0, 2),
            "materiality_score": round(materiality_weight * avg_relevance * 10.0, 2),
            "severity": round(max_relevance * 10.0, 2)
        }

    def _store_raw_data(self, data: Dict[str, Any], task_id: str):
        """Store raw collected data in data/raw/ folder."""
        import os
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"raw_{task_id}_{timestamp}.json"
        filepath = os.path.join("data", "raw", filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w') as f:
                json.dump(data["raw_data"], f, indent=2)
            logger.info(f"Raw data for task {task_id} stored at {filepath}")
        except Exception as e:
            logger.error(f"Failed to store raw data for task {task_id}: {e}")

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status
    
