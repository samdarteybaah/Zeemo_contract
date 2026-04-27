from typing import Dict, List

class RiskScorer:
    MAX_SCORE = 10

    @staticmethod
    def score_list(items: List[str]) -> int:
        """Score based on number of items found."""
        count = len(items)
        if count == 0:
            return 0
        elif count == 1:
            return 2
        elif count == 2:
            return 4
        elif count == 3:
            return 5
        elif count == 4:
            return 7
        elif count <= 6:
            return 8
        else:
            return 10

    @classmethod
    def calculate_scores(cls, data: Dict) -> Dict[str, int]:
        return {
            "risks": cls.score_list(data.get("risks", [])),
            "obligations": cls.score_list(data.get("obligations", [])),
            "negotiation_suggestions": cls.score_list(data.get("negotiation_suggestions", [])),
            "ambiguity_flags": cls.score_list(data.get("ambiguity_flags", [])),
        }

    @staticmethod
    def calculate_overall(scores: Dict[str, int]) -> float:
        if not scores:
            return 0.0
        # weight risks and ambiguity more heavily
        weighted = (
            scores.get("risks", 0) * 0.4 +
            scores.get("ambiguity_flags", 0) * 0.3 +
            scores.get("obligations", 0) * 0.2 +
            scores.get("negotiation_suggestions", 0) * 0.1
        )
        return round(min(weighted, 10), 1)