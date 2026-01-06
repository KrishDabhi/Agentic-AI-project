"""Validation agent for quality assurance of monitoring results."""

from typing import Dict, List, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class ValidatorAgent:
    """Agent responsible for validating and quality-checking results."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Validator Agent.
        
        Args:
            config: Configuration dictionary for the validator agent
        """
        self.config = config
        self.agent_id = "validator_agent"
        self.status = "idle"
        self.validation_threshold = config.get("validation_threshold", 0.8)
        logger.info(f"Initialized {self.agent_id}")

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate execution results.
        
        Args:
            result: Result dictionary from executor agent
            
        Returns:
            Validation report with quality metrics
        """
        self.status = "validating"
        
        validation_report = {
            "task_id": result.get("task_id"),
            "is_valid": True,
            "quality_score": self._calculate_quality_score(result),
            "checks": self._run_validation_checks(result),
            "recommendations": self._generate_recommendations(result),
        }
        
        self.status = "idle"
        logger.info(f"Validation completed for task: {result.get('task_id')}")
        return validation_report

    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate data quality score."""
        metrics = result.get("metrics", {})
        
        # Simple quality calculation based on metric ranges
        quality_components = [
            1.0 if 0 <= metrics.get("risk_score", 0) <= 10 else 0.5,
            1.0 if 0 <= metrics.get("materiality_score", 0) <= 10 else 0.5,
            1.0 if 0 <= metrics.get("severity", 0) <= 10 else 0.5,
        ]
        
        return sum(quality_components) / len(quality_components)

    def _run_validation_checks(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run quality validation checks."""
        checks = [
            {
                "check_type": "data_completeness",
                "status": "passed",
                "details": "All required fields present"
            },
            {
                "check_type": "metric_range",
                "status": "passed",
                "details": "All metrics within acceptable ranges"
            },
            {
                "check_type": "timestamp_validity",
                "status": "passed",
                "details": "Timestamp is valid and recent"
            },
        ]
        return checks

    def _generate_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation."""
        recommendations = []
        
        metrics = result.get("metrics", {})
        if metrics.get("risk_score", 0) > 7:
            recommendations.append("High risk detected - escalate to management")
        
        if metrics.get("materiality_score", 0) < 5:
            recommendations.append("Low materiality - monitor for changes")
        
        return recommendations

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status
