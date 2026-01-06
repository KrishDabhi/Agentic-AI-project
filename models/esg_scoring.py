"""ESG Scoring ML Model."""

from typing import Dict, List, Any
import math
from utils.logger import get_logger

logger = get_logger(__name__)


class ESGScoringModel:
    """Machine learning model for ESG incident scoring."""

    def __init__(self):
        """Initialize the ESG Scoring Model."""
        self.model_version = "1.0"
        self.feature_weights = self._initialize_weights()
        logger.info(f"Initialized ESG Scoring Model v{self.model_version}")

    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize feature weights for scoring."""
        return {
            "incident_severity": 0.30,
            "media_coverage": 0.20,
            "financial_impact": 0.25,
            "regulatory_risk": 0.15,
            "stakeholder_sentiment": 0.10,
        }

    def score_incident(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score an ESG incident using the model.
        
        Args:
            incident: Incident data dictionary
            
        Returns:
            Scoring results
        """
        features = self._extract_features(incident)
        scores = self._calculate_feature_scores(features)
        overall_score = self._calculate_overall_score(scores)
        
        return {
            "incident_id": incident.get("incident_id", "unknown"),
            "feature_scores": scores,
            "overall_score": overall_score,
            "risk_level": self._classify_score(overall_score),
            "confidence": self._calculate_confidence(scores),
            "recommendations": self._generate_recommendations(overall_score),
        }

    def _extract_features(self, incident: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from incident data."""
        return {
            "severity": incident.get("severity", 5.0),
            "coverage": incident.get("media_coverage", 3.0),
            "financial_impact": incident.get("financial_impact", 4.0),
            "regulatory_risk": incident.get("regulatory_risk", 5.0),
            "sentiment": incident.get("sentiment", 0.5),
        }

    def _calculate_feature_scores(self, features: Dict[str, float]) -> Dict[str, float]:
        """Calculate scores for individual features."""
        return {
            "incident_severity": min(features["severity"] / 10.0 * 10, 10),
            "media_coverage": min(features["coverage"] / 5.0 * 10, 10),
            "financial_impact": min(features["financial_impact"] / 8.0 * 10, 10),
            "regulatory_risk": min(features["regulatory_risk"] / 10.0 * 10, 10),
            "stakeholder_sentiment": abs(features["sentiment"]) * 10,
        }

    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score."""
        overall = sum(
            scores[key] * self.feature_weights[key]
            for key in self.feature_weights
        )
        return round(min(overall, 10.0), 2)

    def _classify_score(self, score: float) -> str:
        """Classify score into risk level."""
        if score >= 7.5:
            return "CRITICAL"
        elif score >= 5.0:
            return "HIGH"
        elif score >= 3.0:
            return "MEDIUM"
        else:
            return "LOW"

    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate model confidence."""
        # Higher confidence if scores are available and consistent
        avg_score = sum(scores.values()) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores.values()) / len(scores)
        
        # Lower variance = higher confidence
        confidence = 1.0 - min(variance / 25.0, 1.0)
        return round(confidence, 2)

    def _generate_recommendations(self, score: float) -> List[str]:
        """Generate recommendations based on score."""
        recommendations = []
        
        if score >= 8.5:
            recommendations.append("Immediate escalation to executive team required")
            recommendations.append("Activate crisis management protocol")
            recommendations.append("Prepare stakeholder communication")
        elif score >= 7.0:
            recommendations.append("High priority review recommended")
            recommendations.append("Monitor closely for developments")
            recommendations.append("Assess regulatory implications")
        elif score >= 5.0:
            recommendations.append("Regular monitoring advised")
            recommendations.append("Track for trend changes")
        
        return recommendations

    def batch_score(self, incidents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score multiple incidents.
        
        Args:
            incidents: List of incident dictionaries
            
        Returns:
            List of scoring results
        """
        results = []
        for incident in incidents:
            result = self.score_incident(incident)
            results.append(result)
        
        logger.info(f"Batch scored {len(incidents)} incidents")
        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "version": self.model_version,
            "feature_weights": self.feature_weights,
            "max_score": 10.0,
            "min_score": 0.0,
            "risk_levels": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        }
