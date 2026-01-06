"""Risk calculation module for ESG analysis."""

from typing import Dict, List, Any
import math
from utils.logger import get_logger

logger = get_logger(__name__)


class RiskCalculator:
    """Calculate ESG risks and metrics for portfolio companies."""

    def __init__(self, portfolio=None):
        """
        Initialize the Risk Calculator.
        
        Args:
            portfolio: Portfolio object containing companies
        """
        self.portfolio = portfolio
        self.risk_cache = {}
        logger.info("Initialized Risk Calculator")

    def calculate_company_risk(self, company: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate overall risk score for a company.
        
        Args:
            company: Company dictionary
            
        Returns:
            Risk metrics dictionary
        """
        company_id = company["company_id"]
        
        if company_id in self.risk_cache:
            return self.risk_cache[company_id]
        
        esg_exposure = company.get("esg_exposure", {})
        
        risk_metrics = {
            "environmental_risk": self._calculate_dimension_risk(esg_exposure.get("E", 0.5)),
            "social_risk": self._calculate_dimension_risk(esg_exposure.get("S", 0.5)),
            "governance_risk": self._calculate_dimension_risk(esg_exposure.get("G", 0.5)),
        }
        
        # Calculate weighted overall risk
        risk_metrics["overall_risk"] = (
            0.4 * risk_metrics["environmental_risk"] +
            0.35 * risk_metrics["social_risk"] +
            0.25 * risk_metrics["governance_risk"]
        )
        
        # Add severity classification
        risk_metrics["risk_level"] = self._classify_risk_level(risk_metrics["overall_risk"])
        
        self.risk_cache[company_id] = risk_metrics
        return risk_metrics

    def calculate_portfolio_risk(self) -> Dict[str, Any]:
        """Calculate aggregate risk for the entire portfolio."""
        if not self.portfolio:
            logger.warning("No portfolio loaded")
            return {}
        
        companies = self.portfolio.get_portfolio().get("companies", [])
        
        if not companies:
            return {"error": "No companies in portfolio"}
        
        all_risks = [self.calculate_company_risk(c) for c in companies]
        
        portfolio_risk = {
            "portfolio_id": self.portfolio.portfolio_id,
            "total_companies": len(companies),
            "average_overall_risk": sum(r["overall_risk"] for r in all_risks) / len(all_risks),
            "average_environmental_risk": sum(r["environmental_risk"] for r in all_risks) / len(all_risks),
            "average_social_risk": sum(r["social_risk"] for r in all_risks) / len(all_risks),
            "average_governance_risk": sum(r["governance_risk"] for r in all_risks) / len(all_risks),
            "max_risk": max(r["overall_risk"] for r in all_risks),
            "min_risk": min(r["overall_risk"] for r in all_risks),
            "companies_at_high_risk": sum(1 for r in all_risks if r["risk_level"] == "HIGH"),
            "companies_at_medium_risk": sum(1 for r in all_risks if r["risk_level"] == "MEDIUM"),
            "companies_at_low_risk": sum(1 for r in all_risks if r["risk_level"] == "LOW"),
        }
        
        return portfolio_risk

    def _calculate_dimension_risk(self, exposure: float) -> float:
        """
        Calculate risk for a specific ESG dimension.
        
        Args:
            exposure: Exposure level (0.0-1.0)
            
        Returns:
            Risk score (0.0-10.0)
        """
        # Convert exposure to risk score (inverse relationship)
        # Higher exposure = lower risk (better performance)
        return (1.0 - exposure) * 10.0

    def _classify_risk_level(self, risk_score: float) -> str:
        """
        Classify risk into levels.
        
        Args:
            risk_score: Risk score (0.0-10.0)
            
        Returns:
            Risk level classification
        """
        if risk_score >= 7.5:
            return "HIGH"
        elif risk_score >= 5.0:
            return "MEDIUM"
        else:
            return "LOW"

    def get_at_risk_companies(self, risk_threshold: float = 7.0) -> List[Dict[str, Any]]:
        """
        Get companies with risk above threshold.
        
        Args:
            risk_threshold: Risk score threshold
            
        Returns:
            List of companies with high risk
        """
        if not self.portfolio:
            return []
        
        companies = self.portfolio.get_portfolio().get("companies", [])
        at_risk = []
        
        for company in companies:
            risk = self.calculate_company_risk(company)
            if risk["overall_risk"] > risk_threshold:
                at_risk.append({
                    "company": company,
                    "risk": risk
                })
        
        return sorted(at_risk, key=lambda x: x["risk"]["overall_risk"], reverse=True)

    def clear_cache(self) -> None:
        """Clear the risk cache."""
        self.risk_cache.clear()
        logger.info("Risk cache cleared")
