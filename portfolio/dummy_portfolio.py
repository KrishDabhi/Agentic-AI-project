from typing import Dict, List, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class DummyPortfolio:
    """Manages a synthetic portfolio of companies for ESG risk analysis."""

    def __init__(self):
        """Initialize the dummy portfolio."""
        self.companies = self._create_dummy_companies()
        self.portfolio_id = "portfolio_001"
        logger.info("Initialized Dummy Portfolio")

    def _create_dummy_companies(self) -> List[Dict[str, Any]]:
        """Create a set of dummy companies for testing."""
        return [
            {
                "company_id": "COMP001",
            
                "name": "TechCorp Industries",
                "sector": "Technology",
                "country": "USA",
                "market_cap": 500e9,  # $500B
                "esg_exposure": {"E": 0.8, "S": 0.6, "G": 0.7},
            },
            {
                "company_id": "COMP002",
                "name": "GreenEnergy Ltd",
                "sector": "Energy",
                "country": "UK",
            
                "market_cap": 150e9,  # $150B
                "esg_exposure": {"E": 0.95, "S": 0.5, "G": 0.8},
            },
            {
                "company_id": "COMP003",
                "name": "RetailGlobal Co",
                "sector": "Retail",
                "country": "Canada",
                "market_cap": 80e9,  # $80B
                "esg_exposure": {"E": 0.6, "S": 0.85, "G": 0.65},
            },
            {
                "company_id": "COMP004",
                "name": "FinanceFirst Group",
                "sector": "Finance",
                "country": "Singapore",
                "market_cap": 200e9,  # $200B
                "esg_exposure": {"E": 0.5, "S": 0.7, "G": 0.95},
            },
            {
                "company_id": "COMP005",
                "name": "ConstructionPro Ltd",
                "sector": "Construction",
                "country": "Germany",
                "market_cap": 50e9,  # $50B
                "esg_exposure": {"E": 0.75, "S": 0.65, "G": 0.6},
            },
        ]

    def get_portfolio(self) -> Dict[str, Any]:
        """Get portfolio details."""
        return {
            "portfolio_id": self.portfolio_id,
            "total_companies": len(self.companies),
            "total_market_cap": sum(c["market_cap"] for c in self.companies),
            "companies": self.companies,
        }

    def get_company(self, company_id: str) -> Dict[str, Any]:
        """Get a specific company from portfolio."""
        for company in self.companies:
            if company["company_id"] == company_id:
                return company
        return None

    def get_companies_by_sector(self, sector: str) -> List[Dict[str, Any]]:
        """Get companies by sector."""
        return [c for c in self.companies if c["sector"] == sector]

    def get_high_esg_risk_companies(self, dimension: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Get companies with high ESG risk in a specific dimension."""
        high_risk = []
        for company in self.companies:
            if company["esg_exposure"].get(dimension, 0) > threshold:
                high_risk.append(company)
        return high_risk

    def add_company(self, company: Dict[str, Any]) -> bool:
        """Add a company to the portfolio."""
        if any(c["company_id"] == company["company_id"] for c in self.companies):
            logger.warning(f"Company {company['company_id']} already exists")
            return False
        
        self.companies.append(company)
        logger.info(f"Added company: {company['company_id']}")
        return True

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get summary statistics for the portfolio."""
        return {
            "portfolio_id": self.portfolio_id,
            "total_companies": len(self.companies),
            "sectors": list(set(c["sector"] for c in self.companies)),
            "countries": list(set(c["country"] for c in self.companies)),
            "avg_esg_exposure": {
                "E": sum(c["esg_exposure"]["E"] for c in self.companies) / len(self.companies),
                "S": sum(c["esg_exposure"]["S"] for c in self.companies) / len(self.companies),
                "G": sum(c["esg_exposure"]["G"] for c in self.companies) / len(self.companies),
            },
        }

    def run_monitoring_cycle(self, companies: List[str] = None, dimensions: List[str] = None) -> Dict[str, Any]:
        """Run a monitoring cycle for the portfolio.

        Args:
            companies: List of companies to monitor
            dimensions: ESG dimensions to monitor
        Returns:
            Results of the monitoring cycle 
        """
        if not companies:
            companies = [c["name"] for c in self.companies[:3]]
        
        if not dimensions:
            dimensions = ["E", "S", "G"]
        
        logger.info(f"Running monitoring cycle for {companies} - dimensions {dimensions}")
        
        # Dummy results for demonstration
        cycle_result = {
            "cycle_id": "cycle_001",
            "monitored_companies": companies,
            "monitored_dimensions": dimensions,
            "status": "completed",
            "findings": [
                {"company": company, "dimension": dim, "risk_level": "low"}
                for company in companies for dim in dimensions
            ],
        }
        
        logger.info("Monitoring cycle completed")
        return cycle_result
