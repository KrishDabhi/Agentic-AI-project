"""Test suite for portfolio and fintech workflow."""

import unittest
from portfolio import DummyPortfolio, RiskCalculator
from utils import get_logger

logger = get_logger(__name__)


class TestPortfolioWorkflow(unittest.TestCase):
    """Test portfolio management and risk calculations."""

    def setUp(self):
        """Set up test portfolio."""
        self.portfolio = DummyPortfolio()
        self.risk_calculator = RiskCalculator(self.portfolio)

    def test_portfolio_creation(self):
        """Test that portfolio is created with companies."""
        portfolio_data = self.portfolio.get_portfolio()
        
        self.assertGreater(len(portfolio_data["companies"]), 0)
        self.assertEqual(portfolio_data["portfolio_id"], "portfolio_001")

    def test_get_company(self):
        """Test retrieving specific company."""
        company = self.portfolio.get_company("COMP001")
        
        self.assertIsNotNone(company)
        self.assertEqual(company["company_id"], "COMP001")

    def test_get_companies_by_sector(self):
        """Test filtering companies by sector."""
        tech_companies = self.portfolio.get_companies_by_sector("Technology")
        
        self.assertGreater(len(tech_companies), 0)
        for company in tech_companies:
            self.assertEqual(company["sector"], "Technology")

    def test_portfolio_summary(self):
        """Test portfolio summary generation."""
        summary = self.portfolio.get_portfolio_summary()
        
        self.assertIn("total_companies", summary)
        self.assertIn("sectors", summary)
        self.assertIn("avg_esg_exposure", summary)

    def test_calculate_company_risk(self):
        """Test company risk calculation."""
        company = self.portfolio.companies[0]
        risk = self.risk_calculator.calculate_company_risk(company)
        
        self.assertIn("overall_risk", risk)
        self.assertIn("risk_level", risk)
        self.assertIn("environmental_risk", risk)

    def test_calculate_portfolio_risk(self):
        """Test portfolio-wide risk calculation."""
        portfolio_risk = self.risk_calculator.calculate_portfolio_risk()
        
        self.assertIn("average_overall_risk", portfolio_risk)
        self.assertIn("max_risk", portfolio_risk)
        self.assertIn("companies_at_high_risk", portfolio_risk)

    def test_get_at_risk_companies(self):
        """Test identifying at-risk companies."""
        at_risk = self.risk_calculator.get_at_risk_companies(risk_threshold=5.0)
        
        # Should find some companies above threshold
        self.assertIsInstance(at_risk, list)


if __name__ == "__main__":
    unittest.main()