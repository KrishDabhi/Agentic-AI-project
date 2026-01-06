"""Data management module for synthetic data generation and processing."""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)


class SyntheticDataGenerator:
    """Generate synthetic ESG data for testing and demonstration."""

    def __init__(self, seed: int = 42):
        """
        Initialize the synthetic data generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        random.seed(seed)
        self.data_id_counter = 1000
        logger.info("Initialized Synthetic Data Generator")

    def generate_incidents(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Generate synthetic ESG incidents.
        
        Args:
            count: Number of incidents to generate
            
        Returns:
            List of synthetic incident dictionaries
        """
        incidents = []
        
        companies = ["TechCorp", "GreenEnergy", "RetailGlobal", "FinanceFirst", "ConstructionPro"]
        dimensions = ["E", "S", "G"]
        sources = ["news", "social_media", "internal_report", "regulatory_filing"]
        
        for _ in range(count):
            incident = {
                "incident_id": f"INC{self.data_id_counter:06d}",
                "company": random.choice(companies),
                "dimension": random.choice(dimensions),
                "title": self._generate_incident_title(random.choice(dimensions)),
                "description": self._generate_description(),
                "severity": round(random.uniform(1, 10), 1),
                "source": random.choice(sources),
                "date": self._generate_date(),
                "media_coverage": random.randint(1, 5),
                "financial_impact": round(random.uniform(0, 100), 2),
                "regulatory_risk": random.randint(1, 10),
                "sentiment": round(random.uniform(-1, 1), 2),
                "status": random.choice(["reported", "investigating", "resolved"]),
            }
            incidents.append(incident)
            self.data_id_counter += 1
        
        logger.info(f"Generated {count} synthetic incidents")
        return incidents

    def generate_news_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """
        Generate synthetic news articles.
        
        Args:
            count: Number of news items to generate
            
        Returns:
            List of synthetic news dictionaries
        """
        news_items = []
        
        companies = ["TechCorp", "GreenEnergy", "RetailGlobal", "FinanceFirst", "ConstructionPro"]
        keywords = ["sustainability", "ESG", "carbon", "risk", "governance", "compliance", "ethics"]
        
        for i in range(count):
            news = {
                "news_id": f"NEWS{i+1:05d}",
                "company": random.choice(companies),
                "headline": f"{random.choice(keywords).title()} Concerns for {random.choice(companies)}",
                "content": self._generate_description(),
                "url": f"https://example.com/news/{i+1}",
                "published_date": self._generate_date(),
                "source": random.choice(["Reuters", "Bloomberg", "Financial Times", "BBC"]),
                "sentiment_score": round(random.uniform(-1, 1), 2),
                "relevance_score": round(random.uniform(0, 1), 2),
            }
            news_items.append(news)
        
        logger.info(f"Generated {count} synthetic news items")
        return news_items

    def generate_market_data(self, days: int = 365) -> List[Dict[str, Any]]:
        """
        Generate synthetic market/financial data.
        
        Args:
            days: Number of days of data to generate
            
        Returns:
            List of synthetic market data dictionaries
        """
        companies = ["TechCorp", "GreenEnergy", "RetailGlobal", "FinanceFirst", "ConstructionPro"]
        market_data = []
        
        base_date = datetime.now() - timedelta(days=days)
        
        for company in companies:
            current_price = random.uniform(50, 500)
            
            for day in range(days):
                date = base_date + timedelta(days=day)
                price_change = random.uniform(-0.05, 0.05)
                current_price = current_price * (1 + price_change)
                
                data = {
                    "date": date.isoformat(),
                    "company": company,
                    "open_price": round(current_price * 0.98, 2),
                    "close_price": round(current_price, 2),
                    "high_price": round(current_price * 1.02, 2),
                    "low_price": round(current_price * 0.97, 2),
                    "volume": random.randint(100000, 10000000),
                    "volatility": round(random.uniform(0.1, 0.5), 3),
                }
                market_data.append(data)
        
        logger.info(f"Generated {len(market_data)} market data points")
        return market_data

    def _generate_incident_title(self, dimension: str) -> str:
        """Generate a synthetic incident title."""
        templates = {
            "E": [
                "Carbon emissions exceed targets",
                "Environmental violation detected",
                "Waste management issue reported",
                "Water contamination reported",
            ],
            "S": [
                "Labor dispute in facilities",
                "Community concern raised",
                "Diversity metrics questioned",
                "Health and safety incident reported",
            ],
            "G": [
                "Board governance issue flagged",
                "Executive compensation questioned",
                "Ethical violation reported",
                "Compliance breach detected",
            ],
        }
        return random.choice(templates.get(dimension, ["Incident reported"]))

    def _generate_description(self) -> str:
        """Generate a synthetic incident description."""
        templates = [
            "Multiple reports indicate potential issues in operations",
            "Internal investigation launched into reported concerns",
            "Third-party assessment revealed areas for improvement",
            "Stakeholders raised concerns about company practices",
            "New data suggests need for policy review and updates",
        ]
        return random.choice(templates)

    def _generate_date(self) -> str:
        """Generate a recent synthetic date."""
        days_ago = random.randint(0, 90)
        date = datetime.now() - timedelta(days=days_ago)
        return date.isoformat()
