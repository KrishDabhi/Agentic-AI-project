import yaml
from typing import Dict, List, Any
from utils.logger import get_logger
import os

logger = get_logger(__name__)

class ValidatorAgent:
    """Agent responsible for validating and quality-checking results from the Executor."""

    def __init__(self, config_path: str = "config/agent_configs/validator_config.yml"):
        """
        Initialize the Validator Agent by loading its YAML configuration.
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.agent_id = "validator_agent"
        self.status = "idle"
        self.validation_threshold = self.config.get("validation_threshold", 0.8)
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

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate execution results received from the Executor Agent.
        """
        self.status = "validating"
        task_id = result.get("task_id", "unknown")
        logger.info(f"Validating result for task: {task_id}")

        try:
            checks = self._run_validation_checks(result)
            is_overall_valid = all(check["status"] == "passed" for check in checks)

            quality_score = self._calculate_quality_score(result)
            recommendations = self._generate_recommendations(result, quality_score)

            final_is_valid = is_overall_valid and quality_score >= self.validation_threshold

            validation_report = {
                "task_id": task_id,
                "is_valid": final_is_valid,
                "overall_quality_score": quality_score,
                "validation_threshold": self.validation_threshold,
                "checks": checks,
                "recommendations": recommendations,
                "validated_at": self._get_timestamp(),
            }

        except Exception as e:
            logger.error(f"Error validating result for task {task_id}: {e}")
            validation_report = {
                "task_id": task_id,
                "is_valid": False,
                "overall_quality_score": 0.0,
                "error": str(e),
                "checks": [{"check_type": "validation_error", "status": "failed", "details": str(e)}],
                "recommendations": ["Investigate validation failure for this task."],
                "validated_at": self._get_timestamp(),
            }

        self.status = "idle"
        logger.info(f"Validation completed for task: {task_id}, Valid: {validation_report['is_valid']}")
        return validation_report

    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate a composite data quality score."""
        metrics = result.get("metrics", {})
        data_info = result.get("data", {}).get("processed_data", [])

        score_components = []

        for key, value in metrics.items():
            if isinstance(value, (int, float)) and 0 <= value <= 10:
                score_components.append(1.0)
            else:
                score_components.append(0.5)

        if data_info:
            score_components.append(1.0)
        else:
            score_components.append(0.3)

        if score_components:
            final_score = sum(score_components) / len(score_components)
        else:
            final_score = 0.0

        weight = self.config.get("quality_score_weight", 1.0)
        return round(final_score * weight, 2)

    def _run_validation_checks(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run specific quality validation checks."""
        checks = []
        status = result.get("status", "unknown")
        data = result.get("data", {})
        metrics = result.get("metrics", {})

        checks.append({
            "check_type": "execution_status",
            "status": "passed" if status == "completed" else "failed",
            "details": f"Execution status was {status}"
        })

        checks.append({
            "check_type": "data_presence",
            "status": "passed" if data else "failed",
            "details": "Data dictionary is present" if data else "Data dictionary is missing"
        })

        risk_score = metrics.get("risk_score", -1)
        materiality_score = metrics.get("materiality_score", -1)
        severity = metrics.get("severity", -1)

        checks.append({
            "check_type": "metric_range_risk",
            "status": "passed" if 0 <= risk_score <= 10 else "failed",
            "details": f"Risk score {risk_score} is within range 0-10" if 0 <= risk_score <= 10 else f"Risk score {risk_score} is out of range 0-10"
        })

        checks.append({
            "check_type": "metric_range_materiality",
            "status": "passed" if 0 <= materiality_score <= 10 else "failed",
            "details": f"Materiality score {materiality_score} is within range 0-10" if 0 <= materiality_score <= 10 else f"Materiality score {materiality_score} is out of range 0-10"
        })

        checks.append({
            "check_type": "metric_range_severity",
            "status": "passed" if 0 <= severity <= 10 else "failed",
            "details": f"Severity score {severity} is within range 0-10" if 0 <= severity <= 10 else f"Severity score {severity} is out of range 0-10"
        })

        timestamp = result.get("timestamp", "")
        import re
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$'
        checks.append({
            "check_type": "timestamp_validity",
            "status": "passed" if re.match(iso_pattern, timestamp) else "failed",
            "details": f"Timestamp '{timestamp}' is valid ISO format" if re.match(iso_pattern, timestamp) else f"Timestamp '{timestamp}' is invalid"
        })

        return checks

    def _generate_recommendations(self, result: Dict[str, Any], quality_score: float) -> List[str]:
        """Generate recommendations based on validation results and config."""
        recommendations = []
        metrics = result.get("metrics", {})
        task_id = result.get("task_id", "")
        # Get company info from the processed data if available
        processed_data = result.get("data", {}).get("processed_data", [])
        if processed_data:
             company_ticker = processed_data[0].get("company_ticker", "UNKNOWN_COMPANY") # Get from first item
        else:
             company_ticker = "UNKNOWN_COMPANY_FROM_TASK"
             # Or get from task ID parsing if needed: task_id.split('_')[1] if task_id.startswith('news_')

        if quality_score < self.config.get("low_quality_threshold", 0.6):
            recommendations.append(f"Low data quality detected for task {task_id} (Company: {company_ticker}). Review source data and collection process.")
        elif quality_score < self.validation_threshold:
            recommendations.append(f"Moderate data quality for task {task_id} (Company: {company_ticker}). Consider re-running or manual verification.")

        if metrics.get("risk_score", 0) > self.config.get("high_risk_threshold", 8.0):
            recommendations.append(f"High ESG risk detected ({metrics['risk_score']}) for company {company_ticker} (Task: {task_id}). Escalate to risk management team.")
        if metrics.get("severity", 0) > self.config.get("high_severity_threshold", 7.0):
            recommendations.append(f"High severity ESG event detected ({metrics['severity']}) for company {company_ticker} (Task: {task_id}). Immediate attention required.")

        checks = self._run_validation_checks(result)
        failed_checks = [c for c in checks if c["status"] != "passed"]
        if failed_checks:
             recommendations.append(f"Task {task_id} (Company: {company_ticker}) had {len(failed_checks)} validation failures. Investigate: {[c['check_type'] for c in failed_checks]}")

        if not recommendations:
            recommendations.append(f"Task {task_id} (Company: {company_ticker}) results validated successfully.")

        return recommendations

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status